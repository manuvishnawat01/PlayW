# pages/product_page.py
# Page Object for Product Details Page.

import re
from playwright.sync_api import expect

def clean_text(text):
    text = text.replace('\xa0', ' ').replace('–', '-').replace('—', '-')
    text = re.sub(r'Apparel$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Browse Digital Magazines$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Dresses$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Industrial & Product Design$', '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()

class ProductPage:

    def __init__(self, page):
        self.page = page
        self.product_name = page.locator(".product-information h2")
        self.product_price = page.locator(".product-information span span")
        self.add_to_cart_button = page.locator("button.cart")
        self.cart_modal = page.locator("#cartModal")
        self.view_cart_link = page.locator("#cartModal a[href='/view_cart']")

    def get_product_name(self):
        expect(self.product_name).to_be_visible()
        expect(self.product_price).to_be_visible()
        return clean_text(self.product_name.inner_text())

    def add_to_cart(self, product_name=None):
        expect(self.add_to_cart_button).to_be_visible()
        self.add_to_cart_button.click()
        # Assert confirmation modal appears
        expect(self.cart_modal).to_be_visible()
        expect(self.view_cart_link).to_be_visible()
        if product_name:
            print(f"[ADD TO CART] Product '{product_name}' added to cart.")

    def open_cart(self):
        expect(self.view_cart_link).to_be_visible()
        self.view_cart_link.click()
