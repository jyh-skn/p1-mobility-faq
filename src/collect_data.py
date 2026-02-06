from utils import fetch_from_api    # api 호출하는 함수
from utils import valid_check_with_logging    # api 호출하는 함수
from db_crud import run_bulk_insert_query
from config import config_api_key
import time

def fetch_parking_api():
    '''주차장 정보 가져오기'''

    BASE_URL = 'https://apis.data.go.kr/B553881/Parking/PrkSttusInfo'   # api url 정보
    data_list = []      # api를 받는 data 리스트
    page_no = 1         # page no
    total_saved = 0     # 전체 저장된 개수 카운트
    BATCH_SIZE = 4000   # 만 건 단위로 끊기

    while True:
        numOfRows = 2000    # 한번에 받는 데이터의 수
        items = fetch_from_api( # fetch_from_api(api 공통함수 호출)
            BASE_URL,
            {'serviceKey': config_api_key,'pageNo':page_no,'numOfRows':numOfRows, 'format':2}
        ).get("PrkSttusInfo", [])

        if not items: # 더이상 데이터가 없으면 중단
            break

        data_list.extend(items)
        print(f"{page_no}페이지 완료 (누적: {len(data_list)}건)")

        # list가 설정한 Batch size보다 커지면 DB에 저장
        if len(data_list) >= BATCH_SIZE:
            print(f"{len(data_list)}건 도달! DB 저장을 시작합니다.")

            required = ['prk_center_id', 'prk_plce_nm', 'prk_plce_entrc_la', 'prk_plce_entrc_lo']

            # 검증 함수 실행
            validated_list = valid_check_with_logging(data_list, required)

            # DB에 저장하기 좋게 가공 (튜플 형태로 변환)
            processed_data = [
                (data.get('prk_center_id'), data.get('prk_plce_nm'), data.get('prk_plce_entrc_la'), data.get('prk_plce_entrc_lo')
                     , data.get('prk_plce_adres_sido') , data.get('prk_plce_adres_sigungu'), data.get('prk_plce_adres')
                 , data.get('prk_cmprt_co'), data.get('error_yn'), data.get('error_msg'))
                for data in validated_list
            ]

            sql = '''
                INSERT INTO parking_lot_raw (
                    reg_id, name, lat, lng, sido, sigungu, full_address, space_no, err_yn, err_msg, reg_nm
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'API'
                )
            '''

            # DB 저장 함수 호출 (이미 만들어둔 bulk_insert 사용)
            inserted_count = run_bulk_insert_query(sql, processed_data)

            normal_data = [
                (data.get('prk_center_id'), data.get('prk_plce_nm'), data.get('prk_plce_entrc_la'),
                 data.get('prk_plce_entrc_lo')
                     , data.get('prk_plce_adres_sido'), data.get('prk_plce_adres_sigungu'), data.get('prk_plce_adres')
                     , data.get('prk_cmprt_co'), data.get('prk_plce_entrc_lo'),
                 data.get('prk_plce_entrc_la'))
                for data in validated_list if data.get('error_yn') == 'N'
            ]

            normal_sql = """
                  INSERT INTO parking_lot (reg_id, name, lat, lng, sido, sigungu, full_address, space_no, coord)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(CONCAT('POINT(', %s, ' ', %s, ')'), 4326, 'axis-order=long-lat'))
                  """

            inserted_normal_count = run_bulk_insert_query(normal_sql, normal_data)

            if inserted_count:
                total_saved += inserted_count
                print(f"DB 저장 완료! (누적 저장: {total_saved}건)")
                # 🔥 2. 저장 성공 후 리스트 비우기
                data_list = []
            else:
                print("DB 저장 실패. 다음 루프에서 재시도합니다.")

        page_no += 1
    return None

fetch_parking_api()