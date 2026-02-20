"""Repo Consolidation — Link & Secret Remediation Pipeline.

CLI pipeline that scans a consolidated DevOps repo for broken URLs,
exposed credentials, hardcoded AWS account IDs, and stale Docker image
names — then fixes them in place and validates the results.
"""

__version__ = "0.1.0"
