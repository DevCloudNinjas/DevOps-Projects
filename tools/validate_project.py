"""CLI wrapper for validating one repository project."""

from __future__ import annotations

import sys

from tools.project_inventory import validate_main


if __name__ == "__main__":
    sys.exit(validate_main())
