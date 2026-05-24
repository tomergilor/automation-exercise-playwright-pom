from pathlib import Path
from playwright.sync_api import Page

class ScreenshotHelper:
    def __init__(self, base_dir: str = "artifacts/screenshots"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def take(self, page: Page, name: str) -> Path:
        safe_name = name.replace(" ", "_").replace("/", "_")
        path = self.base_dir / f"{safe_name}.png"
        page.screenshot(path=str(path), full_page=True)
        return path
