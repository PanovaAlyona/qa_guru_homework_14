import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach


@pytest.fixture(scope="function")
def setup_browser_chrome():
    """Фикстура для настройки и управления браузером Chrome через Selene"""

    # 2. Настройка опций Chrome
    chrome_options = Options()
    chrome_options.add_argument(
        "--no-sandbox"
    )  # Отключает sandbox (часто нужно в CI/CD)
    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )  # Решает проблемы с памятью
    chrome_options.add_argument(
        "--disable-gpu"
    )  # Отключает GPU (для стабильности)
    chrome_options.add_argument("--window-size=1920,1080")

    # 3. Создание драйвера с нашими опциями
    driver = webdriver.Chrome(options=chrome_options)

    # 4. Настройка Selene для работы с созданным драйвером
    browser.config.driver = driver

    # 5. Дополнительные настройки Selene
    browser.config.base_url = "https://alpmap.ru"
    browser.config.timeout = 10
    browser.config.save_page_source_on_failure = False

    # 6. Инициализация дополнительных возможностей Selene
    # browser.config._wait_decorator = support._logging.wait_with

    # 7. Возвращаем управление тесту
    yield browser

    # Прикрепление артефактов
    attach.add_screenshot(browser.driver)
    attach.add_logs(browser.driver)
    attach.add_html(browser.driver)
    attach.add_video(browser.driver)

    # 8. Пост-условия (выполняются после теста)
    if browser.driver:  # Проверяем, существует ли драйвер
        browser.quit()


@pytest.fixture(scope="function")
def setup_browser():
    """Фикстура для настройки и управления браузером Chrome через Selenoid"""
    load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env")
    )

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    # Настройка capabilities для Selenoid
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "127.0",
        "selenoid:options": {"enableVNC": True, "enableVideo": True},
    }
    options.capabilities.update(selenoid_capabilities)

    # Создаем драйвер для Selenoid
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options,
    )

    # Настройка Selene с созданным драйвером
    browser.config.driver = driver
    browser.config.timeout = 10
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    # Прикрепление артефактов
    attach.add_screenshot(browser.driver)
    attach.add_logs(browser.driver)
    attach.add_html(browser.driver)
    attach.add_video(browser.driver)

    browser.quit()
