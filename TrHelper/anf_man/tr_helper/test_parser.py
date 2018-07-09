import pytest
from .tasks import check_if_new, NewArticle, articles_queue
from bs4 import BeautifulSoup

instanse_params = [
    ('https://anfenglish.com/rojava/turkish-state-cuts-off-waters-of-euphrates-again-28053',
    'Turkish state cuts off waters of Euphrates again', 2907),
    ('https://anfenglish.com/freedom-of-the-press/action-to-demand-freedom-for-jailed-journalists-in-turkey-28054',
    'Action to demand freedom for jailed journalists in Turkey', 1367)
    ]

@pytest.fixture(scope='module', params=instanse_params)
def newarticle_data(request):
    return request.param

def test_newarticle_cls(newarticle_data):
    inp, *exp = newarticle_data
    inst = NewArticle(inp)
    res = [inst.title, inst.symbols_amount]
    assert res == exp


soup=BeautifulSoup(open('tests/soup_all.html'), 'lxml')
ifnew_params = [
    (
        'Turkish state barbarism in Afrin knows no bounds',
        0,
        'Turkish state barbarism in Afrin knows no bounds'
    ),
    (
        'Vote counting begins in Sulaymaniyah',
        1,
        'Turkish state barbarism in Afrin knows no bounds',
        'Turkish state barbarism in Afrin knows no bounds',
        'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101'
    ),
    (
        "Nechirvan Barzani to attend Erdoğan's ceremony",
        3,
        'Turkish state barbarism in Afrin knows no bounds',
        'Women from Afrin ready to join the campaign to liberate home',
        'https://anfenglish.com/women/women-from-afrin-ready-to-join-the-campaign-to-liberate-home-28099')
    ]

@pytest.fixture(scope='module', params=ifnew_params)
def ifnew_data(request):
    return request.param

def test_ifnew_func(ifnew_data):
    last_article, l, exp_new_last, *rest = ifnew_data
    new_last = check_if_new(last_article, soup)
    assert new_last == exp_new_last
    assert len(articles_queue) == l
    if articles_queue:
        data = articles_queue.pop()
        title, url = rest
        assert isinstance(data, NewArticle) == True
        assert data.title == title
        assert data.url == url
