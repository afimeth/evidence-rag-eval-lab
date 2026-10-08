# Evidence RAG Evaluation Lab

A small, runnable evidence fixture for **Applied AI / RAG / AI Platform** review. Standard-library Python 3.11+; no API key, installation, or external service required.

## Run in under a minute

```sh
git clone https://github.com/afimeth/evidence-rag-eval-lab.git
cd evidence-rag-eval-lab
python -m unittest discover -s tests -v
python app.py
```

The demo uses synthetic inputs and prints JSON. Tests fail with a nonzero exit code. The runtime demo creates and removes a temporary SQLite database; other demos operate in memory.

## Headless click-to-run contract

`python app.py` is the runtime entrypoint. Treat it as the headless equivalent of a click-to-run action: one invocation executes the fixture and returns machine-readable evidence.

No UI is required or shipped. Any UI may wrap this runtime later; the evaluator-facing contract is the input, output, evidence binding, and limitation surface.

## What this demonstrates

Built a deterministic retrieval evaluation harness with extractive citations, source digest verification, abstention fixtures, and adversarial citation tests.

Flow: `Query -> lexical rank -> extractive citations -> binding verification -> eval receipt`.

See [architecture](docs/ARCHITECTURE.md), [contracts](docs/CONTRACTS.md), [evidence and limitations](docs/EVIDENCE.md), and [demo walkthrough](docs/DEMO.md).

## Boundaries

No embeddings, reranker, LLM generation, vector database, production corpus, semantic entailment, prompt injection defense, or latency/scale benchmark. Toy English fixtures are not a real-world accuracy estimate. A matching citation does not prove source truth or answer relevance.

This is a fixture implementation, not a production service or an accepted release of its source project. CI results and local measurements are separate evidence.

## Provenance

The implementation is a fresh, standalone educational distillation of inspected private runtime contracts. No private source files, customer data, credentials, topology, or private project identifiers are included. The private source manifest is retained outside this public repository. No license is assigned to the original private sources; this repository grants no rights to them.

## Extension boundary

Describe the failure boundary, run the denial/adversarial tests, and state what new evidence would be needed before production use. Add live retrieval/model components only when their outputs can remain inspectable and separately measured.
