"""Local-only teaching helper for project-28-openai-chatbot-eks.

This reconstructed module contains no remote service, cloud credential, or deployment
behavior. It is intentionally deterministic for classroom evidence.
"""

from __future__ import annotations


def local_status() -> dict[str, str]:
    return {
        "project": "project-28-openai-chatbot-eks",
        "mode": "local-first",
        "status": "ready-for-local-validation",
    }


if __name__ == "__main__":
    print(local_status())
