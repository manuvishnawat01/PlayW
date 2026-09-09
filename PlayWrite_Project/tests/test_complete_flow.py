# tests/test_complete_flow.py
# Test 2: Complete End-to-End automation test with dynamic category & product selection.

import os
import config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

def test_complete_e2e_flow(page):
    os.makedirs("screenshots", exist_ok=True)

    # Initialize Page Objects
    login_page = LoginPage(page)
    home_page = HomePage(page)
    category_page = CategoryPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    print("==================== test session starts ====================")
    print()

    # 1. Launch Website & Take Screenshot
    login_page.navigate(config.BASE_URL)
    assert login_page.is_login_page_displayed()
    page.screenshot(path="screenshots/01_website_launched.png")
    print("[STEP 1] Website launched successfully.")
    print()

    # 2. Login & Take Screenshot
    login_page.login(config.STANDARD_USER, config.PASSWORD)
    assert home_page.is_logged_in()
    page.screenshot(path="screenshots/02_login_success.png")
    print("[STEP 2] Login successful.")
    print()

    # 3. Dynamically Detect & Randomly Select Category -> Take Screenshot
    main_category, sub_category = home_page.select_random_category()
    page.screenshot(path="screenshots/03_category_selected.png")
    print()

    # 4. Dynamically Detect & Randomly Select Product -> Take Screenshot
    selected_product = category_page.select_random_product()
    actual_product = product_page.get_product_name()
    assert selected_product.lower() in actual_product.lower() or actual_product.lower() in selected_product.lower()
    page.screenshot(path="screenshots/04_product_selected.png")
    print()

    # 5. Add Selected Product to Cart -> Take Screenshot
    product_page.add_to_cart(selected_product)
    page.screenshot(path="screenshots/05_product_added_to_cart.png")
    print()

    # 6. Open Cart & Verify SAME Selected Product is Present -> Take Screenshot
    product_page.open_cart()
    assert cart_page.is_cart_page_displayed()
    cart_page.verify_product_in_cart(selected_product)
    page.screenshot(path="screenshots/06_cart_verified.png")
    print()

    # 7. Logout & Take Screenshot
    cart_page.logout()
    assert login_page.is_login_page_displayed()
    page.screenshot(path="screenshots/07_logout.png")
    print("[LOGOUT] Logout successful.")
    print()

    print("==================================================")
    print("E2E TEST SUMMARY")
    print("==================================================")
    print(f"Main Category    : {main_category}")
    print(f"Sub-category     : {sub_category}")
    print(f"Selected Product : {selected_product}")
    print("==================================================")
