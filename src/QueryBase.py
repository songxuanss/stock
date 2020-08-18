import sqlalchemy
import tushare as ts


class QueryBase:
    ts.set_token('028572c95ef3d09342d099f2a44c61425d4b0ee0e7cbbff00104ba70')
    pro = ts.pro_api()


class DbBase(QueryBase):
    engine = sqlalchemy.create_engine(
                "mysql+pymysql://stock:Sto3345678!@47.108.140.102:3306/stock",
                echo=True,
            )