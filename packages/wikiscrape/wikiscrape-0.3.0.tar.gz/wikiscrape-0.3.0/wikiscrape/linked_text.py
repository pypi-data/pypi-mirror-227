class LinkedText:
    def __init__(self, content):
        self.content = content

    @property
    def link(self):
        return (self.content.a or {}).get("href")

    @property
    def text(self):
        return self.content.text.strip()
