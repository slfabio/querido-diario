from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaPradoSpider(BaseDoemSpider):
    TERRITORY_ID = "2925501"
    name = "ba_prado"
    state_city_url_part = "ba/prado"
    start_date = date(2013, 2, 4)
