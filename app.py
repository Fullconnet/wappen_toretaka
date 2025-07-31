
import streamlit as st
import pandas as pd

# データ読み込み
df = pd.read_csv("jkjo_list.csv")

st.title("JKJO代表選手検索システム")

# 検索条件
name = st.text_input("名前で検索")
dojo = st.selectbox("所属道場で絞り込み", ["すべて"] + sorted(df["所属道場"].dropna().unique()))
grade = st.selectbox("階級（学年）で絞り込み", ["すべて"] + sorted(df["階級（学年）"].dropna().unique()))

# フィルタ適用
if name:
    df = df[df["名前"].str.contains(name)]
if dojo != "すべて":
    df = df[df["所属道場"] == dojo]
if grade != "すべて":
    df = df[df["階級（学年）"] == grade]

# 結果表示
st.dataframe(df)
