"""Deterministic lexical retrieval and extractive citation checks; no LLM."""
import hashlib, json, re
from pathlib import Path

def tokens(text):
    return set(re.findall(r'[a-z0-9]+', text.lower()))

def retrieve(query, corpus, k=2):
    if type(k) is not int or k < 1:
        raise ValueError('K_INVALID')
    if len({d['id'] for d in corpus}) != len(corpus):
        raise ValueError('DUPLICATE_DOCUMENT')
    terms = tokens(query)
    ranked = sorted(((len(terms & tokens(d['text'])), d) for d in corpus), key=lambda x: (-x[0], x[1]['id']))
    return [d for score, d in ranked if score > 0][:k]

def answer(query, corpus):
    hits = retrieve(query, corpus)
    return {'status': 'ANSWERED' if hits else 'ABSTAIN', 'citations': [
        {'document_id': d['id'], 'quote': d['text'], 'sha256': hashlib.sha256(d['text'].encode()).hexdigest()} for d in hits]}

def verify(result, corpus):
    index = {d['id']: d['text'] for d in corpus}
    if len(index) != len(corpus): return False
    if not isinstance(result, dict) or set(result) != {'status', 'citations'}: return False
    citations = result['citations']
    if not isinstance(citations, list): return False
    if result['status'] == 'ABSTAIN': return citations == []
    if result['status'] != 'ANSWERED' or not citations: return False
    seen = set()
    for c in citations:
        if not isinstance(c, dict) or set(c) != {'document_id', 'quote', 'sha256'}: return False
        if not isinstance(c['document_id'], str) or c['document_id'] in seen: return False
        seen.add(c['document_id'])
        text = index.get(c['document_id'])
        if text is None or c['quote'] != text or c['sha256'] != hashlib.sha256(text.encode()).hexdigest(): return False
    return True

def evaluate(corpus, cases):
    if not cases: raise ValueError('EMPTY_EVAL')
    rows = []
    corpus_ids = {d['id'] for d in corpus}
    for c in cases:
        relevant = set(c['relevant'])
        if not relevant <= corpus_ids: raise ValueError('UNKNOWN_RELEVANCE_LABEL')
        result = answer(c['query'], corpus)
        ids = [x['document_id'] for x in result['citations']]
        hits = len(set(ids) & relevant)
        recall = hits / len(relevant) if relevant else None
        # Denominator is returned citations, not fixed k or source validity.
        precision = hits / len(ids) if ids else None
        binding = verify(result, corpus)
        abstained = result['status'] == 'ABSTAIN' and not ids
        quality = abstained if not relevant else recall == 1.0 and precision == 1.0
        rows.append({'id': c['id'], 'retrieved': ids, 'recall_at_2': recall,
                     'retrieved_precision': precision, 'citation_valid': binding,
                     'retrieval_passed': quality,
                     'answerability_correct': (not abstained) == bool(relevant),
                     'abstention_correct': abstained if not relevant else None,
                     'semantic_entailment_verified': None,
                     'passed': quality and binding})
    return {'schema': 'retrieval-evaluation/2', 'cases': rows,
            'passed': sum(r['passed'] for r in rows), 'total': len(rows),
            'precision_definition': 'relevant returned citations / returned citations; at most two; null when none',
            'quality_gate': 'all labeled relevant documents and no irrelevant returned citations, or correct abstention; valid citation binding required',
            'world_truth_verified': False}

if __name__ == '__main__':
    root = Path(__file__).parent
    corpus = json.loads((root / 'fixtures/corpus.json').read_text())
    cases = json.loads((root / 'fixtures/cases.json').read_text())
    result = evaluate(corpus, cases)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] == result['total'] else 1)
