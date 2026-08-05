"""Source-tree import shim for running debug modules with ``python -m``.

The distributable package lives under ``src/open_mic_lab``. This namespace path
extension lets repository-root commands such as
``python -m open_mic_lab.debug_labs.chapter_12_improvisation`` work before an
editable install is available.
"""

from pathlib import Path
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]  # noqa: F821
_src_package = Path(__file__).resolve().parent.parent / "src" / "open_mic_lab"
if _src_package.is_dir():
    __path__.append(str(_src_package))  # type: ignore[name-defined]  # noqa: F821
