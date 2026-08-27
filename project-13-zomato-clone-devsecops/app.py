"""Local-only teaching helper for project-13-zomato-clone-devsecops.

This reconstructed module contains no remote service, cloud credential, or deployment
behavior. It is intentionally deterministic for classroom evidence.
"""
from __future__ import annotations


def local_status() -> dict[str, str]:
    return {"project": "project-13-zomato-clone-devsecops", "mode": "local-first", "status": "ready-for-local-validation"}


if __name__ == "__main__":
    print(local_status())
