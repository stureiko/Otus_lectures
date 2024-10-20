import pytest

from helper import get_least


@pytest.mark.parametrize(
    'src, exp_result',
    [
        ([0, 1, 2, 3], 0),
        ([-1, 0, 1, 2, 3], 0),
        ([-10, 1, 2, 3, -5], 1),
    ]
)
def test_success_get_least(src, exp_result):
    result = get_least(*src)
    assert result == exp_result


@pytest.mark.parametrize(
    'src',
    [
        [0, '1', 2, 3],
        [-1, 'hello', 1, 2, 3],
        [-10, 1, 2, 'True', -5],
        ['-1', '0', 1, 2, 3],
    ]
)
def test_fail_get_least(src):
    with pytest.raises(TypeError):  # Contex Manager
        get_least(*src)
