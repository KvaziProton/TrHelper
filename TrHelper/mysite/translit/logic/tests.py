# from .translit import Translit
import pytest

from .translit import is_integral, integral_term, Translit

@pytest.fixture(params=[
    ('Alan al Umar', True),
    ('Bakar', False),
    ('Agyr Amude', True)
    ])
def int_check(request):
    return request.param

def test_integral(int_check):
    name, exp = int_check
    assert exp == is_integral(name)

@pytest.fixture(params=['Alan-al Umar', 'Bakar Yasemîn', 'Agyr, Amude'])
def int_wrap(request):
    return request.param

class EchoClass():
    def __call__(self, term):
        return term


def test_wrap(int_wrap):
    inst = EchoClass()
    f = integral_term(inst)
    res = f(int_wrap)
    assert res == int_wrap

params_w = zip(
    (
    'Alan', 'Agir', 'Amûdê',
    'Baban', 'Birûsk', 'Banû',
    'Çeman', 'Çîçek', 'Çîn',
    'Yar', 'Yasemîn', 'Yekbûn',

    ),
    (
    'Алан', 'Агыр', 'Амуде',
    'Бабан', 'Быруск', 'Бану',
    'Чаман', 'Чичак', 'Чин',
     'Яр', 'Ясамин', 'Якбун',

    )
    )

@pytest.fixture(scope='module', params=params_w)
def data(request):
    return request.param


def test_translit(data):
    inp, expected = data
    tr = Translit(inp.lower())
    res = tr()
    print(ord(res[0]), ord('А'), ord('А'))
    assert res.capitalize() == expected
