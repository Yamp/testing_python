from dataclasses import dataclass


@dataclass()
class Postgres:
    host:str
    dbname:str
    user:str
    password:str

@dataclass()
class Sqlite:
    database:str
