import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':  # macOS
    rc('font', family='AppleGothic')
else:
    print("Not supported OS")

plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
file_path = 'cafe.xlsx'  # 사용자 파일 경로에 맞게 수정 필요
cafe_data = pd.read_excel(file_path)

# order_date를 datetime 형식으로 변환
cafe_data['order_date'] = pd.to_datetime(cafe_data['order_date'])

# 연도와 월 컬럼 추가
cafe_data['year'] = cafe_data['order_date'].dt.year
cafe_data['month'] = cafe_data['order_date'].dt.month

# Streamlit 대시보드 설정
st.title('카페 매출 대시보드')

# 사이드바에서 연도와 제품 선택
selected_year = st.sidebar.selectbox('연도 선택', sorted(cafe_data['year'].unique()))
selected_product = st.sidebar.selectbox('제품 선택', sorted(cafe_data['item'].unique()))

# 선택된 연도와 제품에 따라 데이터 필터링
filtered_data = cafe_data[(cafe_data['year'] == selected_year) & 
                          (cafe_data['item'] == selected_product)]

# 월별 매출 데이터 계산
monthly_sales = filtered_data.groupby('month')['price'].sum().reset_index()

# 주요 지표 계산
total_sales = filtered_data['price'].sum()
average_sales_per_month = filtered_data.groupby('month')['price'].sum().mean()
total_orders = filtered_data.shape[0]

# 주요 지표 출력
st.write('### 주요 지표')
col1, col2, col3 = st.columns(3)
col1.metric("총 매출", f"{total_sales:,.0f} 원")
col2.metric("평균 월 매출", f"{average_sales_per_month:,.0f} 원")
col3.metric("총 주문 수", total_orders)

# 2열로 차트를 배치하고 각 셀 크기 키움
col1, col2 = st.columns([2, 2], gap="large")  # 각 셀의 크기를 키움

# 첫 번째 차트: 월별 매출 막대 차트
with col1:
    st.write(f'### {selected_year}년 {selected_product} 월별 매출')
    fig1, ax1 = plt.subplots(figsize=(10, 5))  # 크기를 키움
    ax1.bar(monthly_sales['month'], monthly_sales['price'])
    ax1.set_xlabel('월')
    ax1.set_ylabel('매출 (원)')
    ax1.set_title(f'{selected_year}년 {selected_product} 월별 매출', fontsize=12)  # 제목 폰트 크기 조정
    st.pyplot(fig1, use_container_width=True)  # 컨테이너 너비 사용

# 두 번째 차트: 월별 매출 추이 선 차트
with col2:
    st.write(f'### {selected_year}년 {selected_product} 월별 매출 추이')
    fig2, ax2 = plt.subplots(figsize=(10, 5))  # 크기를 키움
    ax2.plot(monthly_sales['month'], monthly_sales['price'], marker='o', linestyle='-')
    ax2.set_xlabel('월')
    ax2.set_ylabel('매출 (원)')
    ax2.set_title(f'{selected_year}년 {selected_product} 월별 매출 추이', fontsize=12)  # 제목 폰트 크기 조정
    st.pyplot(fig2, use_container_width=True)  # 컨테이너 너비 사용

# 세 번째 차트와 네 번째 차트도 각 셀의 크기 키움
st.write("")  # 빈 줄 추가하여 차트 간 간격 조정
col3, col4 = st.columns([2, 2], gap="large")  # 각 셀의 크기를 키움

# 세 번째 차트: 전체 카테고리 월별 매출 비교 (Streamlit 기본 바 차트)
with col3:
    st.write('### 전체 카테고리 월별 매출 비교')
    monthly_sales_all = cafe_data[cafe_data['year'] == selected_year].groupby(['month', 'category'])['price'].sum().unstack()
    st.bar_chart(monthly_sales_all, use_container_width=True)  # 컨테이너 너비 사용

# 네 번째 차트: 전체 카테고리 월별 매출 막대 차트 (Matplotlib 사용)
with col4:
    st.write('### 전체 카테고리 월별 매출')
    fig3, ax3 = plt.subplots(figsize=(10, 5))  # 크기를 키움
    monthly_sales_all.plot(kind='bar', ax=ax3)
    ax3.set_xlabel('월')
    ax3.set_ylabel('매출 (원)')
    ax3.set_title('전체 카테고리 월별 매출', fontsize=12)  # 제목 폰트 크기 조정
    st.pyplot(fig3, use_container_width=True)  # 컨테이너 너비 사용
