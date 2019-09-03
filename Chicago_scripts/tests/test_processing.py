from rcv.processing import distinguish_duplicates


def test_distinguish_duplicates():
    result = distinguish_duplicates(("W", "W", "B", "H", "B"))
    assert result == ["W_1", "W_2", "B_1", "H_1", "B_2"]
