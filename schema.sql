create table services (
  ip unique not null,
  cluster text not null,
  counter integer not null
);
