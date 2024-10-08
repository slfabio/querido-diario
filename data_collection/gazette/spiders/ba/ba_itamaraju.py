from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaItamarajuSpider(BaseDoemSpider):
    TERRITORY_ID = "2915601"
    name = "ba_itamaraju"
    state_city_url_part = "ba/itamaraju"
    start_date = date(2008, 3, 28)
