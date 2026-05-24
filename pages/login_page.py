from automation_exercise_playwright_pom_simple.config.settings import settings
from automation_exercise_playwright_pom_simple.pages.base_page import BasePage

class LoginPage(BasePage):
    """Authentication page object.
    Handles real user login on Automation Exercise.
    """

    LOGIN_URL = f"{settings.base_url}/login"
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGGED_IN_LINK = "a:has-text('Logged in as')"

    def login(self, email: str = settings.user_email, password: str = settings.user_password) -> None:
        print(f"[auth] logging in as {email}", flush=True)
        self.goto(self.LOGIN_URL)
        self.fill(self.page.locator(self.EMAIL_INPUT), email)
        self.fill(self.page.locator(self.PASSWORD_INPUT), password)
        self.click(self.page.locator(self.LOGIN_BUTTON))
        self.assert_visible(self.page.locator(self.LOGGED_IN_LINK))
