from collections import defaultdict
from fractions import Fraction
from itertools import repeat
from numbers import Number


class WeightedSet:
    def __init__(self, weighted_items=None, weight_type=Fraction):
        self._weight_type = weight_type
        self._weights = defaultdict(int)
        if weighted_items is not None:
            self.update(weighted_items)

    def __repr__(self):
        items = (
            "{"
            + ", ".join(["{} * {}".format(weight, item) for item, weight in self])
            + "}"
        )
        return "<{} {}>".format(self.__class__.__name__, items)

    @property
    def is_empty(self):
        return self.total_weight == 0

    @property
    def total_weight(self):
        return sum(self._weights.values())

    @property
    def weight_type(self):
        return self._weight_type

    def add(self, item, weight=1):
        self._weights[item] += self.weight_type(weight)

    def update(self, items):
        for item, weight in items:
            self.add(item, weight)

    def __iter__(self):
        for item, weight in self._weights.items():
            if weight > 0:
                yield item, weight

    def __eq__(self, other):
        return set(self) == set(other)

    def __imul__(self, multiplier):
        if not isinstance(multiplier, Number):
            raise NotImplementedError
        for item in self._weights:
            self._weights[item] *= multiplier
        return self

    def __mul__(self, multiplier):
        if not isinstance(multiplier, Number):
            raise NotImplementedError
        return self.__class__((item, weight * multiplier) for item, weight in self)

    def __rmul__(self, multiplier):
        return self.__mul__(multiplier)

    @classmethod
    def from_items(cls, items):
        return cls(zip(items, repeat(1)))
