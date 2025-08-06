class TimeoutConstants:
    """Constants for timeout settings."""

    DEFAULT_TIMEOUT = 30  # Default timeout in seconds
    SHORT_TIMEOUT = 10  # Short timeout in seconds
    LONG_TIMEOUT = 60  # Long timeout in seconds


class ScrollConstants:
    """Constants for scroll settings."""

    SCROLL_STEP = 10  # Number of times to scroll down per action
    SCROLL_DELAY = 200  # Delay in milliseconds between scrolls


class MobileDeviceConstants:
    """Constants for mobile device configurations."""

    IPHONE_12 = "iPhone 12"
    SAMSUNG_GALAXY_S21 = "Samsung Galaxy S21"
    GOOGLE_PIXEL_5 = "Google Pixel 5"


class DeviceConstants:
    """Constants for device configurations."""

    MOBILE = MobileDeviceConstants()
    TABLET = "Tablet"
    DESKTOP = "Desktop"


class ScreenConstants:
    """Constants for screen dimensions."""

    HD = "1280, 720"  # HD resolution
    FULL_HD = "1920, 1080"  # Full HD resolution
    FOUR_K = "3840, 2160"  # 4K resolution
