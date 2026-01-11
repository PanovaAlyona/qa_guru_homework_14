import allure

from qa_guru_homework_14.category import Category
from qa_guru_homework_14.find_steps import FindSteps

@allure.title("Отфильтровать горы по категориям")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_filter_by_category_mountain(setup_browser):
    browser = setup_browser
    find_steps = FindSteps(browser)
    find_steps.open('https://alpmap.ru/#?lng=102.31910705566408&zoom=12&lat=51.90721369567919')
    find_steps.close_welcome_modal()

    category = Category(
        "5А"
    )

    find_steps.filter_mount_by_categories(category)
    find_steps.check_mountains_category(category)
