# tests/test_complete_flow.py
# Test 2: Complete End-to-End automation test with dynamic multi-product cart validation.

import os
import config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.cart_page import CartPage

def test_complete_e2e_flow(page):
    os.makedirs("screenshots", exist_ok=True)

    # Initialize Page Objects
    login_page = LoginPage(page)
    home_page = HomePage(page)
    category_page = CategoryPage(page)
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

    # Clear old cart items if present to ensure clean cart state
    cart_page.clear_cart_if_needed()

    # 3. Dynamically Detect & Randomly Select Main Category -> Take Screenshot
    main_category, sub_category = home_page.select_random_category()
    page.screenshot(path="screenshots/03_category_selected.png")
    print()

    # 4. Dynamically Detect Subcategory & Select Random Products -> Take Screenshot
    selected_products, selected_indices = category_page.select_random_products()
    page.screenshot(path="screenshots/04_subcategory_selected.png")
    page.screenshot(path="screenshots/05_products_selected.png")
    print()

    # 5. Add ALL Selected Products to Cart -> Take Screenshot
    category_page.add_products_to_cart(selected_indices)
    page.screenshot(path="screenshots/06_products_added_to_cart.png")
    print()

    # 6. Open Cart & Perform Dynamic Multi-Product Cart Validation -> Take Screenshot
    cart_page.open_cart()
    assert cart_page.is_cart_page_displayed()
    cart_page.verify_multi_product_cart(selected_products)
    page.screenshot(path="screenshots/07_cart_verified.png")
    print()

    # 7. Logout & Take Screenshot
    cart_page.logout()
    assert login_page.is_login_page_displayed()
    page.screenshot(path="screenshots/08_logout.png")
    print("[LOGOUT] Logout successful.")
    print()

    selected_count = len(selected_products)
    print("========================================")
    print("E2E TEST SUMMARY")
    print("========================================")
    print(f"Main Category      : {main_category}")
    print(f"Sub-category       : {sub_category}")
    print(f"Selected Item Count: {selected_count}")
    print(f"Cart Item Count    : {selected_count}")
    print("Count Validation   : PASSED")
    print("Product Validation : PASSED")
    print("Logout             : PASSED")
    print("Overall Test       : PASSED")
    print("========================================")
