# pages/cart_page.py
# Page Object for Shopping Cart Page (multi-product cart validation & verification).

import re
from playwright.sync_api import expect

def clean_text(text):
    text = text.replace('\xa0', ' ').replace('–', '-').replace('—', '-')
    suffixes = [
        r'Browse Designer Clothes$',
        r'Browse Digital Magazines$',
        r'Industrial & Product Design$',
        r'Apparel$',
        r'Dresses$',
        r'Dress$',
        r'Tops & Shirts$',
        r'Tops$',
        r'Tshirts$',
        r'Jeans$',
        r'Saree$',
        r'Women$',
        r'Men$',
        r'Kids$'
    ]
    for pattern in suffixes:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()

class CartPage:

    def __init__(self, page):
        self.page = page
        self.cart_table = page.locator("#cart_info")
        self.cart_item = page.locator("td.cart_description a")
        self.cart_price = page.locator("td.cart_price p")
        self.cart_quantity = page.locator("td.cart_quantity button")
        self.delete_buttons = page.locator("td.cart_quantity_delete a")
        self.logout_link = page.locator("a[href='/logout']")

    def open_cart(self):
        """Navigates directly to the Shopping Cart page."""
        self.page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded")

    def is_cart_page_displayed(self):
        expect(self.cart_table).to_be_visible()
        return "view_cart" in self.page.url

    def clear_cart_if_needed(self):
        """Empties the cart if any old items exist before starting the test."""
        self.open_cart()
        self.page.wait_for_selector("#cart_info, #empty_cart", timeout=10000)
        
        # Loop until no item rows remain
        for _ in range(3):
            del_btns = self.page.locator(".cart_quantity_delete")
            if del_btns.count() == 0:
                break

            while del_btns.count() > 0:
                try:
                    with self.page.expect_response(re.compile(r".*delete_cart.*"), timeout=5000):
                        del_btns.first.click()
                except Exception:
                    pass
                self.page.wait_for_timeout(500)

            # Reload to double check server state
            self.page.reload(wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)

        # Return to home page
        self.page.goto("https://automationexercise.com", wait_until="domcontentloaded")

    def verify_multi_product_cart(self, selected_products):
        """
        Dynamically counts products in cart, compares actual cart count with expected count,
        and verifies that every selected product name is present in the cart.
        """
        expect(self.cart_item.first).to_be_visible()
        expect(self.cart_price.first).to_be_visible()
        expect(self.cart_quantity.first).to_be_visible()

        count = self.cart_item.count()
        cart_product_titles = [clean_text(self.cart_item.nth(i).inner_text()) for i in range(count)]

        expected_count = len(selected_products)
        actual_cart_count = len(cart_product_titles)

        print(f"[VERIFY CART] Expected Items: {expected_count}")
        print(f"[VERIFY CART] Actual Cart Items: {actual_cart_count}")

        # Assert count match
        assert actual_cart_count == expected_count, (
            f"Expected {expected_count} products in cart, "
            f"but found {actual_cart_count}."
        )

        # Assert product names presence
        for product in selected_products:
            expected_clean = clean_text(product).lower()
            found = any(expected_clean in item.lower() or item.lower() in expected_clean for item in cart_product_titles)
            assert found, f"Selected product '{product}' was missing from cart items: {cart_product_titles}"

        print("[VERIFY PRODUCTS] All selected products are present in cart.")

    def logout(self):
        expect(self.logout_link).to_be_visible()
        self.logout_link.click()
