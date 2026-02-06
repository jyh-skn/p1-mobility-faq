# 임시 entry page
import streamlit as st

def render_entry():
    # 1. CSS를 이용한 카드 스타일 커스텀
    st.markdown("""
        <style>
        .service-card {
            border-radius: 15px;
            padding: 30px;
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            height: 250px;
            text-align: center;
        }
        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            background-color: #ffffff;
            border-color: #007bff;
        }
        .icon-text {
            font-size: 50px;
            margin-bottom: 15px;
        }
        .title-text {
            font-size: 24px;
            font-weight: bold;
            color: #343a40;
        }
        .desc-text {
            font-size: 14px;
            color: #6c757d;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. 메인 헤더
    st.markdown("<h1 style='text-align: center;'>🚀 ChagokChagok</h1>", unsafe_allow_html=True)
    st.write("---")

    # 3. 서비스 카드 섹션
    col1, col2, col3 = st.columns(3)

    with col1:
        # HTML 카드 시뮬레이션
        st.markdown("""
            <div class="service-card">
                <div class="icon-text">🅿️</div>
                <div class="title-text">주차장 서비스</div>
                <div class="desc-text">전국 주차장 위치와<br>총 주차 가능한 공간을 확인하세요.</div>
            </div>
        """, unsafe_allow_html=True)
        # 실제 이동을 위한 투명한 버튼 혹은 아래 버튼 배치
        if st.button("주차장 찾아보기", key="btn_parking", use_container_width=True):
            st.switch_page("pages/02_nearby_parkinglots.py")

    with col2:
        st.markdown("""
            <div class="service-card">
                <div class="icon-text">⛽</div>
                <div class="title-text">주유소 서비스</div>
                <div class="desc-text">내 주변 최저가 주유소와<br>부가 서비스 정보를 비교하세요.</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("주유소 찾아보기", key="btn_gas", use_container_width=True):
            st.switch_page("pages/04_search_gas_station.py")

    with col3:
        st.markdown("""
                    <div class="service-card">
                        <div class="icon-text">🔍</div>
                        <div class="title-text">통합 서비스</div>
                        <div class="desc-text">주차장과 주유소의 서비스를 함께 확인하세요.</div>
                    </div>
                """, unsafe_allow_html=True)
        if st.button("통합 찾아보기", key="btn_parking_gas", use_container_width=True):
            st.switch_page("pages/05_search_parking_gas.py")

    # 4. 하단 통계 요약 (AI 백엔드 느낌 강조)

if __name__ == "__main__":
    render_entry()

    st.spinner('데이터를 불러오는 중...')