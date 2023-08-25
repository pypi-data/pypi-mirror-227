class Wikitable:
    def __init__(self, table):
        self.table = table

    @property
    def headers(self):
        return [th.contents[0] for th in self.table.find_all("th")]

    @property
    def data(self):
        return [
            [td.contents[0] for td in tr.find_all("td")]
            for tr in self.table.find_all("tr")
            if not tr.th
        ]

    def to_dicts(self):
        return [dict(zip(self.headers, row)) for row in self.data]
