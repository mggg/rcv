import pandas

import pytest
from rcv import PreferenceSchedule
from rcv.ballot import Ballot, BallotSet
from rcv.candidate import Candidate


@pytest.fixture
def items():
    return [
        ("Amy", "Elizabeth", "Kamala"),
        ("Amy", "Elizabeth", "Kamala"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Kamala", "Elizabeth", "Amy"),
        ("Kamala", "Elizabeth", "Amy"),
    ]


@pytest.fixture
def dataframe(items):
    return pandas.DataFrame(items)


@pytest.fixture
def schedule(dataframe):
    return PreferenceSchedule.from_dataframe(dataframe)


@pytest.fixture
def ballot():
    return Ballot(("Kamala", "Elizabeth", "Amy"))


@pytest.fixture
def ballot_set(items):
    return BallotSet.from_items(items)


@pytest.fixture
def candidate():
    ballots = BallotSet([(("Amy", "Elizabeth", "Kamala"), 10), (("Amy", "Kamala"), 5)])
    amy = Candidate("Amy", ballots)
    return amy


@pytest.fixture
def candidates():
    amy = Candidate(
        "Amy", [(("Amy", "Elizabeth", "Kamala"), 20), (("Amy", "Kamala"), 5)]
    )
    kamala = Candidate(
        "Kamala", [(("Kamala",), 10), (("Kamala", "Elizabeth", "Amy"), 10)]
    )
    elizabeth = Candidate(
        "Elizabeth", [(("Elizabeth", "Amy"), 12), (("Elizabeth", "Kamala", "Amy"), 4)]
    )
    return {amy, kamala, elizabeth}


@pytest.fixture
def ballots():
    ballots = BallotSet(
        {
            (("Amy", "Elizabeth", "Kamala"), 20),
            (("Amy", "Kamala"), 5),
            (("Kamala",), 10),
            (("Kamala", "Elizabeth", "Amy"), 10),
            (("Elizabeth", "Amy"), 12),
            (("Elizabeth", "Kamala", "Amy"), 4),
        }
    )
    return ballots


@pytest.fixture
def real_ballots():
    return BallotSet(
        [
            ((87, 402, 396), 1),
            ((393,), 10),
            ((393, 394, 397), 1),
            ((393, 394, 402), 1),
            ((393, 397), 1),
            ((393, 397, 399), 2),
            ((393, 397, 402), 5),
            ((393, 399), 2),
            ((393, 399, 395), 1),
            ((393, 399, 396), 1),
            ((393, 399, 397), 4),
            ((393, 399, 400), 3),
            ((393, 399, 402), 1),
            ((393, 402, 395), 2),
            ((393, 402, 397), 3),
            ((393, 402, 399), 1),
            ((394, 395), 1),
            ((396, 397, 402), 1),
            ((397,), 1),
            ((397, 393), 1),
            ((397, 393, 399), 1),
            ((397, 393, 400), 1),
            ((397, 398, 394), 1),
            ((397, 399, 395), 1),
            ((397, 399, 402), 4),
            ((397, 402, 393), 3),
            ((397, 402, 399), 1),
            ((397, 402, 401), 1),
            ((398,), 2),
            ((398, 394, 393), 1),
            ((398, 395, 396), 1),
            ((398, 399), 2),
            ((399, 393, 397), 1),
            ((399, 394, 400), 1),
            ((399, 395, 393), 1),
            ((399, 395, 397), 3),
            ((399, 395, 402), 2),
            ((399, 397, 395), 1),
            ((399, 397, 402), 4),
            ((399, 400, 396), 1),
            ((399, 401, 398), 1),
            ((399, 402, 393), 3),
            ((399, 402, 397), 3),
            ((400, 393, 397), 1),
            ((400, 394, 393), 1),
            ((402,), 1),
            ((402, 393), 1),
            ((402, 393, 397), 1),
            ((402, 393, 399), 4),
            ((402, 395, 399), 1),
            ((402, 397, 87), 1),
            ((402, 397, 399), 1),
            ((402, 397, 401), 1),
            ((402, 399, 393), 1),
            ((402, 399, 395), 2),
            ((402, 399, 397), 2),
        ]
    )
