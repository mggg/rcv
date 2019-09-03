import pytest
from rcv.weighted_set import WeightedSet


@pytest.fixture
def weighted_set():
    items = [("a", 10), ("b", 15), ("c", 1)]
    weighted_set = WeightedSet(items)
    return weighted_set


class TestWeightedSet:
    def test_can_be_created(self, weighted_set):
        assert weighted_set

    def test_has_total_weight(self, weighted_set):
        assert weighted_set.total_weight == 26

    def test_can_change_weight_with_multiplication(self, weighted_set):
        weighted_set *= 4
        assert weighted_set == WeightedSet([("a", 40), ("b", 60), ("c", 4)])

    def test_can_multiply_immutably(self, weighted_set):
        multiplied = 4 * weighted_set
        assert multiplied == WeightedSet([("a", 40), ("b", 60), ("c", 4)])
        assert multiplied != weighted_set

    def test_can_multiply_on_the_right(self, weighted_set):
        multiplied = weighted_set * 4
        assert multiplied == WeightedSet([("a", 40), ("b", 60), ("c", 4)])
        assert multiplied != weighted_set

    def test_raises_NotImplementedError_when_multiplying_by_non_number(
        self, weighted_set
    ):
        with pytest.raises(NotImplementedError):
            weighted_set *= "not a number"

        with pytest.raises(NotImplementedError):
            weighted_set * "not a number"

        with pytest.raises(NotImplementedError):
            "not a number" * weighted_set

    def test_can_update(self, weighted_set):
        weighted_set.update(WeightedSet([("a", 10), ("d", 5)]))

        assert weighted_set == WeightedSet([("a", 20), ("b", 15), ("c", 1), ("d", 5)])

    def test_from_items(self):
        weighted_set = WeightedSet.from_items([1, 2, 3])
        assert weighted_set == WeightedSet([(1, 1), (2, 1), (3, 1)])

    def test_has_weight_type_argument(self):
        weighted_set = WeightedSet([("a", 40), ("b", 60), ("c", 4)], weight_type=float)
        assert all(isinstance(weight, float) for item, weight in weighted_set)
