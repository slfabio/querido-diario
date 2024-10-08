from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaTucanoSpider(BaseDoemSpider):
    TERRITORY_ID = "2931905"
    name = "ba_tucano"
    state_city_url_part = "ba/tucano"
    start_date = date(2013, 1, 4)
