import pytest
from .logic.tr_new import SingleTranslit

#Izolated class Translit tests for one word.

params_single = zip(
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


@pytest.fixture(scope='module', params=params_single)
def tr_single_data(request):
    return request.param


def test_tr_cls(tr_single_data):
    inp, expected = tr_single_data
    print(inp, expected)
    res = SingleTranslit(inp).translit()
    assert res == expected


#Integred test of RawTranslit class
from .logic.tr_new import RawTranslit

raw_params = zip(
    ('Alan-al Umer', 'Bakar Yasemîn', 'Agir, Amûdê', '123', 'Bakar', 'Марина'),
    ('Алан-аль Умар', 'Бакар Ясамин', 'Агыр, Амуде', '123', 'Бакар', 'Марина')
    )

@pytest.fixture(params=raw_params)
def raw_data_for_cls(request):
    return request.param


def test_raw_translit(raw_data_for_cls):
    raw, exp = raw_data_for_cls
    res = RawTranslit(raw)()
    assert res == exp

#test of dict_check method in RawTranslit class
