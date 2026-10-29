"""Build the search index from every PDF in docs/papers/ and data/docs/."""

from app.config import INDEX_DIR, PAPERS_DIR, UPLOADS_DIR
from app.ingest import build_index, get_embeddings


def main() -> None:
    paths = sorted(PAPERS_DIR.glob("*.pdf")) + sorted(UPLOADS_DIR.glob("*.pdf"))
    if not paths:
        raise SystemExit(f"No PDFs found in {PAPERS_DIR}. Run: uv run fetch_papers.py")
    index = build_index(paths, get_embeddings())
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index.save_local(str(INDEX_DIR))
    print(f"Indexed {len(paths)} files, {index.index.ntotal} chunks, saved to {INDEX_DIR}")


if __name__ == "__main__":
    main()
