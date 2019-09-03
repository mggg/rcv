from rcv.candidate import Candidate


class TestCandidate:
    def test_can_create(self, candidate):
        assert candidate

    def test_has_repr(self, candidate):
        assert repr(candidate) == "<Candidate Amy with 15 votes>"

    def test_str_is_name(self, candidate):
        assert str(candidate) == "Amy"

    # def test_hash_by_name(self, candidate):
    # assert hash(candidate) == hash("Amy")

    def test_name_is_str(self):
        assert Candidate(10).name == "10"
