from pytest import fixture


@fixture(name="current_settings", scope="function")
def mock_current_settings(mocker):
    mock = mocker.patch("flask_gordon.ext.ctx._get_current_settings")
    mock.return_value = {}
    yield mock
