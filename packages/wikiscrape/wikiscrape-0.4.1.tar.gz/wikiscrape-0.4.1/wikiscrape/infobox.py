from bs4 import BeautifulSoup

from .wikitable import Wikitable


class Infobox(Wikitable):
    @property
    def data(self) -> list[BeautifulSoup]:
        return [tr.td.contents[0] for tr in self.table.find_all("tr") if tr.th]

    def to_dicts(self) -> list[dict[BeautifulSoup, BeautifulSoup]]:
        return [dict(zip(self.headers, self.data))]
