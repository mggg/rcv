import math

from .schedule import PreferenceSchedule
from .ballot import BallotSet


def find_winners(candidates, quota):
    return {candidate for candidate in candidates if candidate.total_votes >= quota}


def find_least(candidates):
    iter_candidates = iter(candidates)
    least = next(iter_candidates)
    for candidate in candidates:
        if candidate.total_votes < least.total_votes:
            least = candidate
    return least


def droop_quota(number_of_votes, number_of_seats):
    """The `Droop quota`_ for Single Transferable Vote tabulation. A candidate
    whose vote total meets this quota wins a seat.

    .. _`Droop quota`: https://en.wikipedia.org/wiki/Droop_quota
    """
    return math.floor(number_of_votes / (number_of_seats + 1)) + 1


class FractionalSTV:
    """Tabulates ranked-choice ballots according to Fractional Single
    Transferable Vote rules.

    >>> schedule = PreferenceSchedule.from_ballots([
    ...     ("Kamala", "Amy", "Elizabeth"),
    ...     ("Kamala", "Elizabeth", "Amy"),
    ...     ("Kamala", "Elizabeth", "Amy"),
    ... ])
    >>> stv = FractionalSTV(schedule, seats=2)
    >>> winners = stv.elect()
    >>> winners == {"Kamala", "Elizabeth"}
    True
    """

    def __init__(self, schedule, seats, quota=droop_quota):
        """
        :param schedule: A :class:`~rcv.PreferenceSchedule` holding all the
            ranked-choice ballots cast in the election.
        :param seats: the number of seats up for election
        :param quota: the quota that a candidate must meet to win a seat
        :type schedule: PreferenceSchedule
        :type seats: int
        :type quota: function or Number
        """

        if not isinstance(schedule, PreferenceSchedule):
            schedule = PreferenceSchedule(schedule)
        self.schedule = schedule

        if callable(quota):
            self.quota = quota(schedule.total_votes, seats)
        else:
            self.quota = quota

        if seats > len(self.candidates):
            raise ValueError(
                "The number of seats requested is greater than "
                "the number of candidates available to elect."
            )

        self.seats = seats
        self.elected = set()

    @property
    def candidates(self):
        return self.schedule.candidates

    def elect(self):
        """Runs the Fractional Single Transferable Vote algorithm to
        determine the winners of the election.

        :returns: a set holding the names (as strings) of the elected
            candidates.
        :rtype: Set[str]
        """
        if len(self.candidates) == self.seats:
            return {str(candidate) for candidate in self.candidates}
        while len(self.elected) < self.seats and len(self.candidates) > 0:
            if len(self.candidates) + len(self.elected) == self.seats:
                return {
                    str(candidate) for candidate in self.elected.union(self.candidates)
                }
            winners = find_winners(self.candidates, self.quota)
            if len(winners) > 0:
                for winner in winners:
                    self.declare_winner(winner)
            else:
                least = find_least(self.candidates)
                self.schedule.eliminate(least)
        return {str(candidate) for candidate in self.elected}

    def declare_winner(self, winner):
        ballots_to_transfer = self.transferable_votes(winner)
        self.schedule.distribute_ballots(ballots_to_transfer)
        self.elected.add(winner)
        self.schedule.remove_candidate(winner)

    def transferable_votes(self, candidate):
        total = candidate.total_votes
        quota = self.quota

        if total <= quota:
            return BallotSet()

        fraction = (total - quota) / total
        transferable = BallotSet()
        for vote, count in candidate.votes:
            next_choice = vote.next_choice
            if next_choice is not None:
                transferable.add(vote.eliminate(candidate), count * fraction)

        return transferable
