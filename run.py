#!bin/python
from flask import request, send_from_directory, abort, make_response
from flask import Flask
import sqlite3
import ipaddress

app = Flask(__name__)
app.config.from_object(__name__)


def get_db():
    return sqlite3.connect('services.db')


@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    if db is not None:
        db.close()


def validate_index(request):
        try:
            ip_addr = request.json['ip_address']
            role = request.json['role']
        except:
            abort(make_response("json is invalid or missing", 400))
        valid_roles = [u'web', u'worker', u'etl']
        if role not in valid_roles:
            err = "role is invalid. Valid roles are: " + ','.join(valid_roles)
            abort(make_response(err, 400))
        try:
            ip = ipaddress.ip_address(ip_addr)
        except ValueError:
            abort(make_response("ip_address is invalid", 400))
        if not isinstance(ip, ipaddress.IPv4Address):
            abort(make_response("not an ipv4 address", 400))
        return (ip_addr, role)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return send_from_directory('static', 'index.txt')
    else:
        (ip, role) = validate_index(request)
        db = get_db()
        sql = """SELECT
                     ip, cluster || counter as role
              FROM services WHERE ip=?"""
        c = db.execute(sql, [ip])
        rows = c.fetchall()
        if rows:
            print 'FOUND'
            print rows[0][1]
            return rows[0][1]
        if not rows:
            print 'NOT FOUND'
            # Find max of role
            sql = "SELECT MAX(counter) FROM services WHERE cluster=?"
            c = db.execute(sql, [role])
            counter = c.fetchall()[0][0]
            if counter is None:
                counter = 0
            counter = counter + 1

            # Add to db
            sql = "INSERT INTO services VALUES (?,?,?)"
            db.execute(sql, [ip, role, counter])
            db.commit()
            newrole = '%s%i' % (role, counter)
            print newrole
            return newrole


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
