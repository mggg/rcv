from collections import defaultdict


def distinguish_duplicates(items):
    """
    >>> distinguish_duplicates(("W", "W", "B", "H", "B"))
    ['W_1', 'W_2', 'B_1', 'H_1', 'B_2']

    :param iterable items:
    :returns: a list with unique items obtained by appending ``"_n"`` to each item of
        ``items``, where ``n`` is how many times the item's value has occurred in
        ``items`` (starting at 1).
    :rtype: list[str]
    """
    counter = defaultdict(int)
    new_items = []
    for item in items:
        counter[item] += 1
        new_items.append("{}_{}".format(str(item), str(counter[item])))
    return new_items
