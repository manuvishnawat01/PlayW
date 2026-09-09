# tests/test_data_driven_login.py
# Test 1: CSV Data-Driven Login Test (Positive & Negative Test Cases). No screenshots.

import pytest
import config
from utils.csv_reader import read_login_data
from pages.login_page import LoginPage
from pages.home_page import HomePage

login_dataset = read_login_data()

@pytest.mark.parametrize("username,password,expected_result", login_dataset)
def test_csv_data_driven_login(page, username, password, expected_result):
    login_page = LoginPage(page)
    home_page = HomePage(page)

    # 1. Launch & Submit Login Form
    login_page.navigate(config.BASE_URL)
    login_page.login(username, password)

    # 2. Check Expected Result
    if expected_result == "success":
        # Positive Test Case: Verify successful login & logout
        assert home_page.is_logged_in()
        home_page.logout()
        assert login_page.is_login_page_displayed()

    elif expected_result == "failure":
        # Negative Test Case: Verify application rejects invalid credentials & shows error message
        assert login_page.is_login_error_visible()
        print("[NEGATIVE TEST PASSED] Application correctly rejected invalid login!")
