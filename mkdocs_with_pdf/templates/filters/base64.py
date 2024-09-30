import os
from . import _FilterBase
from ...utils.image_util import convert_image_to_base64


class InlineB64Filter(_FilterBase):
    def __call__(self, pathname: str) -> str:
        if not pathname:
            return ""

        dirs = [
            self.options.custom_template_path,
            getattr(self.config["theme"], "custom_dir", None),
            self.config["docs_dir"],
            ".",
        ]

        for d in dirs:
            if not d:
                continue

            data = convert_image_to_base64(pathname)
            if data:
                return data

        raise FileNotFoundError(f"Image file not found: {pathname}")
