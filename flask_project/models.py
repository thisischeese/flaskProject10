# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Info(Base):
    __tablename__ = 'info'

    email = Column(String(40), primary_key=True)
    username = Column(String(15), nullable=False)
    password = Column(String(40), nullable=False)
    id = Column(String(40))


class Worksheet(Base):
    __tablename__ = 'worksheet'

    word = Column(String(40), primary_key=True)
    image = Column(String(500))
    meaning = Column(String(100), nullable=False)
    subject = Column(TINYINT, nullable=False, comment='1,2,3')


class History(Base):
    __tablename__ = 'history'

    date = Column(Date, primary_key=True)
    sheetCnt = Column(SmallInteger)
    wrongCnt = Column(SmallInteger)
    email = Column(ForeignKey('info.email'), nullable=False, index=True)

    info = relationship('Info')


class Note(Base):
    __tablename__ = 'note'

    seq = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    memo = Column(String(500))
    word = Column(ForeignKey('worksheet.word'), nullable=False, index=True, comment='workcheet 외래키')
    email = Column(ForeignKey('info.email'), nullable=False, index=True, comment='userInfo 외래키')

    info = relationship('Info')
    worksheet = relationship('Worksheet')
