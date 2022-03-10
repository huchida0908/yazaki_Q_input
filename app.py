from operator import length_hint
from random import choice
from re import sub
import string
from unicodedata import name
from PIL import Image
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
import os
from dotenv import load_dotenv
import boto3
import mysql.connector

def main():

    # db_path = r"./quality_db.sqlite3"
    # engine = sqlalchemy.create_engine(f'sqlite:///{db_path}', echo=True)
    engine = sqlalchemy.create_engine("mariadb///?User="mclaren_type_r"&Password="MI6-fallout!"&Database="yazaki"&Server="113.41.135.102"&Port=3307")

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

        person_list = ["矢澤", "中村", "内田","松村"]
        fuguai_group = ["前工程", "自工程"]


        file = st.file_uploader("upload file")

        if file:
            st.write(file)
            st.markdown(f"{file.name}をアップロードしました")

            Filename = file.name

        writer_person = st.selectbox("記入者", person_list)

        fuguai_group = st.multiselect("不良分類", fuguai_group)

        st.write("不具合内容を入力")
        fuguai_detail = st.text_area("不具合内容を記載してください")


        submit = st.button("提出")

        if submit:
            
            IMG_PATH = 'imgs'
            img_path = os.path.join(IMG_PATH, file.name)

            # 画像を保存する
            with open(img_path, 'wb') as f:
                f.write(file.read())

            # 保存した画像を表示
            img = Image.open(img_path)
            st.image(img)

            load_dotenv()
            client = boto3.client('s3',
                aws_access_key_id=os.environ.get("aws_access_key_id"),
                aws_secret_access_key=os.environ.get("aws_secret_access_key"),

                region_name='ap-northeast-1'
            )
            Bucket = 'yazaki-data'
            
            Key = f'image_data_quality/{Filename}'
            client.upload_file(img_path, Bucket, Key)

if __name__ == '__main__':
    main()