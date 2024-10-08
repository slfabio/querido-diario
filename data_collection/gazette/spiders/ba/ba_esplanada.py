from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaEsplanadaSpider(BaseDoemSpider):
    TERRITORY_ID = "2910602"
    name = "ba_esplanada"
    state_city_url_part = "ba/esplanada"
    start_date = date(2021, 1, 4)
