# Contract pack v1

Top-2 ranked by shared token count, then document ID. Zero overlap abstains. Each citation contains complete document text and its SHA256. Verification checks byte/text binding only; retrieval evaluation separately checks relevance labels.

## Interfaces and failure behavior

Read the public functions in `app.py` together with the tests. Invalid admission/task input raises `ValueError`; gateway denial raises `Denied`, runtime replay raises `Blocked`. The eval demo exits 1 if any labelled fixture fails. The other demos demonstrate expected refusals and exit 0 when the walkthrough completes.

## Trust boundary

The host process, code and local data are trusted. Source binding, durable state, and admission are distinct from identity authentication and world verification. No successful return establishes production authority.

## Schema evolution

This v1 lab has no automatic migration. Change the contracts and their rejection tests together; use a new fixture database for incompatible runtime changes.

## Retrieval API and dataset

`retrieve(query: str, corpus: list[dict], k: int = 2)` expects documents with unique string `id` and string `text`. `answer(query, corpus)` returns `{"status": "ANSWERED" | "ABSTAIN", "citations": [...]}`. Each citation contains `document_id`, `quote`, and a UTF-8 source `sha256`.

`verify(result, corpus)` checks full-document extractive bindings; it is not a general arbitrary-object schema validator. Corpus and nested citation scalar types are trusted. `evaluate(corpus, cases)` expects nonempty labelled cases with `id`, `query`, and `relevant` document IDs. A positive case passes only with recall@2 = 1; a negative case passes only with zero citations. Recall is null for negative cases rather than zero. Citation validity must also pass.

The six synthetic labelled cases include one abstention and one two-document query. They are regression fixtures, not held-out evaluation data. Labels do not establish correctness outside this corpus.
