import importlib
import pytest
from typing import Generator
from src.core.decoration_controller import TestDecorationController
from src.core.logger_controller import LoggerController
from tests.test_home_page_posts.assertions import HomePageAssertions


@pytest.fixture
def pre_condition():
    pass


@pytest.fixture(autouse=True, scope="session")
def load_env():
    """
    Fixture to load environment variables before running tests.
    """
    from src.utils.env_utils import load_dotenv_file

    # Load environment variables from the appropriate .env file based on the ENVIRONMENT variable
    # This ensures that the environment is set up correctly for the tests.
    dotenv_path = load_dotenv_file()
    print(f"Environment variables loaded from: {dotenv_path}")
    yield


@pytest.fixture
def logger_controller(request) -> Generator[LoggerController, None, None]:
    """
    Provide logger controller instance for tests with automatic log export.
    """
    test_name = request.node.name
    logger = LoggerController(test_name=test_name)
    yield logger

    # Print summary
    summary = logger.get_test_summary()
    print(f"\n📊 Test Summary for {test_name}:")
    print(f"   Duration: {summary['duration_seconds']:.2f}s")
    print(f"   Total logs: {summary['total_log_entries']}")
    print(f"   Errors: {summary['error_count']}")
    logger.export_logs_to_file(f"test-results/logs/{test_name}.txt", "txt")


def pytest_generate_tests(metafunc):
    # called once per each test session
    TestDecorationController.apply_custom_maker(metafunc, "devices", "device_marker")
    TestDecorationController.apply_custom_maker(
        metafunc, "screen_sizes", "screen_sizes"
    )


@pytest.fixture(scope="function", autouse=True)
def device_marker(request, browser_context_args, playwright):
    device_marker = TestDecorationController.get_maker_value(request, "device_marker")
    if device_marker:
        try:
            browser_context_args.update(**playwright.devices[device_marker])
        except KeyError:
            print(f"Device {device_marker} is not supported.")
    yield


@pytest.fixture(scope="function", autouse=True)
def screen_sizes(request, browser_context_args):
    sizes = TestDecorationController.get_maker_value(request, "screen_sizes")
    if sizes:
        width, height = sizes.replace(" ", "").split(",")
        browser_context_args.update(
            viewport={"width": int(width), "height": int(height)}
        )

    yield
