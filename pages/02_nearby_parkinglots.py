import streamlit as st
from streamlit_folium import st_folium
import folium
import math

from src.db_crud import get_near_parking_data
from src.utils import find_address_and_point

ITEMS_PER_PAGE = 4

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="Parking Mate")

# 2. 세션 상태 초기화 (데이터 바구니 생성)
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if "list_current_page" not in st.session_state: #리스트에서 현재 탐색중인 페이지
    st.session_state.current_page = 1

if "destination" not in st.session_state: #검색 결과
    st.session_state.destination = None

# --- 레이아웃 시작 ---

# 4. 상단 로고 (검색바는 아래 right_col로 이동)
st.title("🚗 Parking Mate")
st.write("---")
st.subheader(f"🔍 검색 결과 ({len(st.session_state.search_results) if len(st.session_state.search_results)>0 else 0}건)")
# 5. 메인 레이아웃 분할: 왼쪽(리스트) | 오른쪽(검색창 + 지도)
left_col, right_col = st.columns([1, 2])


# --- 오른쪽 영역: 검색창(상단) + 지도(하단) ---
with right_col:
    # 지도 너비에 맞춘 단일 검색 폼
    with st.form(key='main_search_form'):
        search_input_col, search_btn_col = st.columns([5, 1])
        with search_input_col:
            target_location = st.text_input(
                label="검색어 입력",
                placeholder="어디로 가시나요? (예: 강남역)",
                label_visibility="collapsed"
            )
        with search_btn_col:
            search_submit = st.form_submit_button(label="검색")

    # 검색 로직 실행
    if search_submit:
        if target_location:
            with st.spinner('데이터를 불러오는 중...'):
                dest = find_address_and_point(target_location)
                st.session_state.destination = dest
                parking_lots = get_near_parking_data(dest)
                st.session_state.search_results = parking_lots
                st.rerun()  # 데이터를 세션에 넣은 후 화면 즉시 갱신
        else:
            st.warning("검색어를 입력해 주세요.")

    # 지도 표시 로직
    if st.session_state.search_results and len(st.session_state.search_results)>0:
        # 데이터가 있을 때 첫 번째 검색 결과 위치로 이동
        center_lat = st.session_state.search_results[0].lat
        center_lng = st.session_state.search_results[0].lng
        zoom_level = 14
    else:
        center_lat, center_lng = 37.5665, 126.9780  # 서울 기본 위치
        zoom_level = 12

    m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_level)
    # 목적지 마커 추가

    # 주차장 마커 추가
    if st.session_state.destination:
        dest = st.session_state.destination
        folium.Marker(
            location=[dest.lat, dest.lng],
            icon=folium.Icon(color="red", icon="star")
        ).add_to(m)

    # 주차장 마커 추가
    for parking_lot in st.session_state.search_results:
        # 1. 길찾기를 위한 출발지 정보 (검색창에 입력한 위치)
        if st.session_state.destination:
            # 주소 전체보다는 사용자가 검색한 명칭이 가독성이 좋습니다.
            raw_start_name = st.session_state.destination.name if st.session_state.destination.name else "내 목적지"
            start_lat = st.session_state.destination.lat
            start_lon = st.session_state.destination.lng
        else:
            raw_start_name = "내 목적지"
            start_lat, start_lon = center_lat, center_lng

        # 2. 안전한 URL 생성을 위한 인코딩 처리
        s_name = urllib.parse.quote(raw_start_name)
        e_name = urllib.parse.quote(parking_lot.name)

        # 카카오맵 길찾기 'dir' 파라미터 구성
        # sp: 출발지 좌표 및 이름, ep: 목적지 좌표 및 이름
        kakao_dir_url = (
            f"https://map.kakao.com/link/from/{s_name},{start_lat},{start_lon}"
            f"/to/{e_name},{parking_lot.lat},{parking_lot.lng}"
        )

        popup_html = f"""
            <div style="width:220px; font-family: 'Nanum Gothic', sans-serif; line-height:1.5;">
                <h4 style="margin:0 0 5px 0; color:#333;">{parking_lot.name}</h4>
                <div style="font-size:13px; color:#666; margin-bottom:10px;">
                    <b>📍 주소:</b> {parking_lot.full_addr}<br>
                    <b>🅿️ 주차면수:</b> <span style="color:#007BFF; font-weight:bold;">{parking_lot.space_no}면</span>
                </div>
                <a href="{kakao_dir_url}" target="_blank" 
                   style="display:block; text-align:center; padding:8px; background-color:#FAE100; color:#3C1E1E; text-decoration:none; border-radius:5px; font-size:13px; font-weight:bold;">
                   🚕 자동으로 길찾기 시작
                </a>
            </div>
            """

        folium.Marker(
            location=[parking_lot.lat, parking_lot.lng],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    st_folium(m, width="100%", height=600, key="main_map")



# --- 왼쪽 영역: 검색 결과 리스트 ---
with left_col:
    sort_option = st.radio("", ["가까운순 ▼", "이름순▼", "이름순▲"], horizontal=True)
    if st.session_state.search_results:
        total_items = len(st.session_state.search_results)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
        start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        if sort_option== '가까운순 ▼':
            page_data = st.session_state.search_results[start_idx:end_idx]
        elif sort_option== '이름순▼':
            page_data = sorted(st.session_state.search_results, key=lambda x:x.name, reverse=True)[start_idx:end_idx]
        else:
            page_data = sorted(st.session_state.search_results, key=lambda x: x.name)[start_idx:end_idx]

        for parking_lot in page_data:
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px; background-color:white;">
                    <h4 style="margin:0; color:black;">{parking_lot.name}</h4>
                    <p style="margin:5px 0; font-size:14px; color:#666;">📍 {parking_lot.full_addr}</p>
                    <p style="margin:0; color:#007BFF; font-weight:bold;">🅿️ 주차면수: {parking_lot.space_no}면</p>
                </div>
                """, unsafe_allow_html=True)

        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            is_first = st.session_state.current_page == 1
            if st.button("⬅️ 이전", use_container_width=True, disabled=is_first):
                st.session_state.current_page -= 1
                st.rerun()

        with col_page:
            st.markdown(
                f"""
                    <div style="text-align: center; background-color: #f0f2f6; border-radius: 8px; padding: 4px;">
                        <span style="font-size: 0.9rem; color: #555;">Page</span><br>
                        <strong style="font-size: 1.2rem; color: #007BFF;">{st.session_state.current_page}</strong> 
                        <span style="color: #999;">/ {total_pages}</span>
                    </div>
                    """,
                unsafe_allow_html=True
            )

        with col_next:
            is_last = st.session_state.current_page == total_pages
            if st.button("다음 ➡️", use_container_width=True, disabled=is_last):
                st.session_state.current_page += 1
                st.rerun()
    else:
        st.info("오른쪽 검색창에서 가고 싶은 곳을 검색해 보세요!")