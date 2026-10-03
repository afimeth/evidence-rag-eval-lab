# Evidence RAG Evaluation Lab

A small, runnable proof of work for **Applied AI / RAG / AI Platform** interviews. Standard-library Python 3.11+; no API key, installation, or external service required.

## Run in under a minute

```sh
git clone https://github.com/afimeth/evidence-rag-eval-lab.git
cd evidence-rag-eval-lab
python -m unittest discover -s tests -v
python app.py
```

The demo uses synthetic inputs and prints JSON. Tests fail with a nonzero exit code. The runtime demo creates and removes a temporary SQLite database; other demos operate in memory.

## What this demonstrates

Built a deterministic retrieval evaluation harness with extractive citations, source digest verification, abstention fixtures, and adversarial citation tests.

Flow: `Query -> lexical rank -> extractive citations -> binding verification -> eval receipt`.

See [architecture](docs/ARCHITECTURE.md), [contracts](docs/CONTRACTS.md), [evidence and limitations](docs/EVIDENCE.md), and [demo walkthrough](docs/DEMO.md).

## Boundaries

No embeddings, reranker, LLM generation, vector database, production corpus, semantic entailment, prompt injection defense, or latency/scale benchmark. Toy English fixtures are not a real-world accuracy estimate. A matching citation does not prove source truth or answer relevance.

This is an interview laboratory with fixture execution. It is not a production service or an accepted release of its source project. CI results and local measurements are separate evidence.

## Provenance

The implementation is a fresh, standalone educational distillation of inspected private runtime contracts. No private source files, customer data, credentials, topology, or private project identifiers are included. The private source manifest is retained outside this public repository. No license is assigned to the original private sources; this repository grants no rights to them.

## Interview extension

Describe the failure boundary, run the denial/adversarial tests, and explain what new evidence would be needed before production use. Start with a durable audit/identity boundary, then add provider integration and measured operational behavior.
