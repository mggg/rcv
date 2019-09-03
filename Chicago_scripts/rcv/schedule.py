from .ballot import BallotSet
from .candidate import Candidate
from .values_dict import ValuesDict


class PreferenceSchedule:
    """A reduced preference schedule.

    The :meth:`from_ballots` method can be useful for creating a preference
    schedule from raw preference orderings:

    >>> PreferenceSchedule.from_ballots([
    ...     ("Amy", "Elizabeth", "Kirsten"),
    ...     ("Amy", "Elizabeth", "Kirsten"),
    ...     ("Amy", "Elizabeth", "Kirsten"),
    ...     ("Kirsten", "Amy"),
    ...     ("Elizabeth", "Kamala", "Kirsten"),
    ...     ("Kamala", "Elizabeth"),
    ...     ("Kamala", "Elizabeth"),
    ...     ("Kamala", "Amy"),
    ...     ("Kamala", "Amy"),
    ... ])
    <PreferenceSchedule total_votes=9>

    You can also create the :class:`~rcv.BallotSet` beforehand and pass it
    directly to the constructor:

    >>> ballots = BallotSet({
    ...     (("Amy", "Elizabeth", "Kirsten"), 10),
    ...     (("Kirsten", "Amy"), 20),
    ...     (("Elizabeth", "Kamala", "Kirsten"), 15),
    ...     (("Kamala", "Elizabeth"), 16),
    ...     (("Kamala", "Amy"), 14),
    ... })
    >>> PreferenceSchedule(ballots)
    <PreferenceSchedule total_votes=75>
    """

    def __init__(self, ballots, candidates=None):
        """
        :param ballots: all of the valid ballots cast in the election
        :type ballots: :class:`~rcv.BallotSet`
        :param candidates: optionally, the set of :class:`Candidates <~rcv.Candidate>`
            up for election. If not provided, the candidates will be inferred
            from the names on the ballots.
        """
        if candidates is None:
            names = {name for ballot, weight in ballots for name in ballot}
            candidates = {Candidate(name) for name in names}
        self.candidates = ValuesDict(
            {str(candidate): candidate for candidate in candidates}
        )
        self.distribute_ballots(ballots)
        self.total_votes = sum(candidate.total_votes for candidate in self.candidates)

    def __repr__(self):
        return "<{} total_votes={}>".format(
            self.__class__.__name__, int(self.total_votes)
        )

    def __iter__(self):
        return self.ballots

    @property
    def ballots(self):
        for candidate in self.candidates:
            for ballot in candidate.votes:
                yield ballot

    def remove_candidate(self, removed):
        for candidate in self.candidates:
            if candidate is not removed:
                candidate.votes = candidate.votes.eliminate(removed)
        removed.votes = BallotSet()
        del self.candidates[str(removed)]

    def distribute_ballots(self, ballots):
        for ballot, weight in ballots:
            if not ballot.is_empty:
                candidate = self.candidates[ballot.top_choice]
                candidate.votes.add(ballot, weight)

    def eliminate(self, eliminated):
        self.distribute_ballots(eliminated.votes.eliminate(eliminated))
        self.remove_candidate(eliminated)

    @classmethod
    def from_ballots(cls, items):
        return cls(BallotSet.from_items(items))

    @classmethod
    def from_dataframe(cls, df):
        """Create a preference schedule from a dataframe whose rows are ballots.
        That is, the first column is the first-ranked candidate for each ballot,
        the second is the second-ranked candidate, and so on.

        The preference orders are cleaned using :func:`normalize_preferences`.
        """
        if df.isna().any().any():
            df = df.fillna(False)

        grouped_ballots = df.groupby(list(df.columns)).size().items()

        return cls(
            BallotSet(
                (
                    (normalize_preferences(ballot), count)
                    for ballot, count in grouped_ballots
                )
            )
        )


def normalize_preferences(choices):
    """Removes duplicates and drops falsy values from a single preference order."""
    new_choices = []
    for choice in choices:
        if choice and (choice not in new_choices):
            new_choices.append(choice)
    return new_choices
