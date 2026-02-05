import requests
# mysql-connector
import mysql.connector
from dotenv import load_dotenv
import os

from model import ParkingLot

load_dotenv()

# mysql-connection 정보
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'skn26',
    'password': 'skn26',
    'database':'menudb'
}

API_KEY = os.getenv("API_KEY")
BASE_URL = 'https://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}

# for pageno in range(1, PAGE_NO):
params = {'serviceKey':API_KEY, 'pageNo':1,'numOfRows':2000, 'format':2}
response = requests.get(url=BASE_URL, params=params, headers=headers)

parking_lots_list: list[ParkingLot] = []
if response.status_code == 200:
    parking_lots = response.json()["PrkSttusInfo"] #주차장 리스트
    # print(parking_lots)
    # print(len(parking_lots))

    if len(parking_lots) > 0:
        for parking_lot in parking_lots:
            if parking_lot['prk_plce_entrc_la'] and parking_lot['prk_plce_entrc_lo']:
                parking_lots_list.append(ParkingLot(None, parking_lot['prk_center_id'], parking_lot['prk_plce_nm'], parking_lot['prk_plce_entrc_la'], parking_lot['prk_plce_entrc_lo'], parking_lot['prk_plce_adres_sido'], parking_lot['prk_plce_adres_sigungu'], parking_lot['prk_plce_adres'], parking_lot['prk_cmprt_co']))

else:
    print('PROBLEM', response.status_code, response.text)
print(parking_lots_list)

if len(parking_lots_list) > 0:
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:
                for parking_lot in parking_lots_list:
                    cursor.execute("""
                        insert
                          into parkinglot (id
                                          , reg_id
                                          , name
                                          , lat
                                          , lng
                                          , sido
                                          , sigungu
                                          , full_address
                                          , space_no
                                          , coord
                                        )
                        values ( %s
                               , %s
                               , %s
                               , %s
                               , %s
                               , %s
                               , %s
                               , %s
                               , %s
                               , ST_GeomFromText(concat('POINT(', %s, ' ', %s, ')'), 4326, 'axis-order=long-lat')
                               )
                    """, (None ,parking_lot.reg_id, parking_lot.name, parking_lot.lat, parking_lot.lng, parking_lot.sido, parking_lot.sigungu, parking_lot.full_addr, parking_lot.space_no, parking_lot.lng, parking_lot.lat))
                conn.commit()
    except mysql.connector.Error as err:
        print('DB에러: ', err)

# executemany 참고 코드
"""
if len(parking_lots_list) > 0:
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:

                # %s 순서: reg_id, name, lat, lng, sido, sigungu, addr, space, lng, lat
                sql = '''
                    INSERT INTO parkinglot (
                        reg_id, name, lat, lng, sido, sigungu, full_address, space_no, coord
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, 
                        ST_GeomFromText(CONCAT('POINT(', %s, ' ', %s, ')'), 4326, 'axis-order=long-lat')
                    )
                '''

                # 2. 데이터 리스트 빌드 (List of Tuples)
                data_list = [
                    (
                        p.reg_id, p.name, p.lat, p.lng, p.sido, p.sigungu, p.full_addr, p.space_no,
                        p.lng, # POINT 경도
                        p.lat  # POINT 위도
                    ) for p in parking_lots_list
                ]

                # 3. 일괄 삽입 실행
                cursor.executemany(sql, data_list)
                
                conn.commit()
                print(f"총 {cursor.rowcount}개의 데이터가 성공적으로 삽입되었습니다.")

    except mysql.connector.Error as err:
        print('DB에러: ', err)

"""

#