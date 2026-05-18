"""CLI wrapper for listing repository projects."""

from __future__ import annotations

import sys

from tools.project_inventory import list_main


if __name__ == "__main__":
    sys.exit(list_main())
