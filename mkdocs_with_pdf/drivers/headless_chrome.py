import playwright
import playwright.sync_api

from logging import Logger
from shutil import which


class HeadlessChromeDriver(object):
    """'Headless Chrome' executor"""

    @classmethod
    def setup(self, program_path: str, logger: Logger):
        if not which(program_path):
            raise RuntimeError(
                "No such `Headless Chrome` program or not executable"
                + f': "{program_path}".'
            )
        return self(program_path, logger)

    def __init__(self, program_path: str, logger: Logger):
        self._program_path = program_path
        self._logger = logger

    def to_pdf(self, html: str, pdf_path: str) -> None:
        if not html:
            raise RuntimeError("Empty HTML content")
        if not pdf_path:
            raise RuntimeError("Empty PDF path")
        self.render_using_playwright(html, pdf_path)

    def render_using_playwright(self, html: str, pdf_path: str = "") -> str:
        page_html_content = ""
        with playwright.sync_api.sync_playwright() as p:
            browser = p.chromium.launch(
                args=[
                    "--no-sandbox",
                    "--disable-web-security",
                    "--disable-gpu",
                    "--allow-file-access-from-files",
                    "--run-all-compositor-stages-before-draw",
                ],
                executable_path=self._program_path,
                headless=True,
                timeout=60000,
            )
            page = browser.new_page()

            page.emulate_media(media="print", color_scheme="light")

            page.set_content(html, wait_until="domcontentloaded")
            page_html_content = page.content()

            page.wait_for_load_state("networkidle")

            # Wait for all fonts to be loaded
            page.evaluate("document.fonts.ready")

            # Ensure all images are loaded
            page.evaluate("""
                Array.from(document.images).forEach(img => {
                    if (!img.complete) {
                        img.onload = () => {};
                        img.onerror = () => {};
                    }
                });
            """)

            if pdf_path:
                b_written = page.pdf(path=pdf_path)
                if not b_written:
                    raise RuntimeError(f"Failed to write PDF: {pdf_path}")
                self._logger.info(f"PDF generated: {pdf_path} ({len(b_written)} bytes)")
            browser.close()

        return page_html_content

    def render(self, html: str) -> str:
        out = self.render_using_playwright(html)
        if not out:
            raise RuntimeError(f"Failed to render by JS: {out}")
        return out
