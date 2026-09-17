import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 TOP 10에 진입한 주요 영화 216편 데이터 분석")


# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 분리되어 있을 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].fillna("기타").astype(str)
    df["genre"] = df["genre"].apply(lambda x: x.split("|")[0].strip())

    return df


# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ----------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# ----------------------------------------------------
st.divider()
st.subheader("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 분포",
)

# 호버 마우스 오버 시 편수(value)와 비율(percent) 표시 설정
fig.update_traces(
    textinfo="percent+label", hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 그래프 해석/알 수 있는 점 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 특정 주요 장르가 전체 상위권 영화 중 가장 큰 비중을 차지하고 있음을 알 수 있습니다."
)
