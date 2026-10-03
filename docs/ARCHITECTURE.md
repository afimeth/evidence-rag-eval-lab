# Architecture

`Query -> lexical rank -> extractive citations -> binding verification -> eval receipt`

`app.py` contains the complete executable path. `tests/test_app.py` exercises success and refusal paths. Fixtures are synthetic. The CI matrix runs unit tests and demo on Linux/Windows and Python 3.11/3.14.

## Design and tradeoffs

Top-2 ranked by shared token count, then document ID. Zero overlap abstains. Each citation contains complete document text and its SHA256. Verification checks byte/text binding only; retrieval evaluation separately checks relevance labels.

The small implementation favors an inspectable boundary over breadth. No external dependency or remote execution participates in the demo.

## Operational limitations

No embeddings, reranker, LLM generation, vector database, production corpus, semantic entailment, prompt injection defense, or latency/scale benchmark. Toy English fixtures are not a real-world accuracy estimate. A matching citation does not prove source truth or answer relevance.
