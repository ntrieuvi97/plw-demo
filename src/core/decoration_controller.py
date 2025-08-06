from typing import Literal
import pytest

PW_EMULATOR_IPHONE_14 = "iPhone 14"


def device_marker(*names):
    """
    Decorator to mark the test to run on a specific devices.
    This will create a new instance of Pytest MarkGenerator with the device name.
    When the test is executed, the device name will be passed to the test function.
    Highly note that: Need the "_emulators" parameter in the test function.
    Example:
        @devices(PW_EMULATOR_IPHONE_14, PW_EMULATOR_IPHONE_14_PM)
        def test_something(_emulators):
            pass

    :param names: The device name. Recommended to use the constants defined in this file.
    :return: The pytest marker.
    """
    return pytest.mark.devices(*names)


def screen_sizes(*sizes):
    """
    Decorator to mark the test to run on a specific screen size.
    This will create a new instance of Pytest MarkGenerator with the screen size.
    When the test is executed, the screen size will be passed to the test function.
    Highly note that: Need the "_screen_sizes" parameter in the test function.
    :param sizes: The screen size. The format is "width, height". Example: "1920, 1080". \\n
    Recommended to use the constants defined in this file.
    :return: The pytest marker.
    """
    return pytest.mark.screen_sizes(*sizes)


class TestDecorationController:
    @staticmethod
    def apply_custom_maker(
        metafunc,
        maker_name: str,
        parameter_name: str,
        scope: Literal["function", "session"] = "function",
    ):
        makers = metafunc.definition.own_markers
        # Get the devices from the markers
        marker_args = [
            marker.args
            for marker in makers
            if marker.name == maker_name and marker.args
        ]
        if marker_args:
            metafunc.parametrize(
                parameter_name, marker_args[0], indirect=True, scope=scope
            )

    @staticmethod
    def get_maker_value(request, maker_name: str):
        makers = request.node.callspec.params.get(maker_name, [])
        # Get the devices from the markers
        return makers if makers else None
