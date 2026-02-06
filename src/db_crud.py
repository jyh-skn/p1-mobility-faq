import mysql.connector
import pandas as pd
import streamlit as st

from src.model import ParkingLot
from src.model import Destination

from src.utils import get_mbr_polygon

from src.config import config_db

@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(**config_db)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None


def get_near_parking_data(_dest: Destination):
    try:
        conn = get_connection()
        if not conn:
            return list()
        if not conn.is_connected():
            conn.reconnect(attempts=3, delay=2)
        delta = 0.023
        min_lat, max_lat = _dest.lat - delta, _dest.lat + delta
        min_lng, max_lng = _dest.lng - delta, _dest.lng + delta

        sql = '''SELECT id, reg_id, name, lat, lng, sido, sigungu, full_address, space_no, use_yn, ST_Distance_Sphere(POINT(lng, lat), POINT(%s, %s)) as dist FROM parking_lot WHERE MBRContains(ST_GeomFromText(%s, 4326, 'axis-order=long-lat'), coord) 
                 and use_yn = 'Y'
              '''
        polygon_str = get_mbr_polygon(min_lng, min_lat, max_lng, max_lat)
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (_dest.lng, _dest.lat, polygon_str))
            rows = cursor.fetchall()
            if not rows: return list()
            print(ParkingLot)
            return [ParkingLot(row['id'], row['reg_id'], row['name'], row['lat'], row['lng'], row['sido'], row['sigungu'], row['full_address'], row['space_no'], row["dist"])for row in rows]

    except Exception as e:
        st.error(f"DB 연결 오류: {e}")
        return []
@st.cache_data
def get_sido_sigungu():
    try:
        conn = get_connection()
        if not conn:
            return list()
        if not conn.is_connected():
            conn.reconnect(attempts=3, delay=2)
        sql = '''
            select 
                  distinct sido, sigungu
                from parking_lot
               where use_yn = 'Y'
              '''
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            result = {}
            rows = cursor.fetchall()
            for row in rows:
                if row['sido'] not in result:
                    result[row['sido']] = []
                else:
                    result[row['sido']].append(row['sigungu'])
            return result
    except Exception as e:
        st.error(f"DB 연결 오류: {e}")
        return dict()


@st.cache_data
def get_region_parking_data():
    return pd.DataFrame(run_query('''
        SELECT name, \
               lat, \
               lng, \
               sido, \
               sigungu,\
               full_address, \
               space_no
          FROM parking_lot
         WHERE use_yn = 'Y'
    '''))

def run_query(query, params=None, is_select=True):
    """
    query를 실행하는 함수.
    """
    conn = get_connection()
    if not conn:
        return None

    # 연결이 끊겼는지 확인하고 필요시 재연결
    if not conn.is_connected():
        conn.reconnect()

    cursor = conn.cursor(dictionary=True)  # 결과를 딕셔너리 형태(k-v)로 반환
    try:
        cursor.execute(query, params or ())

        if is_select:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()  # INSERT, UPDATE, DELETE는 commit 필수
            return cursor.rowcount  # 영향을 받은 행의 수 반환

    except mysql.connector.Error as err:
        st.error(f"SQL 에러: {err}")
        return None
    finally:
        cursor.close()

def run_bulk_insert_query(query, params=None):
    """
    대량의 insert query를 실행하는 함수.
    """
    conn = get_connection()
    if not conn:
        return None

    # 연결이 끊겼는지 확인하고 필요시 재연결
    if not conn.is_connected():
        conn.reconnect()
    else:
        # 기존 연결의 잔여 결과물을 강제로 비우기 (안전장치)
        conn.consume_results()

    cursor = conn.cursor(dictionary=True, buffered=True)  # 결과를 딕셔너리 형태(k-v)로 반환
    try:
        # 대량 데이터 execute
        cursor.executemany(query, params or ())
        conn.commit()
        return cursor.rowcount  # 영향을 받은 행의 수 반환

    except mysql.connector.Error as err:
        print(f"SQL 에러: {err}")
        return None
    except Exception as err:
        print(f"에러: {err}")
    finally:
        cursor.close()
