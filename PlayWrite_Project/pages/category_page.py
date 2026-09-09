# pages/category_page.py
# Page Object for Category Products Page (dynamic product detection & selection).

import re
import random
from playwright.sync_api import expect

def clean_text(text):
    text = text.replace('\xa0', ' ').replace('–', '-').replace('—', '-')
    text = re.sub(r'Apparel$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Browse Digital Magazines$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Dresses$', '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()

class CategoryPage:

    def __init__(self, page):
        self.page = page
        # Locator for each product card container in the category
        self.product_cards = page.locator(".features_items .col-sm-4")

    def select_random_product(self):
        """
        Dynamically detects all product cards displayed in the category,
        randomly selects one product card, logs its name, and opens its details page.
        """
        expect(self.product_cards.first).to_be_visible()
        
        # Count available product cards dynamically
        count = self.product_cards.count()
        assert count > 0, "No product cards found in the selected category!"

        # Use OS-level entropy (SystemRandom) for true random index selection
        sys_rand = random.SystemRandom()
        random_index = sys_rand.randint(0, count - 1)
        selected_card = self.product_cards.nth(random_index)

        # Read product title & detail link from the selected card
        name_element = selected_card.locator(".productinfo p")
        link_element = selected_card.locator("a[href*='product_details']")
        
        expect(name_element).to_be_visible()
        selected_product_name = clean_text(name_element.inner_text())
        print(f"[SELECTED PRODUCT] {selected_product_name}")

        # Open product details page
        product_href = link_element.get_attribute("href")
        self.page.goto(f"https://automationexercise.com{product_href}", wait_until="domcontentloaded")
        
        return selected_product_name
