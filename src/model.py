class ParkingLot:
    def __init__(self, id: int ,reg_id: str, name: str, lat: str, lng: str, sido: str, sigungu: str, full_addr: str, space_no: int, distance: float):
        self.__id = id
        self.__reg_id = reg_id
        self.__name = name
        self.__lat = lat
        self.__lng = lng
        self.__sido = sido
        self.__sigungu = sigungu
        self.__full_addr = full_addr
        self.__space_no = space_no
        self.__distance = distance

    @property
    def id(self):
        return self.__id

    @property
    def reg_id(self):
        return self.__reg_id

    @property
    def name(self):
        return self.__name

    @property
    def lat(self):
        return self.__lat

    @property
    def lng(self):
        return self.__lng

    @property
    def sido(self):
        return self.__sido

    @property
    def sigungu(self):
        return self.__sigungu

    @property
    def full_addr(self):
        return self.__full_addr

    @property
    def space_no(self):
        return self.__space_no

    @property
    def distance(self):
        return self.__distance

    def __repr__(self):
        return f'ParkingLot(id = {self.__id}, reg_id = "{self.__reg_id}", name = "{self.__name}", lat = "{self.__lat}", lng = "{self.__lng}", sido = "{self.__sido}", sigungu = {self.__sigungu}, full_addr = {self.__full_addr}, space_no = {self.__space_no}, distance = {self.__distance})'

class Destination:
    def __init__(self, name: str, address: str, lat: float, lng: float):
        self.__name = name
        self.__address = address
        self.__lat = lat
        self.__lng = lng

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address
    @property
    def lat(self):
        return self.__lat
    @property
    def lng(self):
        return self.__lng

    def __repr__(self):
        return f'Destination(name = "{self.__name}", address = "{self.__address}", lat = {self.__lat}, lng = {self.__lng})'


# 주유소 API 관련
class GasStation:
    def __init__(self, reg_id: str, station_name: str, price: int, brand_name: str,  lat: str, lng: str, distance: float):
        self.__reg_id = reg_id
        self.__station_name = station_name
        self.__price = price
        self.__brand_name = brand_name
        self.__lat = lat
        self.__lng = lng
        self.__distance = distance

        @property
        def reg_id(self):
            return self.__reg_id
        @property
        def station_name(self):
            return self.__station_name
        @property
        def price(self):
            return self.__price
        @property
        def brand_name(self):
            return self.__brand_name
        @property
        def lat(self):
            return self.__lat
        @property
        def lng(self):
            return self.__lng
        @property
        def distance(self):
            return self.__distance

    def __repr__(self):
        return f'GasStation(reg_id = "{self.__reg_id}", station_name = "{self.__station_name}", price = "{self.__price}", brand_name = "{self.__brand_name}", lat = "{self.__lat}", lng = "{self.__lng}", distance = {self.__distance})'