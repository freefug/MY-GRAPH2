import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)


# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르(genre) 컬럼 전처리: '|' 기호로 연결된 여러 장르 중 첫 번째 장르만 추출
    df["genre"] = (
        df["genre"].fillna("기타").astype(str).apply(lambda x: x.split("|")[0].strip())
    )

    return df


# 앱 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 데이터 불러오기
data = load_data()

# ---------------------------------------------------------
# 첫 번째 그래프 구역: 장르별 영화 편수 (Plotly 도넛 차트)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 비율")

# 장르별 영화 수 집계
genre_counts = data["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,  # 도넛 형태
    title="장르별 영화 분포",
)

# 호버 툴팁 및 표시 레이블 설정 (장르, 편수, 비율 표시)
fig.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>영화 수: %{value}편<br>비율: %{percent}<extra></extra>",
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 그래프 하단 설명 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "특정 기간 박스오피스 상위권 영화 중 어떤 장르의 영화가 가장 높은 비중을 차지하고 있는지 한눈에 확인할 수 있습니다."
)

st.markdown("---")
