# Evidence and limitations

Measured: 2026-10-03T15:55:26.672825+00:00. Python 3.14.7, Windows local execution.

`python -m unittest discover -s tests -v`: **11 passed**, exit 0.
`python app.py`: exit 0. See [test output](../evidence/local-tests.txt) and [demo JSON](../evidence/demo.json).

This is producer-run local validation, not an independent review. GitHub CI is a separate run; inspect Actions for its actual status. No L3/L4 acceptance, live provider evidence or production validation is claimed.

No embeddings, reranker, LLM generation, vector database, production corpus, semantic entailment, prompt injection defense, or latency/scale benchmark. Toy English fixtures are not a real-world accuracy estimate. A matching citation does not prove source truth or answer relevance.

Safe CV claim: "Built a deterministic retrieval evaluation harness with extractive citations, source digest verification, abstention fixtures, and adversarial citation tests."
