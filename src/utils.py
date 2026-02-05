from geopy.geocoders import Nominatim

from src.model import Destination

# 목적지를 검색하고 해당 목적지의 주소와 위도/경도 반환
# 연속 요청 시 1초 이상의 간격으로
def find_address_and_point(destination_name):
    geolocator = Nominatim(user_agent="chagokchagok")
    try:
        result_data = geolocator.geocode(destination_name, exactly_one=True)
        if result_data:
            return Destination(result_data.address, result_data.latitude, result_data.longitude)
        else:
            return None
    except Exception as e:
        raise e