# pages/login_page.py
# Page Object for Login Page supporting positive and negative testing.

from playwright.sync_api import expect

class LoginPage:

    def __init__(self, page):
        self.page = page
        self.login_heading = page.locator("h2:has-text('Login to your account')")
        self.email_input = page.locator("[data-qa='login-email']")
        self.password_input = page.locator("[data-qa='login-password']")
        self.login_button = page.locator("[data-qa='login-button']")
        self.error_message = page.locator("p:has-text('Your email or password is incorrect!')")

    def navigate(self, base_url):
        self.page.goto(f"{base_url}/login", wait_until="domcontentloaded")
        assert "Automation Exercise" in self.page.title(), "Website failed to launch properly!"

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def is_login_page_displayed(self):
        return self.login_heading.is_visible()

    def is_login_error_visible(self):
        """Verifies if the login error message is visible for negative test cases."""
        expect(self.error_message).to_be_visible()
        return self.error_message.is_visible()
