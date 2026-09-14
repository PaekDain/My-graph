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

# 앱 제목 및 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 및 각종 지표 변화를 탐색합니다.")
st.markdown("---")

# 2. 데이터 불러오기 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 YYYYMMDD 형태의 문자열에서 실제 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 형변환
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
st.header("📌 구역 1: 영화별 일관객 변화")

top_movies = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()

selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    options=top_movies,
    index=0
)

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
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 상영 기간 동안 일일 관객 수가 주말과 평일에 어떻게 변동하는지, 그리고 최고 전성기(피크) 이후 흥행 감소 추세를 시각적으로 확인할 수 있습니다.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 구역 2: 추후 추가될 그래프 구역
# -----------------------------------------------------------------------------
st.header("📌 구역 2: 주요 영화 동시 관객 비교 (추가 예정)")
st.caption("※ 향후 기간별 주요 흥행작들의 동시 관객 수 비교 그래프가 들어갈 자리입니다.")

st.info("💡 **이 그래프로 알 수 있는 것:** 특정 시점에 경쟁하는 여러 영화 간의 점유율 변화 및 경쟁 양상을 알 수 있습니다.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 구역 3: 날짜별 TOP 10 총 관객 수 변화 (영역 그래프)
# -----------------------------------------------------------------------------
st.header("📌 구역 3: 날짜별 박스오피스 TOP 10 총 관객 수 추이")

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

st.info("💡 **이 그래프로 알 수 있는 것:** 1년 중 극장가 전체 관객이 가장 몰린 성수기(명절, 연휴, 여름/겨울 방학 등) 날짜와 연중 극장 시장 규모의 변동 패턴을 알 수 있습니다.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 구역 4: TOP 10 영화 비교 (일관객 합계 vs 최종 누적관객)
# -----------------------------------------------------------------------------
st.header("📌 구역 4: 기간 내 관객 수 TOP 10 영화")

metric_option = st.radio(
    "집계 기준을 선택하세요:",
    options=["기간 내 일관객 합계", "최종 누적관객 수"],
    horizontal=True
)

top10_movies_summary = df.groupby('영화명').agg(
    일관객합계=('일관객', 'sum'),
    누적관객수=('누적관객', 'max'),
    진입일수=('날짜', 'nunique')
).reset_index()

if metric_option == "기간 내 일관객 합계":
    target_col = '일관객합계'
    chart_title = "기간 내 일관객 합계 TOP 10 영화"
else:
    target_col = '누적관객수'
    chart_title = "최종 누적관객 수 TOP 10 영화"

top10_movies_summary = top10_movies_summary.nlargest(10, target_col).sort_values(target_col, ascending=True)

fig4 = px.bar(
    top10_movies_summary,
    x=target_col,
    y='영화명',
    orientation='h',
    title=chart_title,
    labels={target_col: f'{metric_option}(명)', '영화명': '영화 제목'},
    text=target_col
)

fig4.update_traces(
    texttemplate='%{text:,.0f}명',
    textposition='outside',
    marker_color='#3498DB' if metric_option == "기간 내 일관객 합계" else '#2ECC71',
    customdata=top10_movies_summary[['진입일수', '일관객합계', '누적관객수']],
    hovertemplate=(
        "<b>영화명:</b> %{y}<br>"
        f"<b>{metric_option}:</b> %{{x:,}}명<br>"
        "<b>일관객 합계:</b> %{customdata[1]:,}명<br>"
        "<b>최종 누적관객:</b> %{customdata[2]:,}명<br>"
        "<b>10위권 진입 일수:</b> %{customdata[0]}일<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title=f"{metric_option} (명)",
    yaxis_title="영화명",
    margin=dict(l=20, r=80, t=50, b=20),
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 해당 데이터 집계 기간 동안 기록한 관객 수와 실제 영화의 전체 누적관객 수를 비교하여, 상영 기간 전체 흥행 규모와 특정 기간 차트인 성과 간의 차이를 분석할 수 있습니다.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 구역 5: 월×요일별 일관객 합계 (히트맵)
# -----------------------------------------------------------------------------
st.header("📌 구역 5: 월×요일별 관객 수 분포")

# 데이터 카피 후 월, 요일 추출
heatmap_df = df.copy()
heatmap_df['월'] = heatmap_df['날짜'].dt.month.astype(str) + "월"
heatmap_df['요일'] = heatmap_df['날짜'].dt.day_name()

# 요일 한글 변환 및 정렬 순서 정의 (월요일 -> 일요일)
day_map = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
heatmap_df['요일'] = heatmap_df['요일'].map(day_map)

days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
months_order = [f"{i}월" for i in range(1, 13)]

# 월 x 요일별 일관객 합계 피벗 테이블 생성
pivot_df = heatmap_df.pivot_table(
    index='월',
    columns='요일',
    values='일관객',
    aggfunc='sum'
).reindex(index=months_order, columns=days_order).fillna(0)

# Plotly 히트맵 생성
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="요일", y="월", color="일관객 합계"),
    x=days_order,
    y=months_order,
    color_continuous_scale="Reds",
    aspect="auto",
    title="월 및 요일별 일관객 합계 히트맵"
)

fig5.update_traces(
    hovertemplate="<b>%{y} %{x}</b><br>일관객 합계: %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    margin=dict(l=20, r=20, t=50, b=20),
    height=500
)

st.plotly_chart(fig5, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 월별/요일별로 극장 관객이 어느 시점에 가장 밀집되는지 패턴을 한눈에 파악할 수 있으며, 성수기 주말과 비수기 평일 간의 관객 수 격차를 직관적으로 확인할 수 있습니다.")
