import pytest
from img_compare import img_compare_mse, img_compare_ssim
img_params = []

@pytest.fixture(scope='module', params=img_params)
def imgcompare_data(request):
    return request.params

def test_imgcompare(imgcompare_data):
    data, expected = imgcompare_data
    res_mse = img_compare_mse()
    assert res_mse == expected
