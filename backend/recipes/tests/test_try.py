def one_more(x):
    return x + 1


def test_correct():
    assert one_more(4) == 5


def test_fail():
    assert one_more(3) == 5
