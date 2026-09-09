# conftest.py
# Pytest fixture for Playwright browser setup and flat failure screenshots.

import os
import pytest
from playwright.sync_api import sync_playwright

_driver_page = None

@pytest.fixture
def page():
    """Launches Chromium browser in headed mode with slow motion delay."""
    global _driver_page
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1500)
        _driver_page = browser.new_page()
        yield _driver_page
        browser.close()
        _driver_page = None

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Automatically takes a screenshot directly in screenshots/ if any test step fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if _driver_page:
            os.makedirs("screenshots", exist_ok=True)
            clean_name = item.name.replace("[", "_").replace("]", "_").replace("@", "_").replace(".", "_")
            failure_path = f"screenshots/failure_{clean_name}.png"
            _driver_page.screenshot(path=failure_path)
            print(f"\n[FAILURE SCREENSHOT] Test failed! Captured screenshot at: {failure_path}")
