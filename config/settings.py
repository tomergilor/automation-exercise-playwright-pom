import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()

def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://automationexercise.com")
    browser: str = os.getenv("BROWSER", "chromium")
    browser_channel: str | None = os.getenv("BROWSER_CHANNEL") or None
    headless: bool = parse_bool(os.getenv("HEADLESS", "false"))
    timeout_ms: int = int(os.getenv("TIMEOUT_MS", "30000"))
    user_email: str = os.getenv("USER_EMAIL", "test_auto@gmail.com")
    user_password: str = os.getenv("USER_PASSWORD", "Q1w2e3r4")

settings = Settings()
