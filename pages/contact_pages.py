import allure
from selene import be, browser, have


class ContactPages:

    # def __init__(self):
    #     self.browser = browser

    @allure.step("Открыть контакты из телеграм")
    def open_telegram_contact(self):
        filter_button = browser.all(
            '[id^="headlessui-disclosure-button-"]'
        ).element_by(have.text("Полезные ссылки"))
        filter_button.click()

        link = browser.all(".flex-1.min-w-0").element_by(
            have.text("Написать автору")
        )

        link.should(be.visible)
        link.click()

    @allure.step("Проверить, что открыты нужные контакты из телеграм")
    def check_telegram_contact(self, telegram: str):
        browser.switch_to_next_tab()
        browser.element(".tgme_page_extra").should(have.exact_text(telegram))
