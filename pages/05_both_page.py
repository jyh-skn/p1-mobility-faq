import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import math
import urllib

# 백엔드 함수 임포트
from src.db_crud import get_near_parking_data, get_near_gas_data
from src.utils import find_address_and_point

ITEMS_PER_PAGE = 4

# 1. 페이지 설정 및 디자인 CSS
st.set_page_config(layout="wide", page_title="Mobility Mate")

st.markdown("""
    <style>
    div.stButton > button p { white-space: nowrap !important; font-size: 14px !important; }
    div.stButton > button { min-width: 35px !important; width: 100% !important; padding: 0px !important; margin: 0px 2px !important; }
    [data-testid="column"] { padding-left: 1px !important; padding-right: 1px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화 (검색 결과 및 페이지 관리)
if 'map_center' not in st.session_state: st.session_state.map_center = [37.5665, 126.9780]
if 'search_results' not in st.session_state: st.session_state.search_results = []
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'parking'
if 'current_page' not in st.session_state: st.session_state.current_page = 1
if 'destination' not in st.session_state: st.session_state.destination = None

st.title("🚗 Mobility Mate")

# 3. [상단] 검색바 영역 (엔터 및 검색 버튼 모두 지원)
with st.form(key='search_form'):
    col_in, col_btn = st.columns([5, 1])
    target = col_in.text_input("어디로 가시나요?", placeholder="예: 강남역", label_visibility="collapsed")
    search_submit = col_btn.form_submit_button("검색")

if search_submit and target:
    dest = find_address_and_point(target)
    if dest:
        st.session_state.destination = dest
        st.session_state.map_center = [dest.lat, dest.lng]

        print("==================================> "+ str(st.session_state.map_center))
        # 💡 검색 즉시 현재 선택된 모드(주차장/주유소) 데이터를 리스트에 채움
        if st.session_state.view_mode == 'parking':
            st.session_state.search_results = get_near_parking_data(dest.lat, dest.lng)

        else:
            st.session_state.search_results = get_near_gas_data(dest.lat, dest.lng)
        st.session_state.current_page = 1
        st.rerun()

# 4. [중단] 서비스 전환 버튼 (주차장 vs 주유소)
st.write("")
btn_col1, btn_col2, _ = st.columns([1, 1, 4])
if btn_col1.button("🅿️ 주차장", type="primary" if st.session_state.view_mode == 'parking' else "secondary",
                   use_container_width=True):
    st.session_state.view_mode = 'parking'
    # 현재 지도 위치 기준으로 주차장 데이터 갱신
    st.session_state.search_results = get_near_parking_data(*st.session_state.map_center)
    st.session_state.current_page = 1
    st.rerun()

if btn_col2.button("⛽ 주유소", type="primary" if st.session_state.view_mode == 'gas' else "secondary",
                   use_container_width=True):
    st.session_state.view_mode = 'gas'
    # 현재 지도 위치 기준으로 주유소 데이터 갱신
    st.session_state.search_results = get_near_gas_data(*st.session_state.map_center)
    st.session_state.current_page = 1
    st.rerun()

st.write("---")

# 5. [하단] 레이아웃 분할: 왼쪽(리스트) | 오른쪽(지도)
l_col, r_col = st.columns([1, 2])

# --- 오른쪽: 지도 영역 ---
with r_col:
    m = folium.Map(location=st.session_state.map_center, zoom_start=15)
    cluster = MarkerCluster().add_to(m)

    # 목적지 마커 (빨간 별)
    folium.Marker(st.session_state.map_center, icon=folium.Icon(color='red', icon='star')).add_to(m)

    # 검색 결과 마커 및 길찾기 팝업
    for item in st.session_state.search_results:
        color = 'blue' if st.session_state.view_mode == 'parking' else 'orange'

        # 카카오맵 길찾기 URL 생성
        s_name = urllib.parse.quote(target if target else "내 위치")
        e_name = urllib.parse.quote(item.name)
        kakao_url = f"https://map.kakao.com/link/from/{s_name},{st.session_state.map_center[0]},{st.session_state.map_center[1]}/to/{e_name},{item.lat},{item.lng}"

        popup_html = f"""
            <div style="width:200px; font-family: sans-serif;">
                <b>{item.name}</b><br>
                <small style="color: gray;">{item.full_addr}</small><br>
                <a href="{kakao_url}" target="_blank" style="display:block; margin-top:8px; padding:6px; background:#FAE100; text-align:center; border-radius:4px; text-decoration:none; color:black; font-weight:bold; font-size:12px;">🚕 카카오맵 길찾기</a>
            </div>
        """
        folium.Marker([item.lat, item.lng], popup=folium.Popup(popup_html, max_width=300),
                      icon=folium.Icon(color=color)).add_to(cluster)

    st_folium(m, width="100%", height=550, key=f"map_{st.session_state.map_center}_{st.session_state.view_mode}")

# --- 왼쪽: 리스트 영역 ---
with l_col:
    mode_nm = "주차장" if st.session_state.view_mode == 'parking' else "주유소"
    st.subheader(f"🔍 {mode_nm} 결과 ({len(st.session_state.search_results)}건)")

    # 정렬 기능 (Code A의 장점 이식)
    sort_option = st.radio("", ["가까운순 ▼", "이름순▼", "이름순▲"], horizontal=True, key="sort_radio")

    if st.session_state.search_results:
        # 데이터 정렬
        if sort_option == '이름순▼':
            sorted_data = sorted(st.session_state.search_results, key=lambda x: x.name, reverse=True)
        elif sort_option == '이름순▲':
            sorted_data = sorted(st.session_state.search_results, key=lambda x: x.name)
        else:
            sorted_data = st.session_state.search_results  # 기본 거리순 유지

        # 페이지네이션 계산
        total_items = len(sorted_data)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
        start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
        page_data = sorted_data[start_idx: start_idx + ITEMS_PER_PAGE]

        # 카드 리스트 출력
        for item in page_data:
            with st.container(border=True):
                st.markdown(f"#### {item.name}")
                st.caption(f"📍 {item.full_addr}")
                if st.session_state.view_mode == 'parking':
                    st.write(f"🅿️ 주차면수: **{item.space_no}면**")
                else:
                    st.write(f"⛽ 가격: **{int(item.price):,}원**")
                    st.caption(f"📏 거리: {int(item.distance)}m")

        # 숫자 버튼 페이지네이션 (Code A의 고급 UI)
        st.write("---")
        current_group = (st.session_state.current_page - 1) // 5
        start_page = current_group * 5 + 1
        end_page = min(start_page + 4, total_pages)

        page_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
        with page_cols[0]:
            if current_group > 0:
                if st.button("◀", key="prev"):
                    st.session_state.current_page = start_page - 1
                    st.rerun()
        for i, p in enumerate(range(start_page, end_page + 1)):
            with page_cols[i + 1]:
                if st.button(str(p), key=f"p_{p}",
                             type="primary" if st.session_state.page == p or st.session_state.current_page == p else "secondary"):
                    st.session_state.current_page = p
                    st.rerun()
        with page_cols[6]:
            if end_page < total_pages:
                if st.button("▶", key="next"):
                    st.session_state.current_page = end_page + 1
                    st.rerun()
    else:
        st.info("검색 결과가 없습니다. 다른 지역을 검색해 보세요!")

