from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Float, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    c_id = Column(Integer, unique=True)
    onwer_id = Column(BigInteger)
    bank_id = Column(Integer)
    name = Column(String)
    code = Column(String) #3char
    rate = Column(Float(asdecimal=True)) #rate for vbc
    created_at = Column(DateTime, server_default=func.now())
