from .schedule import PreferenceSchedule
from .ballot import BallotSet

import numpy


class PreferenceSampler(dict):
    """
    For sampling a :class:`~rcv.PreferenceSchedule` from a given
    :class:`~rcv.BallotSet`.
    """

    def __init__(self, data):
        """
        :param data: the ballots to sample from
        :type data: :class:`~rcv.BallotSet`
        """
        ballots = BallotSet(data, weight_type=float)
        rankings, weights = zip(*ballots)
        self.rankings = rankings
        self.indices = numpy.arange(len(rankings))
        self.p = numpy.asarray(weights)
        self.p /= numpy.sum(self.p)

    def __repr__(self):
        return "<PreferenceSampler rankings={} p={}>".format(self.rankings, self.p)

    def sample(self, k):
        """
        Sample ballots to produce a :class:`~rcv.PreferenceSchedule`.

        :param int k: the number of ballots to sample
        :return: a :class:`~rcv.PreferenceSchedule` holding the sampled preferences
        :rtype: rcv.PreferenceSchedule
        """
        chosen = numpy.random.choice(self.indices, size=k, p=self.p)
        return PreferenceSchedule.from_ballots(self.rankings[index] for index in chosen)

    @classmethod
    def from_units(cls, data, turnouts=None):
        if turnouts is None:
            turnouts = dict()
        all_ballots = BallotSet(weight_type=float)
        for unit, ballots in data.items():
            all_ballots.update(ballots * turnouts.get(unit, 1))
        return cls(all_ballots)
