import os
import base64
from . import _FilterBase


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
            path = os.path.abspath(os.path.join(d, pathname))

            if os.path.isfile(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")

        raise FileNotFoundError(f"Image file not found: {pathname}")
