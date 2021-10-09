from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Float, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    c_id = Column(Integer, unique=True)
    onwer_id = Column(BigInteger) #owner can not equal bank owner
    bank_id = Column(Integer) #main bank

    name = Column(String) #name of currency
    code = Column(String) #3char
    rate = Column(Float(asdecimal=True)) #rate for vbc
    created_at = Column(DateTime, server_default=func.now())
    amount = Column(BigInteger) #amount of all currency. can inclease by owner.

    ext = Column(postgresql.JSONB) #for addtional informations storage. this column must be use dict like.
