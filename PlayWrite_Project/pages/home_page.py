# pages/home_page.py
# Page Object for Home Page & Header Navigation (dynamic category detection & selection).

import re
import random
from playwright.sync_api import expect

def clean_category_name(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).strip()
    return text.title()

def clean_subcategory_name(text):
    return re.sub(r'\s+', ' ', text).strip().title()

class HomePage:

    def __init__(self, page):
        self.page = page
        self.logged_in_text = page.locator("a:has-text('Logged in as')")
        self.logout_link = page.locator("a[href='/logout']")
        # Locator for main category panel header links (e.g. Women, Men, Kids)
        self.main_category_links = page.locator("#accordian .panel-heading a")

    def is_logged_in(self):
        expect(self.logged_in_text).to_be_visible()
        return self.logged_in_text.is_visible()

    def select_random_category(self):
        """
        Dynamically detects main categories (Women, Men, Kids),
        randomly selects ONE main category via nth(random_index),
        clicks to expand ONLY that main category,
        dynamically locates subcategories belonging ONLY to that expanded category,
        randomly selects ONE subcategory via nth(random_index),
        prints formatted logs, and opens the subcategory.
        """
        expect(self.main_category_links.first).to_be_attached()
        
        main_count = self.main_category_links.count()
        assert main_count > 0, "No main category panel links found on the page!"

        # Use OS-level entropy (SystemRandom) for true random index selection
        sys_rand = random.SystemRandom()
        random_main_index = sys_rand.randint(0, main_count - 1)
        selected_main_element = self.main_category_links.nth(random_main_index)
        
        # Read and store Main Category name
        raw_main_name = selected_main_element.inner_text()
        main_category_name = clean_category_name(raw_main_name)
        target_id = selected_main_element.get_attribute("href")  # e.g. '#Women', '#Men', '#Kids'

        print(f"[SELECTED CATEGORY] {main_category_name}")

        # 2. Expand ONLY the selected main category
        selected_main_element.scroll_into_view_if_needed()
        selected_main_element.click()

        # Handle potential Google Vignette ad overlay redirect on Automation Exercise
        if "google_vignette" in self.page.url:
            self.page.goto("https://automationexercise.com", wait_until="domcontentloaded")
            self.page.wait_for_selector("#accordian")
            selected_main_element = self.main_category_links.nth(random_main_index)
            selected_main_element.click()

        # 3. Locate subcategories belonging ONLY to this expanded main category
        sub_category_links = self.page.locator(f"{target_id} .panel-body a")
        
        # If not visible immediately due to vignette or animation delay, re-trigger expand
        try:
            expect(sub_category_links.first).to_be_visible(timeout=5000)
        except AssertionError:
            if "google_vignette" in self.page.url:
                self.page.goto("https://automationexercise.com", wait_until="domcontentloaded")
                self.page.wait_for_selector("#accordian")
            selected_main_element = self.main_category_links.nth(random_main_index)
            selected_main_element.click()
            expect(sub_category_links.first).to_be_visible(timeout=10000)

        sub_count = sub_category_links.count()
        assert sub_count > 0, f"No subcategories found under expanded main category '{main_category_name}'!"

        # 4. Randomly select ONE subcategory element via SystemRandom
        random_sub_index = sys_rand.randint(0, sub_count - 1)
        selected_sub_element = sub_category_links.nth(random_sub_index)

        # Read and store Sub-category name
        raw_sub_name = selected_sub_element.inner_text()
        sub_category_name = clean_subcategory_name(raw_sub_name)

        print(f"[SELECTED SUBCATEGORY] {sub_category_name}")

        # 5. Open the selected subcategory
        sub_href = selected_sub_element.get_attribute("href")
        self.page.goto(f"https://automationexercise.com{sub_href}", wait_until="domcontentloaded")
        assert "category_products" in self.page.url, f"Failed to navigate to subcategory page for '{sub_category_name}'!"

        return main_category_name, sub_category_name

    def logout(self):
        expect(self.logout_link).to_be_visible()
        self.logout_link.click()
