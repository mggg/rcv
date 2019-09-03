from .ballot import BallotSet


class Candidate:
    """A candidate up for election."""

    def __init__(self, name, votes=None):
        """
        :param str name: The candidate's name. Must be unique among all candidates
            ranked on ballots in the election.
        :param votes: the ballots belonging to the candidate---i.e., the ballots
            that prefer this candidate to all other remaining candidates, under
            the chosen voting rules.
        :type votes: :class:`~rcv.BallotSet`
        """
        self.name = str(name)
        self.votes = BallotSet(votes)

    def __repr__(self):
        return "<Candidate {} with {} votes>".format(self.name, self.total_votes)

    def __str__(self):
        return self.name

    @property
    def total_votes(self):
        """The total number of votes (possibly fractional) that the candidate
        currently owns at this moment in the voting process."""
        return self.votes.total_weight
