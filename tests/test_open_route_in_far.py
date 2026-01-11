import allure
from qa_guru_homework_14.find_steps import FindSteps
from qa_guru_homework_14.mountain import Mountain


@allure.title("Открыть маршрут на сайте ФАР")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_find_mountain_and_route(setup_browser):
    browser = setup_browser
    find_steps = FindSteps(browser)

    find_steps.open()
    find_steps.close_welcome_modal()

    mountain = Mountain(
        name="Мунку-Сардык",
        route_list=[
            "с ЮВ",
        ],
    )

    find_steps.find_mount_by_name(mountain.name)
    find_steps.find_routes_by_peak_name(mountain.name)

    find_steps.open_route_in_far(mountain.route_list[0])
    find_steps.check_table_values(f'6.1.1.'+mountain.name, mountain.route_list[0])



