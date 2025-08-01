import streamlit as st
import pandas as pd

st.title("代表選手 検索システム")

# 団体を選択
org = st.selectbox("団体を選んでください", ["JKJO", "リアルチャンピオンシップ"])

# ファイル読み込み
if org == "JKJO":
    df = pd.read_csv("jkjo_list.csv")
elif org == "リアルチャンピオンシップ":
    df = pd.read_csv("real_2025kenri.csv")

# 👇 名前列の全角スペース削除＋前後の空白除去
df["名前"] = df["名前"].astype(str).str.replace("　", "").str.strip()

# 検索条件：名前（部分一致）
name = st.text_input("選手名で検索（部分一致）")

# 検索条件：学年（ユニーク値から選択）
if "学年" in df.columns:
    grades = df["学年"].dropna().unique().tolist()
    selected_grade = st.selectbox("学年を選択", ["すべて"] + sorted(grades))
else:
    selected_grade = "すべて"

# 検索条件：性別
genders = df["性別"].dropna().unique().tolist() if "性別" in df.columns else []
selected_gender = st.selectbox("性別を選択", ["すべて"] + genders)

# フィルタリング
if name:
    df = df[df["名前"].astype(str).str.contains(name)]

if selected_grade != "すべて":
    df = df[df["学年"] == selected_grade]

if selected_gender != "すべて":
    df = df[df["性別"] == selected_gender]

# 結果表示
st.subheader("検索結果")
st.write(f"{len(df)} 件ヒット")
st.dataframe(df.reset_index(drop=True))
