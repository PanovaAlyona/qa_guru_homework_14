import allure

from models.mountain import Mountain
from pages.home_page import HomePage
from steps.contact_steps import ContactSteps
from steps.route_steps import RouteSteps


@allure.epic("ALPMAP")
@allure.feature("Поиск")
@allure.title("Отфильтровать горы по категориям")
def test_filter_by_category_mountain(setup_browser):
    homepage = HomePage()
    homepage.open(
        "https://alpmap.ru/#?lng=102.31910705566408&zoom=12&lat=51.90721369567919"
    )

    route_pages = RouteSteps()
    category = "5А"

    route_pages.filter_mount_by_categories(category)
    route_pages.check_mountains_category(category)


@allure.title("Поиск горы и ее маршрутов")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_find_mountain_and_route(setup_browser):
    route_pages = RouteSteps()

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
        number_region="2. КАВКАЗ",
    )

    homepage = HomePage()
    homepage.open()
    route_pages.find_mount_by_name("Эльбрус")
    route_pages.find_routes_by_peak_name(mountain.name)
    route_pages.check_visible_peak_pointer(mountain.name)
    route_pages.should_have_routes(mountain)


@allure.title("Поиск несуществующей горы")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_not_found_mount(setup_browser):
    route_pages = RouteSteps()
    homepage = HomePage()
    homepage.open()
    route_pages.find_mount_by_name("123456789")
    route_pages.check_mount_not_found()


@allure.title("Открыть маршрут на сайте ФАР")
@allure.epic("ALPMAP")
@allure.feature("Поиск")
def test_open_route_in_far(setup_browser):
    route_pages = RouteSteps()

    homepage = HomePage()
    homepage.open()

    mountain = Mountain(
        name="Мунку-Сардык",
        route_list=[
            "с ЮВ",
        ],
        number_area="6.1.1.",
        number_region="6. САЯНЫ",
    )
    with allure.step("найти гору по названию"):
        route_pages.find_mount_by_name(mountain.name)
    route_pages.find_routes_by_peak_name(mountain.name)

    route_pages.open_route_in_far(mountain.route_list[0])
    route_pages.check_table_values(
        mountain.number_area + mountain.name,
        mountain.route_list[0],
        mountain.number_region,
    )


@allure.title("Открыть контакты автора в телеграм")
@allure.epic("ALPMAP")
@allure.feature("Контакты")
def test_open_telegram(setup_browser):
    homepage = HomePage()
    homepage.open()

    contact_pages = ContactSteps()
    contact_pages.open_telegram_contact()
    contact_pages.check_telegram_contact("@alpmap")
