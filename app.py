import streamlit as st
import pandas as pd
import unicodedata

st.title("代表選手 検索システム")

# 異体字などを正規化＋置換する関数
def clean_name(text):
    if pd.isna(text):
        return ""
    return unicodedata.normalize("NFKC", str(text))\
        .replace("﨑", "崎")\
        .replace("髙", "高")\
        .replace("齋", "斉")\
        .replace("　", "")\
        .strip()

# 団体を選択
org = st.selectbox("団体を選んでください", ["JKJO", "リアルチャンピオンシップ"])

# ファイル読み込み
if org == "JKJO":
    df = pd.read_csv("jkjo_list.csv")
elif org == "リアルチャンピオンシップ":
    df = pd.read_csv("real_2025kenri.csv")

# 名前列をクリーン化
df["名前"] = df["名前"].map(clean_name)

# 検索条件：名前（部分一致）
name = st.text_input("選手名で検索（部分一致）")
name = clean_name(name)  # ユーザー入力もクリーン化

# 検索条件：学年
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
    df = df[df["名前"].str.contains(name, case=False, na=False)]

if selected_grade != "すべて":
    df = df[df["学年"] == selected_grade]

if selected_gender != "すべて":
    df = df[df["性別"] == selected_gender]

# 道場検索
dojo = st.text_input("道場名で検索（部分一致）")
dojo = clean_name(dojo)

# フィルタリング：道場
if dojo:
    df = df[df["所属道場"].astype(str).map(clean_name).str.contains(dojo, case=False, na=False)]

# UI
tournaments = df["獲得大会"].dropna().unique().tolist()
selected_tournament = st.selectbox("獲得大会を選択", ["すべて"] + sorted(tournaments))

# 絞り込み
if selected_tournament != "すべて":
    df = df[df["獲得大会"] == selected_tournament]


# 結果表示
st.subheader("検索結果")
st.write(f"{len(df)} 件ヒット")
st.dataframe(df.reset_index(drop=True))
