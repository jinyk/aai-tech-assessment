"""Download the five papers in docs/papers/ again from arXiv."""

import urllib.request
from pathlib import Path

PAPERS = {
    "2210.03629v3": "react.pdf",
    "2302.04761v1": "toolformer.pdf",
    "2303.11366v4": "reflexion.pdf",
    "2304.03442v2": "generative-agents.pdf",
    "2308.11432v7": "agent-survey.pdf",
}

OUT = Path(__file__).parent / "docs" / "papers"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for arxiv_id, name in PAPERS.items():
        target = OUT / name
        if target.exists():
            print(f"skip {name} (already here)")
            continue
        url = f"https://arxiv.org/pdf/{arxiv_id}"
        request = urllib.request.Request(url, headers={"User-Agent": "paper-chat/0.1"})
        with urllib.request.urlopen(request) as response:
            target.write_bytes(response.read())
        print(f"saved {name} ({target.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
