from operator import length_hint
from random import choice
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
from sqlalchemy.sql import select
import datetime


def main():

    db_path = r"./quality_db.sqlite3"
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

    menu = ["実績登録","データチェック","不具合入力"]
    choice = st.sidebar.selectbox("メニュー",menu)

    
    if choice == "実績登録":
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
        
    elif choice == "データチェック":
        st.title('データチェック')

        # select
        sql_statement = (
            select([
                Quality.id,
                Quality.hinban,
                Quality.kako_no,
                Quality.created_at,
                Quality.result
            ])
            
        )

        df = pd.read_sql_query(sql=sql_statement, con=engine)

        st.write(df)

    elif choice =="不具合入力":
        data = st.file_uploader("upload file")


if __name__ == '__main__':
    main()