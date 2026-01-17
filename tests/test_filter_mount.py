import allure

from models.mountain import Mountain
from pages.contact_steps import ContactSteps
from pages.route_steps import RouteSteps


@allure.epic("ALPMAP")
@allure.feature("Поиск")
@allure.title("Отфильтровать горы по категориям")
def test_filter_by_category_mountain(setup_browser):
    browser = setup_browser
    route_steps = RouteSteps(browser)
    route_steps.open(
        "https://alpmap.ru/#?lng=102.31910705566408&zoom=12&lat=51.90721369567919"
    )

    category = "5А"

    route_steps.filter_mount_by_categories(category)
    route_steps.check_mountains_category(category)


@allure.title("Поиск горы и ее маршрутов")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_find_mountain_and_route(setup_browser):
    browser = setup_browser
    route_steps = RouteSteps(browser)

    mountain = Mountain(
        name="Эльбрус, Западная",
        route_list=[
            'через "Приют-11" ("Классика с Юга")',
            "с севера",
            "траверс",
            'через 3 плечо ("купол")',
            "СЗ ребру",
            "З склону через Утюг",
        ],
        number_area="2.4",
        number_region="2. КАВКАЗ"
    )

    route_steps.open()
    route_steps.find_mount_by_name("Эльбрус")
    route_steps.find_routes_by_peak_name(mountain.name)
    route_steps.check_visible_peak_pointer(mountain.name)
    route_steps.should_have_routes(mountain)

@allure.title("Поиск несуществующей горы")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_not_found_mount(setup_browser):
    browser = setup_browser
    route_steps = RouteSteps(browser)

    route_steps.open()
    route_steps.find_mount_by_name("123456789")
    route_steps.check_mount_not_found()

@allure.title("Открыть маршрут на сайте ФАР")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_open_route_in_far(setup_browser):
    browser = setup_browser
    route_steps = RouteSteps(browser)

    route_steps.open()

    mountain = Mountain(
        name="Мунку-Сардык",
        route_list=[
            "с ЮВ",
        ],
        number_area="6.1.1.",
        number_region="6. САЯНЫ"
    )
    with allure.step("найти гору по названию"):
        route_steps.find_mount_by_name(mountain.name)
    route_steps.find_routes_by_peak_name(mountain.name)

    route_steps.open_route_in_far(mountain.route_list[0])
    route_steps.check_table_values(
        mountain.number_area + mountain.name, mountain.route_list[0], mountain.number_region
    )

@allure.title("Открыть контакты автора в телеграм")
@allure.epic("ALPMAP")
@allure.feature("Контакты")
def test_open_telegram(setup_browser):
    browser = setup_browser
    contact_steps = ContactSteps(browser)
    route_steps = RouteSteps(browser)

    route_steps.open()
    contact_steps.open_telegram_contact()
    contact_steps.check_telegram_contact("@alpmap")
