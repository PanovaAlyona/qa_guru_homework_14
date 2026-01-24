from selene import browser


class HomePage:

    def open(self, url="https://alpmap.ru/"):
        browser.open(url)
