import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 앱 제목 및 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 및 각종 지표 변화를 탐색합니다.")
st.markdown("---")

# 2. 데이터 불러오기 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 컬럼명이 정확한지 확인 후 정리 (날짜, 순위, 영화코드, 영화명, 일관객, 누적관객, 스크린수, 상영횟수)
    # 날짜 열을 문자열로 변환 후 datetime 객체로 변환 (YYYYMMDD 형식)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 형변환 (혹시 모를 오류 방지)
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 구역 1: 영화별 일관객 변화 (선 그래프)
# -----------------------------------------------------------------------------
st.header("📌 구역 1: 영화별 추이 분석")

# 영화 목록 추출 (관객 수가 많은 순으로 정렬하여 사용자 편의성 제공)
top_movies = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()

selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    options=top_movies,
    index=0
)

# 선택한 영화 데이터 필터링
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    # Plotly 선 그래프 생성
    fig = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"[{selected_movie}] 일별 관객 수 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True,
        hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d', '순위': True, '스크린수': ':,d'}
    )

    # 툴팁 및 레이아웃 커스텀
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위<br><b>스크린수:</b> %{customdata[1]:,}개<extra></extra>",
        line=dict(width=2.5, color="#E50914"), # 네트플릭스 레드 느낌의 포인트 컬러
        marker=dict(size=6)
    )

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객 수 (명)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # 요약 통계 정보 간단히 제공
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("최고 일관객 수", f"{movie_df['일관객'].max():,} 명")
    col2.metric("최대 스크린 수", f"{movie_df['스크린수'].max():,} 개")
    col3.metric("TOP 10 진입 일수", f"{len(movie_df)} 일")
    col4.metric("기간 내 누적 관객 수", f"{movie_df['일관객'].sum():,} 명")
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

# 그래프 해석/인사이트 영역
st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 상영 기간 동안 일일 관객 수가 주말과 평일에 어떻게 변동하는지, 그리고 최고 전성기(피크) 이후 흥행 감소 추세를 시각적으로 확인할 수 있습니다.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 구역 2: 추후 추가될 그래프 구역 (확장성 확보)
# -----------------------------------------------------------------------------
st.header("📌 구역 2: 일별 박스오피스 TOP 5 관객 추이 (예정)")
st.caption("※ 향후 기간별 상위 영화들의 동시 관객 수 비교 그래프가 추가될 예정입니다.")

# 플레이스홀더 / 안내 문구
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 시점에 여러 개봉작들이 경쟁할 때 각 영화의 점유율 및 흥행 전이 양상을 한눈에 파악할 수 있습니다.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 구역 3: 추후 추가될 그래프 구역
# -----------------------------------------------------------------------------
st.header("📌 구역 3: 월별/요일별 관객 패턴 분석 (예정)")
st.caption("※ 향후 요일별/월별 관객 집중도 분석 그래프가 추가될 예정입니다.")

st.info("💡 **이 그래프로 알 수 있는 것:** 극장가 성수기와 비성수기 패턴, 그리고 주말 효과(금~일 관객 급증)의 비중을 알 수 있습니다.")
