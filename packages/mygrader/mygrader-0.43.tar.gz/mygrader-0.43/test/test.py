def display_time(ms: int):
    """
    The function `display_time` takes in a time in milliseconds and prints it in the format "X day(s), X
    hour(s), X minute(s), X second(s), and X millisecond(s)".

    Args:
      ms: The parameter `ms` represents the number of milliseconds.
    """
    sec = ms // 1000
    ms = ms % 1000

    minute = sec // 60
    sec = sec % 60

    hr = minute // 60
    minute = minute % 60

    day = hr // 24
    hr = hr % 24

    print(
        f"{day} day(s), {hr} hour(s), {minute} minute(s), {sec} second(s), and {ms} millisecond(s)")

    return 2


if __name__ == '__main__':
    from mygrader import mygrader
    from mygrader.src.y2023 import Solution

    tester = mygrader.Tester(2023, debug=True)
    solver = Solution()
    tester.run_test(display_time, num_test_cases=100, show_table=True)
