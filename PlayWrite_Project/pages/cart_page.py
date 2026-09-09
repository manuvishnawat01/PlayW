# pages/cart_page.py
# Page Object for Shopping Cart Page.

import re
from playwright.sync_api import expect

def clean_text(text):
    text = text.replace('\xa0', ' ').replace('–', '-').replace('—', '-')
    text = re.sub(r'Apparel$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Browse Digital Magazines$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Dresses$', '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()

class CartPage:

    def __init__(self, page):
        self.page = page
        self.cart_table = page.locator("#cart_info")
        self.cart_item = page.locator("td.cart_description a")
        self.cart_price = page.locator("td.cart_price p")
        self.cart_quantity = page.locator("td.cart_quantity button")
        self.logout_link = page.locator("a[href='/logout']")

    def is_cart_page_displayed(self):
        expect(self.cart_table).to_be_visible()
        return "view_cart" in self.page.url

    def verify_product_in_cart(self, expected_name):
        expect(self.cart_item.first).to_be_visible()
        expect(self.cart_price.first).to_be_visible()
        expect(self.cart_quantity.first).to_be_visible()
        
        count = self.cart_item.count()
        cart_product_titles = [clean_text(self.cart_item.nth(i).inner_text()) for i in range(count)]
        
        print(f"[VERIFY CART] Checking if '{expected_name}' exists in cart...")
        print(f"[VERIFY CART] Cart Products: {cart_product_titles}")
        
        expected_clean = clean_text(expected_name).lower()
        found = any(expected_clean in item.lower() or item.lower() in expected_clean for item in cart_product_titles)
        assert found, f"Expected product '{expected_name}' not found in cart items: {cart_product_titles}"
        
        print(f"[SUCCESS] Verified '{expected_name}' in cart.")

    def logout(self):
        expect(self.logout_link).to_be_visible()
        self.logout_link.click()
