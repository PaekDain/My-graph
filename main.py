import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # 구역 3에서 go.Scatter를 쓸 때 필수!


# -----------------------------------------------------------------------------
# 구역 3: 날짜별 TOP 10 총 관객 수 변화 (영역 그래프)
# -----------------------------------------------------------------------------
st.header("📌 구역 3: 날짜별 박스오피스 TOP 10 총 관객 수 추이")

# 1. 날짜별 10위권 관객 수 합계 계산
daily_total = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')

# 2. 관객 수 합계가 가장 컸던 상위 3일 추출
top3_days = daily_total.nlargest(3, '일관객').sort_values('날짜')

# 3. 영역 그래프 생성 (px.area)
fig3 = px.area(
    daily_total,
    x='날짜',
    y='일관객',
    title="일별 박스오피스 TOP 10 영화 관객 수 총합",
    labels={'날짜': '날짜', '일관객': 'TOP 10 총 관객 수(명)'}
)

# 기본 영역 스타일 커스텀
fig3.update_traces(
    line_color='#2E86C1',
    fillcolor='rgba(46, 134, 193, 0.3)',
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>TOP 10 총 관객수:</b> %{y:,}명<extra></extra>"
)

# 4. 상위 3일 최고점에 별 모양 마커 및 날짜/관객수 라벨 표기
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

# 5. 상위 3일 요약 메트릭 표시
st.subheader("🔥 관객 수가 가장 많았던 Top 3 날짜")
cols = st.columns(3)
for idx, (_, row) in enumerate(top3_days.sort_values('일관객', ascending=False).iterrows()):
    cols[idx].metric(
        label=f"{idx+1}위: {row['날짜'].strftime('%Y-%m-%d')}",
        value=f"{row['일관객']:,} 명"
    )

# 6. 인사이트 문구
st.info("💡 **이 그래프로 알 수 있는 것:** 1년 중 극장가 전체 관객이 가장 몰린 최고 성수기(명절, 연휴, 방학 시즌 등) 날짜와 연중 극장 시장의 전체적인 규모 변동 패턴을 알 수 있습니다.")
