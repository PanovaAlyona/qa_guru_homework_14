import time

import allure
from selene import be, by, have, query

from qa_guru_homework_14.find_steps import FindSteps
from qa_guru_homework_14.mountain import Mountain


@allure.title("Проверка поиска альпинистского маршрута")
@allure.epic("ALPMAP")
@allure.feature("Поиск горы и ее маршрутов")
def test_find_mountain_and_route(setup_browser):
    browser = setup_browser
    find_steps = FindSteps(browser)

    mountain = Mountain(
        mount_name="Эльбрус",
        mount_peak_name="Эльбрус, Западная",
        route_list=[
            'через "Приют-11" ("Классика с Юга")',
            "с севера",
            "траверс",
            'через 3 плечо ("купол")',
            "СЗ ребру",
            "З склону через Утюг",
        ],
    )

    find_steps.open()
    find_steps.close_welcome_modal()
    find_steps.find_mount_by_name(mountain)
    find_steps.find_routes_by_peak_name(mountain)
    find_steps.check_visible_peak_pointer(mountain)
    find_steps.should_have_routes(mountain)

    time.sleep(20)
