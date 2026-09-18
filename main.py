import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

    # 개봉일 전처리 및 월(Month) 추출
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_month"] = df["release_date"].dt.month

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

# 데이터 기반 분석 문구
with st.container():
    st.info(
        f"**이 그래프로 알 수 있는 것:** 대다수의 영화(약 80% 이상)가 **100만 명 이하의 관객 수 구간**에 밀집해 있는 극단적인 오른쪽 꼬리 분포(Right-skewed)를 보입니다. "
        f"가장 관객 수가 많은 영화는 **'{max_movie_name}'**(총 {max_movie_audi:,}명)입니다."
    )

# -------------------------------------------------------------------
# 섹션 4: 개봉일 스크린 수와 총 관객 수의 관계 (산점도)
# -------------------------------------------------------------------
st.divider()
st.header("4. 개봉일 스크린 수 vs 총 관객 수 관계")

# 산점도 생성 (장르별 색상 구분, 마우스 오버 시 영화명 노출)
fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,d",
        "total_audi": ":,d",
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르",
        "movieNm": "영화명"
    },
    title="개봉일 스크린 수에 따른 총 관객 수 분포"
)

fig_scatter.update_traces(marker=dict(size=9, opacity=0.8))
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린 수(개)",
    yaxis_title="총 관객 수(명)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 개봉일 스크린 수가 많을수록 총 관객 수가 증가하는 명확한 양(+)의 상관관계를 보이지만, 일부 영화는 적은 스크린 수에도 불구하고 입소문을 통해 높은 총 관객 수를 기록하는 등 예외적인 사례도 존재합니다."
    )

# -------------------------------------------------------------------
# 섹션 5: 주요 장르별 총 관객 수 분포 (박스플롯)
# -------------------------------------------------------------------
st.divider()
st.header("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 영화 편수가 10편 이상인 장르 필터링
genre_counts_all = df["genre"].value_counts()
major_genres = genre_counts_all[genre_counts_all >= 10].index
df_major_genres = df[df["genre"].isin(major_genres)]

# 박스플롯 생성
fig_box = px.box(
    df_major_genres,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",  # 이상치 점 표시
    hover_name="movieNm",
    hover_data={
        "total_audi": ":,d",
        "genre": True
    },
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수",
        "movieNm": "영화명"
    },
    title="주요 장르별 총 관객 수 분포 및 이상치"
)

fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수(명)",
    showlegend=False
)

st.plotly_chart(fig_box, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 대부분 장르의 중앙값(Median) 관객 수는 낮은 편이지만, 상단에 위치한 이상치(Outlier) 점들을 통해 해당 장르의 메가 히트 흥행작들을 한눈에 식별할 수 있습니다."
    )

# -------------------------------------------------------------------
# 섹션 6: 스크린 수 vs 총 관객 수 vs 첫 주 관객 수 (버블 차트)
# -------------------------------------------------------------------
st.divider()
st.header("6. 스크린 수 vs 총 관객 수 vs 첫 주 관객 수 (버블 차트)")

# 버블 차트 생성 (점 크기: 개봉 첫 주 관객 수)
fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,d",
        "total_audi": ":,d",
        "first_week_audi": ":,d",
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "개봉 첫 주 관객 수",
        "genre": "장르",
        "movieNm": "영화명"
    },
    size_max=50,
    title="스크린 수와 총 관객 수 및 첫 주 관객 수(버블 크기) 관계"
)

fig_bubble.update_traces(marker=dict(opacity=0.7, sizemode="area"))
fig_bubble.update_layout(
    xaxis_title="개봉일 스크린 수(개)",
    yaxis_title="총 관객 수(명)"
)

st.plotly_chart(fig_bubble, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 원의 크기(첫 주 관객 수)가 큰 영화일수록 최종 총 관객 수(Y축)도 높게 형성되는 경향을 보여, 초반 흥행 성공(초반 관객 동원력)이 최종 총 관객 수 결정에 핵심적인 역할을 함을 알 수 있습니다."
    )

