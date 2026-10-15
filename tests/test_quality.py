import copy
import unittest
from unittest.mock import patch
from app import answer, evaluate, verify


class QualityRegressions(unittest.TestCase):
    def setUp(self):
        self.docs = [{'id': 'policy', 'text': 'Release policy requires review.'},
                     {'id': 'concert', 'text': 'Release concert tickets today.'}]

    def score(self, query='release', relevant=None):
        return evaluate(self.docs, [{'id': 'case', 'query': query,
                                    'relevant': ['policy'] if relevant is None else relevant}])

    def test_valid_irrelevant_citation_fails_quality_not_binding(self):
        report = self.score()
        row = report['cases'][0]
        self.assertTrue(row['citation_valid'])
        self.assertEqual(row['recall_at_2'], 1.0)
        self.assertEqual(row['retrieved_precision'], 0.5)
        self.assertFalse(row['retrieval_passed'])
        self.assertFalse(row['passed'])
        self.assertEqual(report['passed'], 0)
        self.assertIsNone(row['semantic_entailment_verified'])

    def test_all_and_only_relevant_passes(self):
        report = self.score('policy')
        self.assertEqual(report['passed'], 1)
        self.assertEqual(report['cases'][0]['retrieved_precision'], 1.0)

    def test_two_relevant_pass(self):
        self.assertEqual(self.score(relevant=['policy', 'concert'])['passed'], 1)

    def test_missing_relevant_fails(self):
        report = self.score('concert', ['policy', 'concert'])
        self.assertEqual(report['cases'][0]['recall_at_2'], 0.5)
        self.assertEqual(report['passed'], 0)

    def test_correct_abstention_has_no_fake_precision(self):
        row = self.score('quasar', [])['cases'][0]
        self.assertTrue(row['abstention_correct'])
        self.assertTrue(row['passed'])
        self.assertIsNone(row['retrieved_precision'])
        self.assertIsNone(row['recall_at_2'])

    def test_answer_to_unanswerable_case_fails(self):
        row = self.score('release', [])['cases'][0]
        self.assertFalse(row['abstention_correct'])
        self.assertFalse(row['answerability_correct'])
        self.assertFalse(row['passed'])

    def test_duplicate_citations_are_not_extra_evidence(self):
        result = answer('policy', self.docs)
        result['citations'].append(copy.deepcopy(result['citations'][0]))
        self.assertFalse(verify(result, self.docs))
        with patch('app.answer', return_value=result):
            self.assertEqual(self.score('policy')['passed'], 0)

    def test_valid_relevance_with_tampered_quote_fails(self):
        result = answer('policy', self.docs)
        result['citations'][0]['quote'] = 'fabricated'
        with patch('app.answer', return_value=result):
            row = self.score('policy')['cases'][0]
        self.assertTrue(row['retrieval_passed'])
        self.assertFalse(row['citation_valid'])
        self.assertFalse(row['passed'])

    def test_unknown_gold_label_is_configuration_error(self):
        with self.assertRaisesRegex(ValueError, 'UNKNOWN_RELEVANCE_LABEL'):
            self.score(relevant=['missing'])

    def test_invalid_citation_identifier_is_rejected(self):
        result = answer('policy', self.docs)
        result['citations'][0]['document_id'] = []
        self.assertFalse(verify(result, self.docs))


if __name__ == '__main__':
    unittest.main()
