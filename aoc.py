import argparse
import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)

import days

parser = argparse.ArgumentParser(
  prog = "aoc",
  description = "Solutions for Advent of Code 2022"
)

parser.add_argument("day")

args = parser.parse_args()

Solution = getattr(days, "day%s" % args.day).Solution
Solution().run()