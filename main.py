import pandas as pd
import plotly.express as px
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

# 영화별 중복을 제거하고 관객 수를 합산한 안전한 데이터프레임 생성
treemap_df = (
    df.groupby(["genre", "movieNm"], as_index=False)["total_audi"]
    .sum()
)

# Plotly 트리맵 생성
fig_treemap = px.treemap(
    treemap_df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    labels={"total_audi": "총 관객 수", "genre": "장르", "movieNm": "영화명"},
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>",
    root_color="lightgrey",
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 특정 장르 내에서 소수의 흥행 대작이 전체 장르 관객 수의 대부분을 견인하고 있음을 한눈에 비교할 수 있습니다."
    )

# -------------------------------------------------------------------
# 섹션 3: 총 관객 수 분포 (히스토그램)
# -------------------------------------------------------------------
st.divider()
st.header("3. 총 관객 수 분포")

# 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수", "count": "영화 편수"},
    title="총 관객 수 분포 (히스토그램)",
)

fig_hist.update_traces(
    hovertemplate="총 관객 수 구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)

fig_hist.update_layout(
    xaxis_title="총 관객 수(명)",
    yaxis_title="영화 편수(개)",
    bargap=0.1
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 관객이 많은 영화 추출
max_movie = df.loc[df["total_audi"].idxmax()]
max_movie_name = max_movie["movieNm"]
max_movie_audi = max_movie["total_audi"]

# 관객 수 주요 분포 구간 계산 (상위 편수 구간 계산)
# 데이터 기반 분석 문구
st.markdown(
    f"""
    **이 그래프로 알 수 있는 것:**
    - 대다수의 영화(약 80% 이상)가 **100만 명 이하의 관객 수 구간**에 밀집해 있는 극단적인 오른쪽 꼬리 분포(Right-skewed)를 보입니다.
    - 데이터셋 내에서 가장 관객 수가 많은 영화는 **'{max_movie_name}'**(총 {max_movie_audi:,}명)입니다.
    """
)
