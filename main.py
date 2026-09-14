# -----------------------------------------------------------------------------
# 구역 4: TOP 10 영화 비교 (일관객 합계 vs 최종 누적관객)
# -----------------------------------------------------------------------------
st.header("📌 구역 4: 기간 내 관객 수 TOP 10 영화")

# 기준 선택 옵션 (라디오 버튼)
metric_option = st.radio(
    "집계 기준을 선택하세요:",
    options=["기간 내 일관객 합계", "최종 누적관객 수"],
    horizontal=True
)

# 영화별 데이터 집계
top10_movies_summary = df.groupby('영화명').agg(
    일관객합계=('일관객', 'sum'),
    누적관객수=('누적관객', 'max'),
    진입일수=('날짜', 'nunique')
).reset_index()

# 선택한 기준에 따라 정렬 및 칼럼 지정
if metric_option == "기간 내 일관객 합계":
    target_col = '일관객합계'
    chart_title = "기간 내 일관객 합계 TOP 10 영화"
else:
    target_col = '누적관객수'
    chart_title = "최종 누적관객 수 TOP 10 영화"

# 상위 10개 영화 추출 (가로 막대그래프 상단에 1위가 오도록 오름차순 정렬)
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
