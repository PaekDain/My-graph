# -----------------------------------------------------------------------------
# 구역 4: 기간 내 합계 관객 수 TOP 10 영화 (가로 막대그래프)
# -----------------------------------------------------------------------------
st.header("📌 구역 4: 기간 내 관객 수 TOP 10 영화")

# 1. 영화별 합계 관객 수 및 10위권 진입 일수 집계
top10_movies_summary = df.groupby('영화명').agg(
    총관객수=('일관객', 'sum'),
    진입일수=('날짜', 'nunique')
).reset_index()

# 2. 관객 수 기준 상위 10개 영화 추출 (가로 막대 상단에 1위가 오도록 오름차순 정렬)
top10_movies_summary = top10_movies_summary.nlargest(10, '총관객수').sort_values('총관객수', ascending=True)

# 3. 가로 막대그래프 생성 (orientation='h')
fig4 = px.bar(
    top10_movies_summary,
    x='총관객수',
    y='영화명',
    orientation='h',
    title="기간 내 관객 수 TOP 10 영화",
    labels={'총관객수': '합계 관객 수(명)', '영화명': '영화 제목'},
    text='총관객수'
)

# 4. 막대 위 관객 수 표기 및 마우스 오버(툴팁) 설정
fig4.update_traces(
    texttemplate='%{text:,.0f}명',
    textposition='outside',
    marker_color='#3498DB',
    customdata=top10_movies_summary[['진입일수']],
    hovertemplate="<b>영화명:</b> %{y}<br><b>합계 관객수:</b> %{x:,}명<br><b>10위권 진입 일수:</b> %{customdata[0]}일<extra></extra>"
)

fig4.update_layout(
    xaxis_title="기간 내 합계 관객 수 (명)",
    yaxis_title="영화명",
    margin=dict(l=20, r=80, t=50, b=20),
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

# 5. 인사이트 문구
st.info("💡 **이 그래프로 알 수 있는 것:** 1년 동안 박스오피스 TOP 10에 차트인한 전체 관객 수 상위 10개 영화의 흥행 규모와, 10위권에 머무른 일수(흥행 지속력)를 함께 비교해 볼 수 있습니다.")
