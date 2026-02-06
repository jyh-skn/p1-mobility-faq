import streamlit as st
from streamlit import session_state
from streamlit_folium import st_folium
import folium
import mysql.connector
import pandas as pd
import os
import json
import math
import warnings  # 👈 경고 메시지 제어를 위해 추가
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from src.db_crud import run_query
from folium.plugins import MarkerCluster

from src.db_crud import get_sido_sigungu
from src.db_crud import get_region_parking_data

# --- 0. 불필요한 경고 및 출력 억제 ---
# Pandas의 SQLAlchemy 관련 UserWarning을 무시합니다.
warnings.filterwarnings('ignore', category=UserWarning)

# 1. 환경 설정 로드 (메시지 출력 제거)
load_dotenv()
geolocator = Nominatim(user_agent="parking_mate")

db_config_raw = os.getenv("DB_CONFIG")
if db_config_raw:
    DB_CONFIG = json.loads(db_config_raw)
else:
    st.error("DB 설정 정보를 불러올 수 없습니다.")

# 세션 상태 초기화

if 'search_result' not in st.session_state:
    st.session_state['search_result'] = pd.DataFrame()

if 'sido_name' not in st.session_state:         # 선택된 시도명 저장
    st.session_state.sido_name = ""

if 'sgg_name' not in st.session_state:          # 선택된 시군구명 저장
    st.session_state.sgg_name = ""

if 'page' not in st.session_state:
    st.session_state.page = 1

if 'region_data' not in st.session_state: # 시도/시군구 저장해둘 state 변수 - 시도를 key로, 시군구를 value 로
    st.session_state.region_data = get_sido_sigungu()

df = st.session_state.search_result
# --- 레이아웃 설정 ---
st.set_page_config(layout="wide", page_title="Parking Mate")
st.title("🚗 Parking Mate")
st.write("---")
st.subheader(f"🔍 검색 결과 ({len(df)}건)")

# --- 상단 구현 ---
left_col, right_col = st.columns([1, 2])

# --- 왼쪽 영역: 조회 결과 리스트 ---
with left_col:
    all_data = get_region_parking_data()
    # 1. 필터 UI (조회 결과 리스트 바로 위나 적절한 위치에 배치)
    sort_option = st.radio("", ["이름순▼", "이름순▲"], horizontal=True)

    if not df.empty:
        # ---------------- 여기에 필터 정렬 로직 추가 ----------------
        if sort_option == '이름순▼':
            df = df.sort_values(by='name', ascending=False)
        else: # 이름순▲
            df = df.sort_values(by='name', ascending=True)
        # --------------------------------------------------------

        # 2. 페이지네이션 설정
        items_per_page = 5
        total_pages = min(math.ceil(len(df) / items_per_page), 5)
        start_idx = (st.session_state.page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        df_page = df.iloc[start_idx:end_idx]
        for i, row in df_page.iterrows():
            st.markdown(f"""
            <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px; background-color:white;">
                <h4 style="margin:0; color:black;">{row['name']}</h4>
                <p style="margin:5px 0; font-size:14px; color:#666;">📍 {row['full_address']}</p>
                <p style="margin:0; color:#007BFF; font-weight:bold;">🅿️ 주차면수: {row['space_no']}면</p>
            </div>
            """, unsafe_allow_html=True)
        st.write("---")
        cols = st.columns([1] * (total_pages + 2))
        for p in range(1, total_pages + 1):
            with cols[p]:
                btn_type = "primary" if st.session_state.page == p else "secondary"
                if st.button(str(p), key=f"p_{p}", type=btn_type, use_container_width=True):
                    st.session_state.page = p
                    st.rerun()
    else:
        st.info("위 선택창에서 원하는 위치를 선택해 보세요!")

# --- 오른쪽 영역: 지도 ---
with right_col:
    with st.container(border=True):
        col1, col2, col3 = st.columns([0.45, 0.45, 0.1])

        with col1:
            st.session_state.sido_name = col1.selectbox(
                '시도 선택',
                # sorted(df['sido'].unique()),           # 시도명을 가나다순으로 정렬
                sorted(st.session_state.region_data.keys()),  # 딕셔너리의 키값들
                index=None,  # 처음 선택을 None으로 초기화
                placeholder='시도명을 선택해주세요.',
                label_visibility="collapsed"
            )
        with col2:
            if st.session_state.sido_name:  # 시도명이 선택되면 선택된 시도명에 해당하는 시군구 필터링해 출력.
                data_sd = all_data[all_data['sido'] == st.session_state.sido_name]
                st.session_state.sgg_name = col2.selectbox(
                    '시군구 선택',
                    #    sorted(data_sd['sigungu'].unique()),  # 시군구명을 가나다순으로 정렬
                    sorted(st.session_state.region_data[st.session_state.sido_name]),  # 딕셔너리 값 조회
                    index=None,  # 처음 선택을 None으로 초기화
                    placeholder='시군구명을 선택해주세요.',
                    label_visibility="collapsed"
                )
            else:  # 시도명이 선택되지 않았을 시 빈 selectbox 출력.
                st.session_state.sgg_name = col2.selectbox(
                    '시군구 선택',
                    [],  # 시도명이 선택되기 전 빈 리스트 띄움
                    index=None,  # 처음 선택을 None으로 초기화
                    placeholder='시도명을 먼저 선택해주세요.',
                    label_visibility="collapsed"
                )

        with col3:
            search_btn = st.button("검색", use_container_width=True)
            if st.session_state.sido_name and st.session_state.sgg_name and search_btn:  # 시도명, 시군구명, 버튼 클릭이 모두 충족되는 경우
                st.session_state.search_result = data_sd[
                    data_sd['sigungu'] == st.session_state.sgg_name]  # 결과 값에 시군구명까지 필터링한 데이터 저장
            #        print(st.session_state.search_result)

    # 지도 표시
    center_lat, center_lng = (df.iloc[0]['lat'], df.iloc[0]['lng']) if not df.empty else (37.5665, 126.9780)
    m = folium.Map(location=[center_lat, center_lng], zoom_start=14 if not df.empty else 12)

    cluster = MarkerCluster().add_to(m)

    for i, row in df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=f"<b>{row['name']}</b><br>면수: {row['space_no']}면",
            icon=folium.Icon(color='orange', icon='info-sign')
         ).add_to(cluster)

    st_folium(m, width="100%", height=600, key="main_map", returned_objects=[])