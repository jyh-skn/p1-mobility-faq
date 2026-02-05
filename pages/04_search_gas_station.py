import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os
import requests
from pyproj import Transformer
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

from folium.plugins import MarkerCluster

# 1. 환경 설정 및 API 키 로드
load_dotenv()
OPINET_KEY = os.getenv("OPINET")

# 좌표 변환기 설정 (WGS84 <-> KATEC)
KATEC_STR = "+proj=tmerc +lat_0=38 +lon_0=128 +k=0.9999 +x_0=400000 +y_0=600000 +ellps=bessel +units=m +no_defs +towgs84=-115.80,483.35,664.43,0,0,0,0"
WGS84_STR = "epsg:4326"

to_katec = Transformer.from_crs(WGS84_STR, KATEC_STR, always_xy=True)
to_wgs84 = Transformer.from_crs(KATEC_STR, WGS84_STR, always_xy=True)

# 주소 -> 위경도 변환기 (Nominatim 사용)
geolocator = Nominatim(user_agent="gas_station_mate")

BRAND_MAP = {
    'SKE': 'SK에너지', 'GSC': 'GS칼텍스', 'HDO': '현대오일뱅크',
    'SOL': 'S-OIL', 'RTE': '자영알뜰', 'RTX': '고속도로알뜰',
    'NHO': '농협알뜰', 'ETC': '자가상표', 'E1G': 'E1', 'SKG': 'SK가스', 'RTO': '자영알뜰'
}

# 2. 페이지 설정
st.set_page_config(layout="wide", page_title="Gas Station Mate")

# 세션 상태 초기화
if 'oil_results' not in st.session_state:
    st.session_state['oil_results'] = []
if 'map_center' not in st.session_state:
    st.session_state['map_center'] = [37.5665, 126.9780]  # 서울 시청 기준


# 3. 데이터 호출 함수
def get_oil_stations(lat, lon, radius=3000):
    kx, ky = to_katec.transform(lon, lat)
    url = "https://www.opinet.co.kr/api/aroundAll.do"
    params = {
        "code": OPINET_KEY,
        "out": "json",
        "x": kx,
        "y": ky,
        "radius": radius,
        "prodcd": "B027",  # 휘발유 기준
        "sort": 1  # 거리순
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        stations = data.get('RESULT', {}).get('OIL', [])

        for s in stations:
            s['lng'], s['lat'] = to_wgs84.transform(s['GIS_X_COOR'], s['GIS_Y_COOR'])
            s['brand_nm'] = BRAND_MAP.get(s['POLL_DIV_CD'], '기타')
        return stations
    except Exception as e:
        st.error(f"오피넷 API 오류: {e}")
        return []


# --- 레이아웃 ---
st.title("⛽ 주유 Mate")
st.write("---")

left_col, right_col = st.columns([1, 2])
stations = st.session_state['oil_results']

# --- 왼쪽 영역: 검색 결과 리스트 ---
with left_col:
    st.subheader(f"🔍 주변 주유소 ({len(stations)}건)")
    if stations:
        for s in stations:
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px; background-color:white;">
                    <h4 style="margin:0; color:#333;">{s['OS_NM']} <small style="color:#666;">({s['brand_nm']})</small></h4>
                    <p style="margin:5px 0; font-size:16px; color:#ff4b4b; font-weight:bold;">가격: {int(s['PRICE']):,}원</p>
                    <p style="margin:0; font-size:13px; color:#666;">📏 거리: {s['DISTANCE']}m</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("오른쪽 검색창에서 동네 이름이나 주소를 검색해 보세요!")

# --- 오른쪽 영역: 검색창 + 지도 ---
with right_col:
    # 1. 주소 검색 폼
    with st.form(key='search_form'):
        search_col, btn_col = st.columns([4, 1])
        with search_col:
            address_input = st.text_input("어디 근처 주유소를 찾으시나요?", placeholder="예: 강남역, 성수동, 분당구 등")
        with btn_col:
            search_submit = st.form_submit_button("검색")

    if search_submit:
        if address_input:
            with st.spinner('위치 확인 및 주유소 데이터를 불러오는 중...'):
                # A. 주소를 좌표로 변환
                location = geolocator.geocode(address_input)
                if location:
                    # B. 해당 좌표 주변 주유소 검색
                    found_stations = get_oil_stations(location.latitude, location.longitude)
                    st.session_state['oil_results'] = found_stations
                    st.session_state['map_center'] = [location.latitude, location.longitude]
                    st.rerun()
                else:
                    st.warning("입력하신 주소의 위치를 찾을 수 없습니다. 다시 시도해 주세요.")
        else:
            st.error("검색어를 입력해 주세요.")

    # 2. 지도 표시
    m = folium.Map(location=st.session_state['map_center'], zoom_start=14)
    cluster = MarkerCluster().add_to(m)

    # 검색 중심점 마커 (내 위치 느낌)
    folium.Marker(
        location=st.session_state['map_center'],
        popup="검색 위치",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(m)

    # 주변 주유소 마커
    for s in stations:
        folium.Marker(
            location=[s['lat'], s['lng']],
            popup=f"<b>{s['OS_NM']}</b><br>가격: {s['PRICE']}원",
            tooltip=f"{s['OS_NM']} ({s['PRICE']}원)",
            icon=folium.Icon(color='blue', icon='oil-can', prefix='fa')
        ).add_to(cluster)

    st_folium(m, width="100%", height=600, key="oil_map")