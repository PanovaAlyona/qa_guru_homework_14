import allure
from qa_guru_homework_14.find_steps import FindSteps



@allure.title("Поиск несуществующей горы")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_find_mountain_and_route(setup_browser):
    browser = setup_browser
    find_steps = FindSteps(browser)

    find_steps.open()
    find_steps.close_welcome_modal()
    find_steps.find_mount_by_name("123456789")
    find_steps.check_mount_not_found()

