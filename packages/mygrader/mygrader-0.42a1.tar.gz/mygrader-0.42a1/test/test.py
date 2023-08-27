import math
from time import sleep


def calculate_triangle_area(a: float, b: float, c: float) -> float:
    """
    Calculates the area of a triangle using Heron's formula.

    Given the lengths of the three sides of a triangle, this function
    calculates the area of the triangle using Heron's formula, which is based
    on the semi-perimeter and the lengths of the sides.

    Parameters:
    - a: Length of side a of the triangle
    - b: Length of side b of the triangle
    - c: Length of side c of the triangle

    Returns:
    The area of the triangle.
    """

    s = (a + b + c) / 2
    area_squared = s * (s - a) * (s - b) * (s - c)
    area = math.sqrt(area_squared)

    sleep(0.1)
    return area


if __name__ == '__main__':
    from mygrader import mygrader
    from mygrader.src.y2023 import Solution

    tester = mygrader.Tester(2023, runtime_limit=3)
    solver = Solution()
    tester.run_test(calculate_triangle_area, 10)
