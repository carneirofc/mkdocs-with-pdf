import logging

from mkdocs.config import config_options as c, Config
from mkdocs.config.defaults import MkDocsConfig

from .drivers.event_hook import EventHookHandler
from .drivers.headless_chrome import HeadlessChromeDriver
from .templates.template import Template


class Options(Config):
    author = c.Optional(c.Type(str, default=None))
    back_cover = c.Type(bool, default=False)
    convert_iframe = c.Type(list, default=[])
    copyright = c.Optional(c.Type(str, default=None))
    cover = c.Type(bool, default=True)
    cover_logo = c.Type(str, default=None)
    cover_subtitle = c.Type(str, default=None)
    cover_title = c.Optional(c.Type(str, default=None))
    custom_template_path = c.Type(str, default="templates")
    debug_html = c.Type(bool, default=False)
    debug_html_path = c.Type(str, default=None)
    enabled_if_env = c.Type(str)
    exclude_pages = c.Type(list, default=[])
    excludes_children = c.Type(list, default=[])
    heading_shift = c.Type(bool, default=True)
    headless_chrome_path = c.Type(str, default="chromium-browser")
    ordered_chapter_level = c.Type(int, default=3)
    output_path = c.Type(str, default="pdf/document.pdf")
    show_anchors = c.Type(bool, default=False)
    theme_handler_path = c.Optional(c.Type(str, default=None))
    toc_level = c.Type(int, default=2)
    toc_title = c.Type(str, default="Table of contents")
    two_columns_level = c.Type(int, default=0)
    verbose = c.Type(bool, default=False)
    strict = c.Type(bool, default=False)

    _mkdocs_config: MkDocsConfig | None = None
    _hook: EventHookHandler | None = None
    _template: Template | None = None
    _logger: logging.Logger | None = None
    js_renderer: HeadlessChromeDriver | None = None
    theme_name: str | None = None

    def use_mkdocs_configs(self, mkdocs_config: MkDocsConfig, logger: logging.Logger):
        self._mkdocs_config = mkdocs_config
        if not self.author:
            self.author = mkdocs_config.site_author or "Unknown"

        if not self.copyright:
            self.copyright = mkdocs_config.copyright or "Unknown"

        if not self.cover_title:
            self.cover_title = mkdocs_config.site_name

        if not self._logger:
            self._logger = logger

        if not self.js_renderer:
            self.js_renderer = HeadlessChromeDriver.setup(
                self.headless_chrome_path, logger
            )

        if not self.theme_name:
            self.theme_name = mkdocs_config.theme.name

        if not self.theme_handler_path:
            self.theme_handler_path = mkdocs_config.get("theme_handler_path", None)

        # Template handler(Jinja2 wrapper)
        self._template = Template(self, mkdocs_config)

        self._hook = EventHookHandler(self, mkdocs_config, logger=logger)

    @property
    def logger(self) -> logging.Logger | None:
        return self._logger

    @property
    def template(self) -> Template | None:
        return self._template

    @property
    def hook(self) -> EventHookHandler | None:
        return self._hook
