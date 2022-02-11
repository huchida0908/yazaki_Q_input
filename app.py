from operator import length_hint
import string
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 
import hashlib
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
import datetime

# write data to sqlite

db_path = r"G:\マイドライブ\001.project\43.yazaki_dx\20_検討資料\25.長崎DX\8.webapp\yazaki_Q_input\quality_db.sqlite3"
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class Quality(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    kanri = Column(String(length=255))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    kako_no = Column(Integer)
    hinban = Column(String(length = 255))
    result = Column(Float)

    __tablename__ = 't_quality'

Base.metadata.create_all(bind=engine)

st.title('工程能力管理')

kanri = st.radio(
     "初物管理",
     ('初物', '終物', 'その他'))

number = st.number_input('加工済みロット数', step=1)
st.write('加工数 ：', number*25 )

code = st.text_input('看板バーコード')
st.write('品番 ：', code)

# 品番

result = st.number_input('被覆剥取長[mm]')
st.write('被覆剥取長 ：', result )

if st.button('登録'):
    Data = Quality(kanri=kanri,kako_no=number,hinban=code,result=result)
    session.add(Data)
    session.commit()

    st.write(f'{code}の{kanri}実績値を登録しました。')
