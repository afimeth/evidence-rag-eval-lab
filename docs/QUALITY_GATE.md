# Retrieval quality gate — 15 October 2026

The v2 evaluation separates recall, precision among returned citations, citation-byte binding and answerability/abstention. A fixture passes only when it retrieves all labeled relevant documents with no extra irrelevant citation and valid binding, or correctly abstains on an unanswerable case. Unknown gold IDs fail configuration validation. Duplicate citations fail binding verification.

`retrieved_precision` uses the number of returned citations as its denominator (at most two), not a fixed denominator of two. With no retrieved citation it is null; correct abstention is evaluated separately. `recall_at_2` remains null for cases with no relevant documents.

The adversarial policy/concert fixture deliberately has recall 1.0, valid source bytes and precision 0.5. Its evaluation must fail. A passing unit test verifies that this bad retrieval is detected; it does not mean the retriever answered that case correctly.

The deterministic retriever and original fixtures have not been tuned to remove this known failure. Semantic entailment is explicitly unmeasured, not inferred from source hashes or labels. These synthetic tests are not an independent real-world benchmark. Historical evidence files are unchanged.

Run `python -m unittest discover -s tests -v` and `python app.py` from the repository root. The existing CI discovers both the original suite and `tests/test_quality.py`.
