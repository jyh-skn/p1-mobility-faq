import streamlit as st
from streamlit_folium import st_folium
import folium
import math
from folium.plugins import MarkerCluster

from src.utils import get_oil_stations, find_address_and_point

ITEMS_PER_PAGE = 4

# 2. 페이지 설정
st.set_page_config(layout="wide", page_title="Oil Mate")
#
# 세션 상태 초기화
if 'oil_results' not in st.session_state:
    st.session_state.oil_results = []

if 'destination' not in st.session_state:   # 검색 결과
    st.session_state.destination = None

if "current_page" not in st.session_state: #리스트에서 현재 탐색중인 페이지
    st.session_state.current_page = 1

# --- 레이아웃 ---

stations = st.session_state['oil_results']
# 4. 상단 로고 (검색바는 아래 right_col로 이동)
st.title("⛽ Oil Mate")
st.write("---")
st.subheader(f"🔍 검색 결과 ({len(stations)}건)")
# 5. 메인 레이아웃 분할: 왼쪽(리스트) | 오른쪽(검색창 + 지도)
left_col, right_col = st.columns([1, 2])

# --- 왼쪽 영역: 검색 결과 리스트 ---
with left_col:
    sort_option = st.radio("", ["가까운순▼", "가격낮은순▼", "이름순▲", "이름순▼"], horizontal=True)
    if stations:
        # 정렬 라디오 버튼 (이 코드가 subheader 바로 아래 있어야 화면에 뜹니다)
        st.write("---")

        # ---------------- 2. 필터 정렬 로직 (stations 리스트 직접 정렬) ----------------
        if sort_option == '가까운순▼':
            stations.sort(key=lambda x: x.distance)
        elif sort_option == '가격낮은순▼':  # 주유소 앱 특성상 이름보다 가격이 중요하므로 예시로 추가
            stations.sort(key=lambda x: x.price)
        elif sort_option == '이름순▲':
            stations.sort(key=lambda x: x.station_name)
        elif sort_option == '이름순▼':
            stations.sort(key=lambda x: x.station_name, reverse=True)

        total_items = len(stations)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

        current_group = (st.session_state.current_page - 1) // 5
        start_page = current_group * 5 + 1
        end_page = min(start_page + 4, total_pages)

        start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_data = stations[start_idx:end_idx]
        for s in page_data:
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px; background-color:white;">
                    <h4 style="margin:0; color:#333;">{s.station_name} <small style="color:#666;">({s.brand_name})</small></h4>
                    <p style="margin:5px 0; font-size:16px; color:#ff4b4b; font-weight:bold;">가격: {s.price:,}원</p>
                    <p style="margin:0; font-size:13px; color:#666;">📏 거리: {s.distance}m</p>
                </div>
                """, unsafe_allow_html=True)

        st.write("---")
        page_cols = st.columns([1.1, 1, 1, 1, 1, 1, 1.5])

        with page_cols[0]:
            if current_group > 0:
                if st.button("◀", key="prev_group"):
                    st.session_state.current_page = start_page - 1
                    st.rerun()

        for i, p in enumerate(range(start_page, end_page + 1)):
            with page_cols[i + 1]:
                btn_type = "primary" if st.session_state.current_page == p else "secondary"
                if st.button(str(p), key=f"p_{p}", type=btn_type, use_container_width=True):
                    st.session_state.current_page = p
                    st.rerun()

        with page_cols[6]:
            if end_page < total_pages:
                if st.button("▶", key="next_group"):
                    st.session_state.current_page = end_page + 1
                    st.rerun()
    else:
        st.info("오른쪽 검색창에서 동네 이름이나 주소를 검색해 보세요!")

# --- 오른쪽 영역: 검색창 + 지도 ---
with right_col:
    # 1. 주소 검색 폼
    with st.form(key='search_form'):
        search_col, btn_col = st.columns([4, 1])
        with search_col:
            address_input = st.text_input("어디 근처 주유소를 찾으시나요?", placeholder="예: 강남역, 성수동, 분당구 등", label_visibility="collapsed")
        with btn_col:
            search_submit = st.form_submit_button("검색")

    if search_submit:
        if address_input:
            with st.spinner('위치 확인 및 주유소 데이터를 불러오는 중...'):
                # A. 주소를 좌표로 변환
                dest = find_address_and_point(address_input)
                st.session_state.destination = dest
                if dest:
                    # B. 해당 좌표 주변 주유소 검색
                    found_stations = get_oil_stations(dest.lat, dest.lng)
                    st.session_state.oil_results = found_stations
                    st.rerun()
                else:
                    st.warning("입력하신 주소의 위치를 찾을 수 없습니다. 다시 시도해 주세요.")
        else:
            st.error("검색어를 입력해 주세요.")

    # 2. 지도 표시
    if st.session_state.destination:
        # 사용자가 입력한 장소로 지도 중심 고정
        center_lat = st.session_state.destination.lat
        center_lng = st.session_state.destination.lng
        zoom_level = 14
    else:
        center_lat, center_lng = 37.5665, 126.9780  # 서울 기본 위치
        zoom_level = 12
    
    m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_level)
    cluster = MarkerCluster().add_to(m)

    # 목적지 마커 추가
    if st.session_state.destination:
        dest = st.session_state.destination
        folium.Marker(
            location=[dest.lat, dest.lng],
            icon=folium.Icon(color="red", icon="star")
        ).add_to(m)

    # 주변 주유소 마커
    for s in stations:
        # 출발지 정보: 사용자가 검색한 주소와 좌표
        # 목적지 정보: 주유소 이름과 좌표
        start_name = address_input if address_input else "내 검색 위치"
        start_lat, start_lon = [dest.lat, dest.lng]

        # 카카오맵 길찾기 'dir' 파라미터 구성
        # sp: 출발지 좌표 및 이름, ep: 목적지 좌표 및 이름
        kakao_dir_url = (
            f"https://map.kakao.com/link/from/{start_name},{start_lat},{start_lon}"
            f"/to/{s.station_name},{s.lat},{s.lng}"
        )

        popup_html = f"""
            <div style="width:220px; font-family: 'Nanum Gothic', sans-serif; line-height:1.5;">
                <h4 style="margin:0 0 5px 0; color:#333;">{s.station_name}</h4>
                <div style="font-size:13px; color:#666; margin-bottom:10px;">
                    <b>💰 가격:</b> <span style="color:#ff4b4b; font-weight:bold;">{s.price:,}원</span><br>
                    <b>™️ 브랜드:</b> {s.brand_name}<br>
                    <b>📏 거리:</b> {s.distance}m
                </div>
                <a href="{kakao_dir_url}" target="_blank" 
                   style="display:block; text-align:center; padding:8px; background-color:#FAE100; color:#3C1E1E; text-decoration:none; border-radius:5px; font-size:13px; font-weight:bold;">
                   🚕 자동으로 길찾기 시작
                </a>
            </div>
            """

        folium.Marker(
            location=[s.lat, s.lng],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='blue', icon='tilt', prefix='fa')
        ).add_to(cluster)

    st_folium(m, width="100%", height=600, key="oil_map", returned_objects=[])