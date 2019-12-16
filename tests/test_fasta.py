import unittest

from io import StringIO

from fqfa.fasta.fasta import yield_fasta_records


class TestYieldFastaRecords(unittest.TestCase):
    def test_empty(self):
        data = StringIO("")

        iterator = yield_fasta_records(data)

        # should return an empty generator
        self.assertRaises(StopIteration, next, iterator)

    def test_noheader(self):
        data = StringIO("ACGT\n")

        iterator = yield_fasta_records(data)

        # should return an empty generator
        self.assertRaises(StopIteration, next, iterator)

    def test_single(self):
        data = StringIO(">seq1\nACGT\n")

        iterator = yield_fasta_records(data)

        self.assertTupleEqual(next(iterator), ("seq1", "ACGT"))
        self.assertRaises(StopIteration, next, iterator)

    def test_multiple(self):
        data = StringIO(">seq1\nACGT\n>seq2\nTGCA\n\n>seq3\nTTTT")

        iterator = yield_fasta_records(data)

        self.assertTupleEqual(next(iterator), ("seq1", "ACGT"))
        self.assertTupleEqual(next(iterator), ("seq2", "TGCA"))
        self.assertTupleEqual(next(iterator), ("seq3", "TTTT"))
        self.assertRaises(StopIteration, next, iterator)

    def test_multiline(self):
        data = StringIO(">seq1\nACGT\nTGCA")

        iterator = yield_fasta_records(data)

        self.assertTupleEqual(next(iterator), ("seq1", "ACGTTGCA"))
        self.assertRaises(StopIteration, next, iterator)


if __name__ == "__main__":
    unittest.main()