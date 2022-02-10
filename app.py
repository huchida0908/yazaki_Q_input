import streamlit as st
import pandas as pd
import numpy as np

st.title('工程能力管理')

kanri = st.radio(
     "初物管理",
     ('初物', '終物', 'その他'))

number = st.number_input('加工済みロット数', step=1)
st.write('加工数 ：', number*25 )

code = st.text_input('code')
st.write('入力対象コード ：', code)

result = st.number_input('被覆剥取長[mm]')
st.write('被覆剥取長 ：', result )

if st.button('登録'):
     st.write(f'{code}の{kanri}実績値を登録しました。')
