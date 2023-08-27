from mygrader.src.y2023 import Solution
from mygrader.tester import Tester


def display_time(n):
    print(n)


if __name__ == '__main__':
    tester = Tester(2023, runtime_limit=0.4, log_option="print")
    tester.run_test(Solution.calculate_sum, 100_000)
