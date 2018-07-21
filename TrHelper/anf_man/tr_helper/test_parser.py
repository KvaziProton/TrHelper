import django
django.setup()

import pytest
from .toolbox import NewArticle, Manager, FlowListener
from bs4 import BeautifulSoup


# instanse_params = [
#     ('https://anfenglish.com/rojava/turkish-state-cuts-off-waters-of-euphrates-again-28053',
#     'turkish-state-cuts-off-waters-of-euphrates-again-28053', 'english',
#     'https://anfenglish.com/uploads/en/articles/2018/07/20180707-120207-menbic-artesa-turik-a-dagerkir-avi-leser-gelen-mennbci-qot-kir593f43-image.jpg'
#     ),
#     ('https://anfenglish.com/freedom-of-the-press/action-to-demand-freedom-for-jailed-journalists-in-turkey-28054',
#     'action-to-demand-freedom-for-jailed-journalists-in-turkey-28054', 'english',
#     'https://anfenglish.com/uploads/en/articles/2018/07/20180707-20180707-mesale-0188ba4f-image794008-image.jpg'
#     ),
#     ('https://anfkurdi.com/rojava-sUriye/Soresa-me-berhema-keda-ji-40-sali-ye-99981',
#     "Soresa-me-berhema-keda-ji-40-sali-ye-99981", 'kurdi',
#     'https://anfkurdi.com/uploads/ku/articles/2018/07/20180719-20180719-img-108224bbd0-imageb6eff3-image.JPG'
#     )
#     ]
#
# @pytest.fixture(scope='module', params=instanse_params)
# def newarticle_data(request):
#     return request.param
#
# def test_newarticle_cls(newarticle_data):
#     url, *exp = newarticle_data
#     inst = NewArticle(url=url,)
#     res = [inst.url_title, inst.language, inst.img_url]
#     assert res == exp
#
# soup=BeautifulSoup(open('test_static/soup_all.html'), 'lxml')
# ifnew_params = [
#     (   'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101',
#         [],
#         'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101'
#     ),
#
#     (   'https://anfenglish.com/news/vote-counting-begins-in-sulaymaniyah-28100',
#         ['https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101',
#         ],
#         'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101'
#     ),
#
#     (   "https://anfenglish.com/news/nechirvan-barzani-to-attend-erdogan-s-ceremony-28098",
#         ['https://anfenglish.com/women/women-from-afrin-ready-to-join-the-campaign-to-liberate-home-28099',
#         'https://anfenglish.com/news/vote-counting-begins-in-sulaymaniyah-28100',
#         'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101',
#
#         ],
#         'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28101'
#     )]
#
# @pytest.fixture(scope='module', params=ifnew_params)
# def ifnew_data(request):
#     return request.param
#
# def test_flowlistener_cls(ifnew_data):
#     last_article, exp, new_last = ifnew_data
#     res, last = FlowListener(
#         last=last_article,
#         soup=soup,
#         log='test_static/test_last.txt'
#         ).start()
#     assert res == exp
#     assert last == new_last
#
# manager_params_eng = [
#     ('test_static/ar_1.html',
#     'https://anfenglish.com/features/turkish-state-barbarism-in-afrin-knows-no-bounds-28115',
#     'update'), #same pict, similar title
#     ('test_static/ar_1.html',
#     'https://anfenglish.com/features/turkish-state-brbarism-in-efrin-knows-bounds-28101',
#     'update'),#same pict, similar title
#     ('test_static/ar_2.html',
#     'https://anfenglish.com/rojava/turkish-state-cuts-off-waters-of-euphrates-again-28053',
#     'new'), #diff pict, diff title
#     ('test_static/ar_4(kurd).html',
#     'https://anfenglish.com/rojava-sUriye/Soresa-me-berhema-keda-ji-40-sali-ye-99981',
#     'found version') #same pict, diff lang
#     ]
#
#
# @pytest.fixture(scope='module', params=manager_params_eng)
# def manage_data_eng(request):
#     return request.param
#
# def test_manager_cls(manage_data_eng):
#     path, url, exp = manage_data_eng
#     soup = BeautifulSoup(open(path), 'lxml')
#     manager = Manager(log='test_static/test_log.txt', url=url, soup=soup)
#     res = manager.get_status(url, test=True)
#     assert res == exp


def test_integrity():
    start = open('tr_helper/last_article_log.txt').readlines()[-1].strip()
    listener = FlowListener(last=start)
    listener.start()
    assert False
