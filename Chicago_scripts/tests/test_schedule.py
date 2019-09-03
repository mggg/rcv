from numbers import Number

import pandas

from rcv import PreferenceSchedule
from rcv.schedule import normalize_preferences
from rcv.ballot import Ballot
from rcv.candidate import Candidate


class TestPreferenceSchedule:
    def test_create_from_dataframe(self, dataframe):
        schedule = PreferenceSchedule.from_dataframe(dataframe)
        assert schedule

    def test_preferences_are_weighted_ballots(self, schedule):
        assert all(
            isinstance(ballot, Ballot) and isinstance(weight, Number)
            for ballot, weight in schedule
        )

    def test_gives_expected_counts(self, schedule):
        assert set(schedule) == {
            (Ballot(("Amy", "Elizabeth", "Kamala")), 2),
            (Ballot(("Elizabeth", "Kamala", "Amy")), 4),
            (Ballot(("Kamala", "Elizabeth", "Amy")), 2),
        }

    def test_eliminate(self, ballots):
        amy = Candidate("Amy")
        kamala = Candidate("Kamala")
        elizabeth = Candidate("Elizabeth")

        schedule = PreferenceSchedule(ballots, candidates={amy, kamala, elizabeth})
        schedule.eliminate(elizabeth)
        for candidate in schedule.candidates:
            for ballot, weight in candidate.votes:
                assert str(elizabeth) not in ballot


class TestNormalizePreferences:
    def test_removes_duplicates(self):
        prefs = ["A", "A", "B"]
        result = normalize_preferences(prefs)
        assert result == ["A", "B"]

    def test_skips_falsy_values(self):
        assert normalize_preferences([None, None, "Amy", 0]) == ["Amy"]

    def test_can_normalize_a_dataframe(self):
        df = pandas.DataFrame(
            {
                "first": [None, "Amy", "Amy", "Kamala"],
                "second": ["Elizabeth", "Elizabeth", "Amy", "Amy"],
                "third": ["Kamala", "Kamala", "Elizabeth", "Elizabeth"],
            }
        )
        schedule = PreferenceSchedule.from_dataframe(df)
        assert set(schedule) == {
            (("Elizabeth", "Kamala"), 1),
            (("Amy", "Elizabeth", "Kamala"), 1),
            (("Amy", "Elizabeth"), 1),
            (("Kamala", "Amy", "Elizabeth"), 1),
        }

    def test_from_ballotS(self):
        schedule = PreferenceSchedule.from_ballots(
            [
                ("Kamala", "Elizabeth", "Amy"),
                ("Kirsten", "Elizabeth"),
                ("Kamala", "Elizabeth", "Amy"),
                ("Amy", "Elizabeth", "Kirsten"),
            ]
        )
        assert schedule is not None

    def test_repr(self, schedule):
        assert repr(schedule) == "<PreferenceSchedule total_votes=8>"
