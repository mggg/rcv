from rcv.ballot import Ballot, BallotSet


class TestBallot:
    def test_implements_repr(self, ballot):
        assert repr(ballot) == "<Ballot (Kamala, Elizabeth, Amy)>"

    def test_can_eliminate_candidate(self, ballot):
        ballot.eliminate("Kamala")
        return ballot == Ballot(("Elizabeth", "Amy"))

    def test_has_top_choice_property(self, ballot):
        assert ballot.top_choice == "Kamala"

    def test_has_is_empty_property(self, ballot):
        assert ballot.is_empty is False
        assert Ballot().is_empty is True

    def test_has_next_choice_property(self, ballot):
        assert ballot.next_choice == "Elizabeth"

    def test_top_choice_is_none_for_empty_ballot(self):
        assert Ballot().top_choice is None

    def test_next_choice_is_none_for_ballots_with_one_name(self):
        assert Ballot(["Kamala"]).next_choice is None


class TestBallotSet:
    def test_can_eliminate_candidate(self, ballot_set):
        assert any("Amy" in ballot for ballot, weight in ballot_set)

        eliminated = ballot_set.eliminate("Amy")

        for ballot, weight in eliminated:
            assert "Amy" not in ballot

    def test_can_be_instantiated_empty(self):
        assert BallotSet() is not None

    def test_has_repr_method(self, ballot_set):
        assert repr(ballot_set) == (
            "<BallotSet {"
            "2 * <Ballot (Amy, Elizabeth, Kamala)>, "
            "4 * <Ballot (Elizabeth, Kamala, Amy)>, "
            "2 * <Ballot (Kamala, Elizabeth, Amy)>"
            "}>"
        )

    def test_has_weight_type_argument(self):
        weighted_set = BallotSet([(("a",), 40), (("b",), 60)], weight_type=float)
        assert all(isinstance(weight, float) for item, weight in weighted_set)
