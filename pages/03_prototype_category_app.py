import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import math
import numpy as np

from folium.plugins import MarkerCluster

ITEMS_PER_PAGE = 4

# csv 파일 읽어옴
df = pd.read_csv('KC_490_WNTY_PRKLT_2024.csv')

if "current_page" not in st.session_state: #현재 검색중인 페이지
    st.session_state.current_page = 1

if 'sido_name' not in st.session_state:         # 선택된 시도명 저장
    st.session_state.sido_name = ""

if 'sgg_name' not in st.session_state:          # 선택된 시군구명 저장
    st.session_state.sgg_name = ""

if 'search_result' not in st.session_state:     # 선택된 시군구 데이터 저장
    st.session_state.search_result = pd.DataFrame()

# 페이지 설정
st.set_page_config(layout="wide", page_title="지역별 주차장 검색 프로토타입")

# 페이지 제목
st.title("🚗 지역별 주차장 찾기")

# 1. 입력부: 검색바와 버튼
# 검색창과 버튼을 나란히 배치하기 위해 컬럼 사용
col1, col2, col3 = st.columns([0.45, 0.45, 0.1])
with col1:
    st.session_state.sido_name = col1.selectbox(
        '시도명을 선택해주세요.',
        sorted(df['CTPRVN_NM'].unique()),           # 시도명을 가나다순으로 정렬
        index=None,                                 # 처음 선택을 None으로 초기화
        placeholder='시도명을 선택해주세요.',
        label_visibility="collapsed"
    )
with col2:
    if st.session_state.sido_name:      # 시도명이 선택되면 선택된 시도명에 해당하는 시군구 필터링해 출력.
        data_sd = df[df['CTPRVN_NM'] == st.session_state.sido_name]
        st.session_state.sgg_name = col2.selectbox(
            '시군구명을 선택해주세요',
            sorted(data_sd['SIGNGU_NM'].unique()),  # 시군구명을 가나다순으로 정렬
            index=None,                             # 처음 선택을 None으로 초기화
            placeholder='시군구명을 선택해주세요.',
            label_visibility="collapsed"
        )
    else:           # 시도명이 선택되지 않았을 시 빈 selectbox 출력.
        st.session_state.sgg_name = col2.selectbox(
            '시군구명을 선택해주세요.',
            [],                             # 시도명이 선택되기 전 빈 리스트 띄움
            index=None,                             # 처음 선택을 None으로 초기화
            placeholder='시도명을 먼저 선택해주세요.',
            label_visibility="collapsed"
        )

with col3:
    # st.write("")
    # st.write("")
    search_btn = st.button("검색", use_container_width=True)
    if st.session_state.sido_name and st.session_state.sgg_name and search_btn:     # 시도명, 시군구명, 버튼 클릭이 모두 충족되는 경우
        st.session_state.search_result = data_sd[data_sd['SIGNGU_NM'] == st.session_state.sgg_name] # 결과 값에 시군구명까지 필터링한 데이터 저장


st.divider()  # 구분선

# 2. 메인 화면 구성 (지도 2 : 리스트 1 비율)
main_col2, main_col1 = st.columns([1, 2])

if not st.session_state.search_result.empty:  # 검색 결과가 나온경우
    # [논리] 여기서 DB 세션을 열고 검색 로직을 수행합니다.

    result = st.session_state.search_result
    with main_col1:  # 지도탭
        st.subheader("📍 주변 지도")
        # 지도 생성
        m = folium.Map(location=[np.mean(result['FCLTY_LA']), np.mean(result['FCLTY_LO'])], zoom_start=13)  # 시군구의 모든 주차장 위도,경도의 평균값을 넣었음
        cluster = MarkerCluster().add_to(m)
        # 데이터 마커 추가
        for lat, lon, name in zip(result['FCLTY_LA'], result['FCLTY_LO'], result['FCLTY_NM']):  # 각 행의 위도, 경도, 주차장이름 추출
            folium.Marker(
                location=[lat, lon],    # 위도, 경도
                popup=name,             # 주차장 이름
                tooltip=name,           # 주차장 이름
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(cluster)

        # 지도 렌더링
        clicked_place = st_folium(m, width='100%', height=800)
        if clicked_place and clicked_place.get("last_object_clicked_tooltip"):
            clicked_name = clicked_place["last_object_clicked_tooltip"]
            st.session_state.selected_parking = clicked_name
            # 페이지 리런을 통해 리스트 색상을 즉시 반영
            st.rerun()

    with main_col2:  # 리스트탭
        df = st.session_state.search_result
        total_items = len(st.session_state.search_result)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
        start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_data = df.iloc[start_idx:end_idx]

        st.subheader(f"📋 검색 결과 ({total_items}개)")
        for index, row in page_data.iterrows():
            with st.container():
                st.markdown(f"### {row['FCLTY_NM']}")           # 주차장 이름
                st.write(f'주소: {row['RDNMADR_NM']}')            # 주차장 도로주소
                st.caption(f"요금: {row['UTILIIZA_CHRGE_CN']}")   # 유료/무료 여부
                if st.button(f"상세보기", key=f"btn_{index}"):
                    st.write(f"{row['FCLTY_NM']}의 추가적인 정보나 리뷰 정보 등이 표시됩니다")
                st.divider()
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("이전") and st.session_state.current_page > 1:
                st.session_state.current_page -= 1
                st.rerun()

        with col_page:
            st.write(f"{st.session_state.current_page} / {total_pages}")

        with col_next:
            if st.button("다음") and st.session_state.current_page < total_pages:
                st.session_state.current_page += 1
                st.rerun()


else:
    st.info("지역을 선택하고 검색 버튼을 눌러주세요.")