#streamlit main page
import streamlit as st

# 페이지 정의
entry_p = st.Page("pages/01_entry_page.py", title="홈", icon="🏠", default=True)
nearby_parking_p = st.Page("pages/02_nearby_parkinglots.py", title="Parking Mate", icon="🅿️")
parking_by_region_p = st.Page("pages/03_prototype_category_app.py", title="Parking Lot by region", icon="🅿️")
search_gas_station_p =  st.Page("pages/04_search_gas_station.py", title="Gas Station Mate", icon="⛽")

# 내비게이션 실행
pg = st.navigation({'home':[entry_p], 'parking':[nearby_parking_p, parking_by_region_p], 'Gas Station':[search_gas_station_p]})

# 이전 페이지와 비교
if "prev_page" not in st.session_state:
    st.session_state.prev_page = pg.title

if st.session_state.prev_page != pg.title:
    st.session_state.prev_page = pg.title

    # session_state 상태 확인 코드
    # st.write(st.session_state)

    # 1. session_state에 유지해야하는 key
    keep_keys = ['prev_page']

    # 2. session_state key 중에 keep_keys에 없는 것만 삭제
    for key in list(st.session_state.keys()):
        if key not in keep_keys:
            del st.session_state[key]

pg.run()