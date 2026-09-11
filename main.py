import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 및 각종 지표 변화를 탐색합니다.")
st.markdown("---")

# 2. 데이터 불러오기 함수 정의
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df_raw = pd.read_csv(url)
    
    # 날짜 변환 및 수치형 변환
    df_raw['날짜'] = pd.to_datetime(df_raw['날짜'].astype(str), format='%Y%m%d')
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df_raw.columns:
            df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')
            
    return df_raw

# 3. 데이터 로드 (핵심: 함수 호출 결과를 전역 변수 'df'에 할당해야 합니다!)
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 구역 1: 영화별 일관객 변화
# -----------------------------------------------------------------------------
st.header("📌 구역 1: 영화별 일관객 변화")

top_movies = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("조회할 영화를 선택하세요:", options=top_movies, index=0)

movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"[{selected_movie}] 날짜별 일관객 수 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True,
        hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d', '순위': True, '스크린수': ':,d'}
    )

    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위<br><b>스크린수:</b> %{customdata[1]:,}개<extra></extra>",
        line=dict(width=2.5, color="#E50914"),
        marker=dict(size=6)
    )

    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객 수 (명)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("최고 일관객 수", f"{movie_df['일관객'].max():,} 명")
    col2.metric("최대 스크린 수", f"{movie_df['스크린수'].max():,} 개")
    col3.metric("TOP 10 진입 일수", f"{len(movie_df)} 일")
    col4.metric("기간 내 누적 관객 수", f"{movie_df['일관객'].sum():,} 명")

st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 상영 기간 동안 일일 관객 수가 주말과 평일에 어떻게 변동하는지, 그리고 최고 전성기(피크) 이후 흥행 감소 추세를 시각적으로 확인할 수 있습니다.")

st.markdown("---")


# -----------------------------------------------------------------------------
# 구역 2: 추후 추가용 구역
# -----------------------------------------------------------------------------
st.header("📌 구역 2: 주요 영화 동시 관객 비교 (추가 예정)")
st.caption("※ 향후 기간별 주요 흥행작들의 동시 관객 수 비교 그래프가 들어갈 자리입니다.")

st.info("💡 **이 그래프로 알 수 있는 것:** 특정 시점에 경쟁하는 여러 영화 간의 점유율 변화 및 경쟁 양상을 알 수 있습니다.")

st.markdown("---")


# -----------------------------------------------------------------------------
# 구역 3: 날짜별 TOP 10 총 관객 수 추이 (영역 그래프)
# -----------------------------------------------------------------------------
st.header("📌 구역 3: 날짜별 박스오피스 TOP 10 총 관객 수 추이")

# 'df' 변수가 정상 작동하도록 함
daily_total = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')
top3_days = daily_total.nlargest(3, '일관객').sort_values('날짜')

fig3 = px.area(
    daily_total,
    x='날짜',
    y='일관객',
    title="일별 박스오피스 TOP 10 영화 관객 수 총합",
    labels={'날짜': '날짜', '일관객': 'TOP 10 총 관객 수(명)'}
)

fig3.update_traces(
    line_color='#2E86C1',
    fillcolor='rgba(46, 134, 193, 0.3)',
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>TOP 10 총 관객수:</b> %{y:,}명<extra></extra>"
)

fig3.add_trace(
    go.Scatter(
        x=top3_days['날짜'],
        y=top3_days['일관객'],
        mode='markers+text',
        name='최대 관객 3일',
        text=[f"🏆 {d.strftime('%Y-%m-%d')}<br>({v:,.0f}명)" for d, v in zip(top3_days['날짜'], top3_days['일관객'])],
        textposition="top center",
        marker=dict(size=12, color='#E74C3C', symbol='star'),
        hoverinfo='skip'
    )
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="TOP 10 일관객 합계 (명)",
    hovermode="x unified",
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=20),
    height=500
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("🔥 관객 수가 가장 많았던 Top 3 날짜")
cols = st.columns(3)
for idx, (_, row) in enumerate(top3_days.sort_values('일관객', ascending=False).iterrows()):
    cols[idx].metric(
        label=f"{idx+1}위: {row['날짜'].strftime('%Y-%m-%d')}",
        value=f"{row['일관객']:,} 명"
    )

st.info("💡 **이 그래프로 알 수 있는 것:** 1년 중 극장가 전체 관객이 가장 몰린 최고 성수기(명절, 연휴, 방학 시즌 등) 날짜와 연중 극장 시장의 전체적인 규모 변동 패턴을 알 수 있습니다.")
