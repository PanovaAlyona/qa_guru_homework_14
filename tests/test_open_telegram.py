import allure
from qa_guru_homework_14.find_steps import FindSteps



@allure.title("Открыть контакты автора в телеграм")
@allure.epic("ALPMAP")
@allure.feature("Контакты")
def test_open_telegram(setup_browser):
    browser = setup_browser
    find_steps = FindSteps(browser)

    find_steps.open()
    find_steps.close_welcome_modal()
    find_steps.open_telegram_contact()
    find_steps.check_telegram_contact()

