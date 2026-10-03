import copy, unittest
from app import answer, evaluate, retrieve, verify

class Tests(unittest.TestCase):
    def setUp(self): self.docs = [{'id': 'a', 'text': 'Dispatch uncertainty requires hold.'}, {'id': 'b', 'text': 'Citation binds exact source bytes.'}]
    def test_relevant(self): self.assertEqual(retrieve('dispatch', self.docs)[0]['id'], 'a')
    def test_abstain(self): self.assertEqual(answer('bananas', self.docs)['status'], 'ABSTAIN')
    def test_citation_valid(self): self.assertTrue(verify(answer('citation', self.docs), self.docs))
    def test_fabricated_quote(self):
        r = answer('citation', self.docs); r['citations'][0]['quote'] = 'invented'
        self.assertFalse(verify(r, self.docs))
    def test_modified_source(self):
        r = answer('dispatch', self.docs); self.docs[0]['text'] += ' changed'
        self.assertFalse(verify(r, self.docs))
    def test_unknown_source(self):
        r = answer('dispatch', self.docs); r['citations'][0]['document_id'] = 'missing'
        self.assertFalse(verify(r, self.docs))
    def test_false_abstention(self):
        r = answer('dispatch', self.docs); r['status'] = 'ABSTAIN'
        self.assertFalse(verify(r, self.docs))
    def test_duplicate_id(self):
        with self.assertRaises(ValueError): retrieve('x', self.docs + [self.docs[0]])
    def test_eval_catches_missed_relevance(self):
        r = evaluate(self.docs, [{'id': 'miss', 'query': 'banana', 'relevant': ['a']}])
        self.assertEqual(r['passed'], 0)
    def test_ties_deterministic(self):
        docs = [{'id': 'z', 'text': 'same'}, {'id': 'a', 'text': 'same'}]
        self.assertEqual(retrieve('same', docs, 1)[0]['id'], 'a')
    def test_empty_eval(self):
        with self.assertRaises(ValueError): evaluate(self.docs, [])
