import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach


@pytest.fixture(scope="function")
def setup_browser():
    load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env")
    )

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    if selenoid_url:
        # Настройка capabilities для Selenoid
        options = Options()
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": "127.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                # ,
                # "sessionTimeout": "5m",  # Увеличиваем до 5 минут
                # "env": ["TZ=UTC"]
            },
        }
        options.capabilities.update(selenoid_capabilities)

        # Создаем драйвер для Selenoid
        driver = webdriver.Remote(
            command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
            options=options,
        )

        driver.set_window_size(1920, 1080)

        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                window.localStorage.setItem('WELCOME_MODAL_DONT_SHOW', 'true');
            """
            },
        )

        # Настройка Selene с созданным драйвером
        browser.config.driver = driver
        browser.config.timeout = 10
    else:
        """Фикстура для настройки и управления браузером Chrome через Selene"""

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)

        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                window.localStorage.setItem('WELCOME_MODAL_DONT_SHOW', 'true');
            """
            },
        )

        browser.config.driver = driver

        browser.config.base_url = "https://alpmap.ru"
        browser.config.timeout = 10
        browser.config.save_page_source_on_failure = False

    yield browser

    # Прикрепление артефактов
    attach.add_screenshot(browser.driver)
    attach.add_logs(browser.driver)
    attach.add_html(browser.driver)
    attach.add_video(browser.driver)

    browser.quit()
