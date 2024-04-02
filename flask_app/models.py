from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Files(db.Model):
    __tablename__ = "files"
    __table_args__ = {"schema": "mean_prices"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.Date(), nullable=False,
                             default=datetime.datetime.now)
    status = db.Column(db.Boolean(), default=False, nullable=False)


class Prices(db.Model):
    __tablename__ = "prices"
    __table_args__ = {"schema": "mean_prices"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.ForeignKey("mean_prices.files.id"), nullable=False)
    gas_type = db.Column(db.String(128), unique=True, nullable=False)
    gas_price = db.Column(db.Float(), unique=True, nullable=False)
