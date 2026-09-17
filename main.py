import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 분리 후 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).str.split("|").str[0]

    return df


df = load_data()

# -------------------------------------------------------------------
# 섹션 1: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.divider()
st.header("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig_genre = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    hover_data=["count"],
    labels={"count": "영화 편수", "genre": "장르"},
)

fig_genre.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig_genre, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 특정 주요 장르(예: 드라마, 액션 등)가 전체 개봉 영화의 과반수 이상을 차지하는 비대칭적 분포를 확인할 수 있습니다."
    )

# -------------------------------------------------------------------
# 섹션 2: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.divider()
st.header("2. 장르 및 영화별 총 관객 수 분포")

# 트리맵용 계층 구조 데이터 생성 (graph_objects 방식)
labels = ["전체"]
parents = [""]
values = [df["total_audi"].sum()]
custom_labels = ["전체"]

# 1계층: 장르
genre_grouped = df.groupby("genre")["total_audi"].sum().reset_index()
for _, row in genre_grouped.iterrows():
    labels.append(row["genre"])
    parents.append("전체")
    values.append(row["total_audi"])
    custom_labels.append(row["genre"])

# 2계층: 영화
for _, row in df.iterrows():
    # 고유 ID로 movieCd 사용
    labels.append(str(row["movieCd"]))
    parents.append(row["genre"])
    values.append(row["total_audi"])
    # 툴팁 및 표시용 실제 영화명
    custom_labels.append(row["movieNm"])

# go.Treemap으로 안전한 생성
fig_treemap = go.Figure(
    go.Treemap(
        ids=labels,
        labels=custom_labels,
        parents=parents,
        values=values,
        branchvalues="totalroot",
        hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>",
    )
)

fig_treemap.update_layout(margin=dict(t=10, l=10, r=10, b=10))

st.plotly_chart(fig_treemap, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 특정 장르 내에서 소수의 흥행 대작이 전체 장르 관객 수의 대부분을 견인하고 있음을 한눈에 비교할 수 있습니다."
    )
