from os import rmdir
from os.path import isdir

from ecoindex.models import Ecoindex, Result, ScreenShot, WebPage
from pydantic import ValidationError
from pytest import raises


def test_model_webpage_no_url():
    with raises(ValidationError) as error:
        WebPage()

    assert (
        "1 validation error for WebPage\n"
        "url\n  "
        "Field required [type=missing, input_value={}, input_type=dict]\n"
    ) in str(error.value)


def test_model_webpage_invalid_url():
    with raises(ValidationError) as error:
        WebPage(url="toto")

    assert (
        "1 validation error for WebPage\n"
        "url\n  "
        "Input should be a valid URL, relative URL without a base "
        "[type=url_parsing, input_value='toto', input_type=str]\n"
    ) in str(error.value)


def test_model_webpage_wrong_size():
    with raises(ValidationError) as error:
        WebPage(url="https://www.google.fr", width=0, height=0)
        print(error.value)

    assert (
        "2 validation errors for WebPage\n"
        "width\n  "
        "Input should be greater than or equal to 100 [type=greater_than_equal, "
        "input_value=0, input_type=int]\n    "
        "For further information visit https://errors.pydantic.dev/2.3/v/greater_than_equal\n"
        "height\n  "
        "Input should be greater than or equal to 50 [type=greater_than_equal, "
        "input_value=0, input_type=int]\n    "
        "For further information visit https://errors.pydantic.dev/2.3/v/greater_than_equal"
    ) in str(error.value)


def test_model_webpage_default_size():
    webpage = WebPage(url="https://www.google.fr")
    assert webpage.height == 1080
    assert webpage.width == 1920


def test_model_valid():
    valid_ecoindex = Ecoindex(grade="A", score=99.9, ges=0.6, water=0.1)
    assert valid_ecoindex.grade == "A"
    assert valid_ecoindex.score == 99.9
    assert valid_ecoindex.ges == 0.6
    assert valid_ecoindex.water == 0.1
    assert valid_ecoindex.ecoindex_version not in [None, ""]


def test_model_invalid():
    with raises(ValidationError) as error:
        Ecoindex(grade="dummy", score="dummy")

    assert (
        "1 validation error for Ecoindex\nscore\n  "
        "Input should be a valid number, unable to parse string as a number"
    ) in str(error.value)


def test_ecoindex_model_empty():
    ecoindex = Ecoindex()
    assert ecoindex.ges is None
    assert ecoindex.grade is None
    assert ecoindex.score is None
    assert ecoindex.water is None


def test_result_model():
    result = Result(
        size=119,
        nodes=45,
        requests=8,
        url="http://www.myurl.com",
        width=1920,
        height=1080,
        grade="A",
        score=89,
        ges=1.22,
        water=1.89,
    )
    assert result.page_type is None
    assert result.size == 119
    assert result.nodes == 45
    assert result.requests == 8
    assert result.width == 1920
    assert result.height == 1080
    assert result.grade == "A"
    assert result.score == 89
    assert result.ges == 1.22
    assert result.water == 1.89
    assert result.ecoindex_version is not None


def test_screenshot_model():
    id = "screenshot_test_id"
    folder = "./screenshot_test"

    screenshot = ScreenShot(id=id, folder=folder)

    assert isdir(folder) is True
    assert screenshot.id == id
    assert screenshot.folder == folder
    assert screenshot.get_png() == f"{folder}/{id}.png"
    assert screenshot.get_webp() == f"{folder}/{id}.webp"

    rmdir(folder)
    assert isdir(folder) is False


if __name__ == "__main__":
    test_model_webpage_no_url()
    test_model_webpage_invalid_url()
    test_model_webpage_wrong_size()
    test_model_webpage_default_size()
    test_model_valid()
    test_model_invalid()
    test_ecoindex_model_empty()
    test_result_model()
    test_screenshot_model()
