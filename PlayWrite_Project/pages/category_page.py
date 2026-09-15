# pages/category_page.py
# Page Object for Category Products Page (dynamic multi-product selection & addition).

import re
import random
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

class CategoryPage:

    def __init__(self, page):
        self.page = page
        self.product_cards = page.locator(".features_items .col-sm-4")
        self.cart_modal = page.locator("#cartModal")
        self.continue_shopping_button = page.locator("#cartModal button.close-modal")

    def select_random_products(self):
        """
        Dynamically detects all product cards in the sub-category,
        randomly generates a count of products to select (1 to min(5, total)),
        picks UNIQUE products using random.sample(), stores names in a list,
        and prints the selection summary.
        """
        expect(self.product_cards.first).to_be_visible()
        available_count = self.product_cards.count()
        assert available_count > 0, "No product cards found in the selected sub-category!"

        # Use OS-level entropy (SystemRandom) for true random count & sample selection
        sys_rand = random.SystemRandom()
        max_to_select = min(5, available_count)
        number_to_select = sys_rand.randint(1, max_to_select)

        # Select unique product indices without duplicates
        selected_indices = sys_rand.sample(range(available_count), number_to_select)

        selected_products = []
        for idx in selected_indices:
            card = self.product_cards.nth(idx)
            name_element = card.locator(".productinfo p")
            expect(name_element).to_be_visible()
            product_name = clean_text(name_element.inner_text())
            selected_products.append(product_name)

        # Print formatted log output
        print(f"[RANDOM COUNT] Number of products selected: {number_to_select}")
        print()
        print("[SELECTED PRODUCTS]")
        for i, name in enumerate(selected_products, start=1):
            print(f"{i}. {name}")

        return selected_products, selected_indices

    def add_products_to_cart(self, selected_indices):
        """
        Loops through all selected product cards, clicks 'Add to cart' on each card,
        handles the confirmation modal by clicking 'Continue Shopping',
        and adds all selected products into the cart.
        """
        for idx in selected_indices:
            card = self.product_cards.nth(idx)
            add_to_cart_btn = card.locator(".productinfo a.add-to-cart")
            
            try:
                with self.page.expect_response(re.compile(r".*add_to_cart.*"), timeout=5000):
                    add_to_cart_btn.click()
            except Exception:
                pass

            # Wait for confirmation modal and click 'Continue Shopping'
            expect(self.cart_modal).to_be_visible()
            self.continue_shopping_button.click()
            self.cart_modal.wait_for(state="hidden")

        print("[ADD TO CART] All selected products added successfully.")
