class PositionUtils:
    """Utility class for handling element positions in Playwright.
    Provides methods to get relative and absolute positions of elements.
    Why?
       {
            - Composition over Inheritance: More flexible and doesn't force a rigid class hierarchy
            - Single Responsibility: Each utility class has a focused purpose
            - Easier Testing: Static methods are easier to unit test
            - Less Coupling: Page objects aren't forced into an inheritance hierarchy
            - Extensibility: Easy to add more utilities without affecting existing code
        }
    """

    @staticmethod
    def get_relative_position(element, x_percent=50, y_percent=50):
        """
        Get position based on percentage of element size.

        Args:
            element: Playwright ElementHandle object
            x_percent: int - X position as percentage (0-100)
            y_percent: int - Y position as percentage (0-100)

        Returns:
            dict: Dictionary with 'x' and 'y' coordinates

        Example:
            # Click at 25% from left, 75% from top
            pos = PositionUtils.get_relative_position(element, 25, 75)
        """
        bounding_box = element.bounding_box()

        if not bounding_box:
            raise ValueError("Element is not visible or has no bounding box")

        x = bounding_box["x"] + (bounding_box["width"] * x_percent / 100)
        y = bounding_box["y"] + (bounding_box["height"] * y_percent / 100)

        return {"x": int(x), "y": int(y)}

    @staticmethod
    def get_absolute_position(element):
        """Example"""
        pass
