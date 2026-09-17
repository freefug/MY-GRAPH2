import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 앱 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 데이터 전처리: .str 접근자를 사용해 안전하게 분리 및 공백 제거
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # 트리맵 중복 에러 방지: 동명 영화 구분용 고유 레이블 생성 (예: "영화명 (영화코드)")
    # movieCd가 없는 경우에 대비해 행 번호(index) 기반 식별자 적용
    df["movie_id"] = df["movieNm"] + " (" + df.index.astype(str) + ")"

    return df


df = load_data()

# ==========================================
# 1. 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스 오버 시 편수와 비율이 함께 표시되도록 설정
fig_donut.update_traces(
    hoverinfo="label+value+percent", textinfo="percent+label"
)

# 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("여기에 그래프 해석 및 분석 인사이트 한 문장을 입력하세요.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 2. 두 번째 그래프: 장르별/영화별 총 관객 수 (트리맵)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

# Plotly 트리맵 생성 (고유한 movie_id를 path로 사용하여 중복 에러 방지)
fig_treemap = px.treemap(
    df,
    path=["genre", "movie_id"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 트리맵",
    custom_data=["movieNm", "total_audi"],
)

# 마우스 오버 시 순수 영화명과 총 관객 수만 표시되도록 툴팁 설정
fig_treemap.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br><b>총 관객 수:</b> %{customdata[1]:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("여기에 그래프 해석 및 분석 인사이트 한 문장을 입력하세요.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 3. 세 번째 그래프: 총 관객 수 분포 (히스토그램)
# ==========================================
st.subheader("3. 총 관객 수 분포 히스토그램")

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={"total_audi": "총 관객 수(명)"},
)

fig_hist.update_layout(
    yaxis_title="영화 수(편)",
    bargap=0.1
)

# 그래프 출력
st.plotly_chart(fig_hist, use_container_width=True)

# 데이터 수식 계산 (가장 많은 관객 수 영화 & 분포 구간 정보)
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# 관객 수 200만 명 미만 비율 계산
under_2m_pct = (df["total_audi"] < 2000000).mean() * 100

# 구분선 및 동적 분석 문구 출력 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화(약 {under_2m_pct:.1f}%)가 관객 수 200만 명 이하 구간에 다수 집중되어 있으며, "
    f"가장 관객 수가 많은 영화는 **'{top_movie_name}'** ({top_movie_audi:,}명)입니다."
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 4. 네 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (산점도)
# ==========================================
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계")

# Plotly 산점도 생성
fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객 수",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객 수(명)",
        "genre": "장르",
    },
    custom_data=["movieNm", "genre", "first_scrn", "total_audi"],
)

# 마우스 오버(Hover) 툴팁 설정
fig_scatter.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "장르: %{customdata[1]}<br>"
        "개봉일 스크린수: %{customdata[2]:,}개<br>"
        "총 관객 수: %{customdata[3]:,}명<extra></extra>"
    )
)

# 그래프 출력
st.plotly_chart(fig_scatter, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보입니다.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 5. 다섯 번째 그래프: 주요 장르별 총 관객 수 상자 그림 (박스플롯)
# ==========================================
st.subheader("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 영화 편수가 10편 이상인 장르 필터링
genre_counts_series = df["genre"].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_top_genres = df[df["genre"].isin(top_genres)]

# Plotly 박스플롯 생성
fig_box = px.box(
    df_top_genres,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",  # 이상치 점을 명확히 표시
    title="영화 수 10편 이상 장르별 총 관객 수 상자 그림",
    labels={"genre": "장르", "total_audi": "총 관객 수(명)"},
    custom_data=["movieNm", "genre", "total_audi"],
)

# 마우스 오버 툴팁 설정 (상자 밖 이상치 점에 마우스 올릴 시 영화명 표시)
fig_box.update_traces(
    hovertemplate=(
        "<b>영화명:</b> %{customdata[0]}<br>"
        "<b>장르:</b> %{customdata[1]}<br>"
        "<b>총 관객 수:</b> %{customdata[2]:,}명<extra></extra>"
    )
)

# 그래프 출력
st.plotly_chart(fig_box, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("장르별로 총 관객 수의 중간값과 분포 범위가 크게 다르며, 상자 밖의 극단적인 흥행 성공작(이상치)이 다수 존재함을 알 수 있습니다.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 6. 여섯 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (버블 차트 - 크기: 첫 주 관객 수)
# ==========================================
st.subheader("6. 개봉일 스크린수, 첫 주 관객 수, 총 관객 수의 관계 (버블 차트)")

# Plotly 버블 차트 생성 (size=first_week_audi)
fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,  # 원의 최대 크기 조절
    title="개봉일 스크린수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객 수(명)",
        "first_week_audi": "개봉 첫 주 관객 수(명)",
        "genre": "장르",
    },
    custom_data=["movieNm", "genre", "first_scrn", "total_audi", "first_week_audi"],
)

# 마우스 오버(Hover) 툴팁 설정
fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "장르: %{customdata[1]}<br>"
        "개봉일 스크린수: %{customdata[2]:,}개<br>"
        "개봉 첫 주 관객 수: %{customdata[4]:,}명<br>"
        "총 관객 수: %{customdata[3]:,}명<extra></extra>"
    )
)

# 그래프 출력
st.plotly_chart(fig_bubble, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수가 많을수록 개봉 첫 주 관객 수(버블 크기)가 크며, 이는 최종 총 관객 수로도 직결되는 경향을 명확히 보여줍니다.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 7. 일곱 번째 그래프: 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ==========================================
st.subheader("7. 제작 국가 및 장르별 영화 편수 계층 구조")

# 국가 및 장르별 영화 편수 계산을 위한 열 생성
df["movie_count"] = 1

# Plotly 선버스트 차트 생성 (계층: 제작 국가 -> 장르, 크기: 영화 편수)
fig_sunburst = px.sunburst(
    df,
    path=["nation", "genre"],
    values="movie_count",
    title="제작 국가 및 장르별 영화 편수 선버스트 차트",
    labels={"nation": "제작 국가", "genre": "장르", "movie_count": "영화 편수"},
)

# 마우스 오버 툴팁 설정
fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig_sunburst, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("제작 국가별로 주력 제작 장르의 구성 비중이 어떻게 다른지 한눈에 파악할 수 있습니다.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 8. 여덟 번째 그래프: 10위권에 오래 머문 영화는 총 관객도 많은가 (산점도)
# ==========================================
st.subheader("8. 10위권 머문 날수와 총 관객 수의 관계")

# Plotly 산점도 생성
fig_days_audi = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "10위권에 머문 날수(일)",
        "total_audi": "총 관객 수(명)",
        "genre": "장르",
    },
    custom_data=["movieNm", "genre", "days_in_top10", "total_audi"],
)

# 마우스 오버(Hover) 툴팁 설정 (영화명, 머문 날수, 총 관객 수 표시)
fig_days_audi.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "장르: %{customdata[1]}<br>"
        "10위권 머문 날수: %{customdata[2]}일<br>"
        "총 관객 수: %{customdata[3]:,}명<extra></extra>"
    )
)

# 그래프 출력
st.plotly_chart(fig_days_audi, use_container_width=True)

# 구분선 및 인사이트 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("10위권에 오래 머문 날수가 길수록 대체로 총 관객 수도 증가하며, 흥행 차트에서의 장기 집권이 최종 관객 수 확보에 강한 긍정적 영향을 미침을 알 수 있습니다.")