# -------------------------------------------------------------------
# 섹션 7: 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# -------------------------------------------------------------------
st.divider()
st.header("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

# 국가-장르별 영화 편수 집계
nation_genre_df = (
    df.groupby(["nation", "genre"]).size().reset_index(name="count")
)

# 선버스트 차트 생성
fig_sunburst = px.sunburst(
    nation_genre_df,
    path=["nation", "genre"],
    values="count",
    title="제작 국가 → 장르 계층 구조별 영화 편수",
    labels={"nation": "제작 국가", "genre": "장르", "count": "영화 편수"},
)

fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 각 제작 국가별로 주력 생산하는 주요 장르 비중의 차이를 계층 구조로 직관적 비교가 가능하며, 국가별 장르 다양성 양상을 한눈에 파악할 수 있습니다."
    )

# -------------------------------------------------------------------
# 섹션 8: 10위권 유지 일수 vs 총 관객 수 (산점도)
# -------------------------------------------------------------------
st.divider()
st.header("8. 10위권에 오래 머문 영화는 총 관객도 많은가")

# 10위권 유지 일수 vs 총 관객 수 산점도 생성
fig_top10_scatter = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "days_in_top10": ":,d",
        "total_audi": ":,d",
        "genre": True
    },
    labels={
        "days_in_top10": "10위권 유지 일수(일)",
        "total_audi": "총 관객 수(명)",
        "genre": "장르",
        "movieNm": "영화명"
    },
    title="10위권에 오래 머문 영화는 총 관객도 많은가"
)

fig_top10_scatter.update_traces(marker=dict(size=9, opacity=0.8))
fig_top10_scatter.update_layout(
    xaxis_title="10위권 유지 일수(일)",
    yaxis_title="총 관객 수(명)"
)

st.plotly_chart(fig_top10_scatter, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 10위권 내에 오랫동안 차트에 머무른 영화일수록 최종 총 관객 수도 높게 형성되는 강한 양(+)의 상관관계를 확인할 수 있습니다. 롱런 흥행(장기 상영) 여부가 관객 동원력의 주요 지표임을 보여줍니다."
    )

# -------------------------------------------------------------------
# 섹션 9: 월별 개봉 영화 편수 및 평균 관객 수 (이중 축 복합 차트)
# -------------------------------------------------------------------
st.divider()
st.header("9. 월별 개봉 영화 편수 및 평균 관객 수 (월별 계절성)")

# 월별 집계 데이터 생성 (1~12월)
monthly_df = (
    df.dropna(subset=["release_month"])
    .groupby("release_month")
    .agg(
        movie_count=("movieNm", "count"),
        avg_audi=("total_audi", "mean")
    )
    .reset_index()
)
monthly_df["release_month_str"] = monthly_df["release_month"].astype(int).astype(str) + "월"

# 보조 축(Secondary Y-axis)을 포함하는 Subplot 생성
fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])

# 1. 막대 차트: 개봉 영화 편수
fig_monthly.add_trace(
    go.Bar(
        x=monthly_df["release_month_str"],
        y=monthly_df["movie_count"],
        name="개봉 영화 편수",
        opacity=0.7,
        hovertemplate="<b>%{x}</b><br>개봉 편수: %{y}편<extra></extra>",
    ),
    secondary_y=False,
)

# 2. 선 차트: 평균 관객 수
fig_monthly.add_trace(
    go.Scatter(
        x=monthly_df["release_month_str"],
        y=monthly_df["avg_audi"],
        name="평균 관객 수",
        mode="lines+markers",
        line=dict(width=3, color="crimson"),
        marker=dict(size=8),
        hovertemplate="<b>%{x}</b><br>평균 관객 수: %{y:,.0f}명<extra></extra>",
    ),
    secondary_y=True,
)

fig_monthly.update_layout(
    title="월별 개봉 영화 편수(막대) 및 평균 관객 수(선)",
    xaxis_title="개봉 월",
    legend=dict(x=0.01, y=0.99),
)

fig_monthly.update_yaxes(title_text="개봉 영화 편수(개)", secondary_y=False)
fig_monthly.update_yaxes(title_text="평균 관객 수(명)", secondary_y=True)

st.plotly_chart(fig_monthly, use_container_width=True)

# 시각화 해석 구역
with st.container():
    st.info(
        "**이 그래프로 알 수 있는 것:** 개봉 영화 편수가 많은 달(공급)과 실제 영화 1편당 평균 관객 수가 높은 달(수요/성수기) 간의 차이를 확인할 수 있습니다. 여름 방학(7~8월)이나 겨울/연말 시즌(12~1월)에 평균 관객 수가 높아지는 계절적 흥행 특성을 파악할 수 있습니다."
    )
