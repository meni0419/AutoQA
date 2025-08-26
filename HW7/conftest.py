import os
import pytest
import requests

from employee_api import EmployeeApi


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=os.environ.get("EMPLOYEE_API_BASE_URL", "http://5.101.50.27:8000"),
        help="Base URL for Employee API",
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    return pytestconfig.getoption("--base-url")


@pytest.fixture(scope="session")
def http_session() -> requests.Session:
    sess = requests.Session()
    # При необходимости добавить заголовки/авторизацию:
    # sess.headers.update({"Authorization": "Bearer <token>"})
    return sess


@pytest.fixture(scope="session")
def api(http_session, base_url) -> EmployeeApi:
    return EmployeeApi(http_session, base_url)