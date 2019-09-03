from .weighted_set import WeightedSet


class Ballot(tuple):
    def __repr__(self):
        names = "({})".format(", ".join(map(str, self)))
        return "<Ballot {}>".format(names)

    def eliminate(self, eliminated_candidate):
        return self.__class__(
            candidate
            for candidate in self
            if str(candidate) != str(eliminated_candidate)
        )

    @property
    def top_choice(self):
        if len(self) == 0:
            return None
        return str(self[0])

    @property
    def next_choice(self):
        if len(self) < 2:
            return None
        return str(self[1])

    @property
    def is_empty(self):
        return len(self) == 0


class BallotSet(WeightedSet):
    def __init__(self, weighted_items=None, **kwargs):
        if weighted_items is not None:
            super().__init__(
                ((Ballot(item), weight) for item, weight in weighted_items), **kwargs
            )
        else:
            super().__init__(**kwargs)

    def eliminate(self, eliminated_candidate):
        return self.__class__(
            (ballot.eliminate(eliminated_candidate), weight)
            for (ballot, weight) in self
        )
