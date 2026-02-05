import streamlit as st
from streamlit_folium import st_folium
import folium
import mysql.connector
import pandas as pd
import os
import json
import math
import warnings
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

# --- 0. 불필요한 경고 및 출력 억제 ---
warnings.filterwarnings('ignore', category=UserWarning)

# 1. 환경 설정 로드
load_dotenv('env')
geolocator = Nominatim(user_agent="parking_mate")

db_config_raw = os.getenv("DB_CONFIG")
if db_config_raw:
    DB_CONFIG = json.loads(db_config_raw)
else:
    st.error("DB 설정 정보를 불러올 수 없습니다.")

# 2. 세션 상태 초기화
if 'results' not in st.session_state:
    st.session_state['results'] = pd.DataFrame()
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()

# 3. DB 조회 함수
def get_parking_data_by_coords(lat, lng, radius=3000):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = """
                SELECT name, lat, lng, full_address, space_no,
                       ST_Distance_Sphere(POINT(lng, lat), POINT(%s, %s)) AS distance
                FROM parking_lot
                HAVING distance <= %s
                ORDER BY distance
                """
        df = pd.read_sql(query, conn, params=(lng, lat, radius))
        conn.close()
        return df
    except Exception as e:
        st.error(f"DB 조회 중 오류: {e}")
        return pd.DataFrame()

# --- 레이아웃 설정 ---
st.set_page_config(layout="wide", page_title="Parking Mate")

# ⭐ [통합 CSS] 버튼 겹침 방지 및 글자 깨짐 해결
st.markdown("""
    <style>
    /* 버튼 내부 글자 줄바꿈 방지 */
    div.stButton > button p {
        white-space: nowrap !important;
        font-size: 14px !important;
    }
    /* 버튼 간격 및 최소 너비 최적화 */
    div.stButton > button {
        min-width: 35px !important; 
        width: 100% !important;
        padding: 0px !important;
        margin: 0px 2px !important; 
    }
    /* 컬럼 간격 미세 조정 */
    [data-testid="column"] {
        padding-left: 1px !important;
        padding-right: 1px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 사이드바: 즐겨찾기 목록 표시 및 개별 삭제
with st.sidebar:
    st.header("⭐ 즐겨찾기 목록")
    if st.session_state.favorites:
        for fav_name in list(st.session_state.favorites):
            col_fav_name, col_delete = st.columns([4, 1])
            with col_fav_name:
                st.write(f"✅ {fav_name}")
            with col_delete:
                if st.button("🗑️", key=f"del_{fav_name}"):
                    st.session_state.favorites.remove(fav_name)
                    st.rerun()
        st.write("---")
        if st.button("즐겨찾기 전체 삭제"):
            st.session_state.favorites = set()
            st.rerun()
    else:
        st.info("찜한 주차장이 없습니다.")

st.title("🚗 Parking Mate")
st.write("---")

left_col, right_col = st.columns([1, 2])
df = st.session_state['results']

# --- 왼쪽 영역: 검색 결과 리스트 & 개선된 페이지네이션 ---
with left_col:
    st.subheader(f"🔍 검색 결과 ({len(df)}건)")
    st.radio("정렬", ["가까운순 ▼", "가격순 ▼", "공영"], horizontal=True)
    st.write("---")

    if not df.empty:
        # [1] 페이지네이션 설정 (한 페이지에 4개씩)
        items_per_page = 4
        total_pages = math.ceil(len(df) / items_per_page)

        # [2] 현재 페이지 그룹 계산 (5개 버튼씩 묶음)
        current_group = (st.session_state.page - 1) // 5
        start_page = current_group * 5 + 1
        end_page = min(start_page + 4, total_pages)

        # 데이터 슬라이싱
        start_idx = (st.session_state.page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        df_page = df.iloc[start_idx:end_idx]

        # 리스트 카드 출력 (일체형 별표 디자인)
        for i, row in df_page.iterrows():
            with st.container(border=True):
                col_name, col_star = st.columns([0.85, 0.15])
                is_fav = row['name'] in st.session_state.favorites
                star_icon = "⭐" if is_fav else "☆"

                with col_name:
                    st.markdown(f"#### {row['name']}")
                with col_star:
                    if st.button(star_icon, key=f"star_{i}", use_container_width=True):
                        if is_fav:
                            st.session_state.favorites.remove(row['name'])
                        else:
                            st.session_state.favorites.add(row['name'])
                        st.rerun()
                st.write(f"📍 {row['full_address']}")
                st.write(f"🅿️ **주차면수: {row['space_no']}면**")

        st.write("---")

        # [3] 화살표 + 숫자 5개 버튼 UI (겹침 방지 비율 적용)
        page_cols = st.columns([1.5, 1, 1, 1, 1, 1, 1.5])

        with page_cols[0]:
            if current_group > 0:
                if st.button("◀", key="prev_group"):
                    st.session_state.page = start_page - 1
                    st.rerun()

        for i, p in enumerate(range(start_page, end_page + 1)):
            with page_cols[i + 1]:
                btn_type = "primary" if st.session_state.page == p else "secondary"
                if st.button(str(p), key=f"p_{p}", type=btn_type, use_container_width=True):
                    st.session_state.page = p
                    st.rerun()

        with page_cols[6]:
            if end_page < total_pages:
                if st.button("▶", key="next_group"):
                    st.session_state.page = end_page + 1
                    st.rerun()
    else:
        st.info("오른쪽 검색창에서 가고 싶은 곳을 검색해 보세요!")

# --- 오른쪽 영역: 검색창 & 지도 ---
with right_col:
    with st.form(key='main_search_form'):
        search_input_col, search_btn_col = st.columns([5, 1])
        with search_input_col:
            target_location = st.text_input(label="검색어", placeholder="예: 강남역, 서초동", label_visibility="collapsed")
        with search_btn_col:
            search_submit = st.form_submit_button(label="검색")

    if search_submit:
        if target_location:
            with st.spinner(f"'{target_location}' 주변을 찾는 중..."):
                location = geolocator.geocode(target_location)
                if location:
                    df_results = get_parking_data_by_coords(location.latitude, location.longitude, 3000)
                    if len(df_results) > 25:
                        df_results = get_parking_data_by_coords(location.latitude, location.longitude, 1500)
                        st.info(f"💡 결과가 많아 가장 가까운 1.5km 이내 정보 위주로 보여드려요!")

                    st.session_state['results'] = df_results
                    st.session_state.page = 1
                    st.rerun()
                else:
                    st.warning("장소를 찾을 수 없습니다.")
        else:
            st.warning("검색어를 입력해 주세요.")

    center_lat, center_lng = (df.iloc[0]['lat'], df.iloc[0]['lng']) if not df.empty else (37.5665, 126.9780)
    m = folium.Map(location=[center_lat, center_lng], zoom_start=14 if not df.empty else 12)

    for i, row in df.iterrows():
        is_fav = row['name'] in st.session_state.favorites
        marker_color = 'red' if is_fav else 'orange' #
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=f"<b>{row['name']}</b>",
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(m)

    st_folium(m, width="100%", height=600, key="main_map")