import re
from datetime import date

import dateparser
from fuzzywuzzy import process
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjCampoGoytacazesSpider(BaseGazetteSpider):
    name = "rj_campos_goytacazes"
    TERRITORY_ID = "3301009"
    allowed_domains = ["www.campos.rj.gov.br"]
    start_urls = ["https://www.campos.rj.gov.br/diario-oficial.php"]
    start_date = date(2013, 11, 1)
    months = [
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ]

    def parse(self, response):
        for element in response.css("ul.ul-licitacoes li"):
            gazette_data = element.css("h4::text")
            gazette_text = element.css("h4::text").get("")

            date_re = re.search(r"(\d{2} de (.*) de \d{4})", gazette_text)
            if not date_re:
                continue

            date = date_re.group(0).lower()
            month = date_re.group(2).lower()
            if month not in self.months:
                correct_month, id_fuzzy = process.extractOne(month, self.months)
                date = date.replace(month, correct_month)
                self.logger.warning(
                    f' Erro de digitação em "{gazette_text}". CORRIGIDO DE {month} PARA {correct_month}'
                )

            date = dateparser.parse(date, languages=["pt"]).date()
            if date > self.end_date:
                continue
            if date < self.start_date:
                return

            edition_number = gazette_data.re_first(r"Edição.*\s(\d+)")

            path_to_gazette = element.css("a::attr(href)").get().strip()
            # From November 17th, 2017 and backwards the path to the gazette PDF
            # is relative.
            if path_to_gazette.startswith("up/diario_oficial.php"):
                path_to_gazette = response.urljoin(path_to_gazette)

            is_extra_edition = bool(
                re.search(r"extra|supl|revis", gazette_text, re.IGNORECASE)
            )

            yield Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[path_to_gazette],
                power="executive",
            )

        next_url = (
            response.css(".pagination")
            .xpath("//a[contains(text(), 'Proxima')]/@href")
            .get()
        )
        if next_url:
            yield Request(response.urljoin(next_url))
