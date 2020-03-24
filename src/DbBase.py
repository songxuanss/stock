import sqlalchemy
from src.QueryBase import QueryBase
from sqlalchemy.ext.declarative import declarative_base

class DbBase(QueryBase):
    engine = sqlalchemy.create_engine(
                "postgresql://postgres:postgres@47.108.140.102:5432/stock",
                echo=True
            )

