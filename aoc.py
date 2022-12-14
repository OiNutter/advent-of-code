import argparse
import os
import sys
import cProfile

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)

import days

parser = argparse.ArgumentParser(
  prog = "aoc",
  description = "Solutions for Advent of Code 2022"
)

parser.add_argument("day")
parser.add_argument("--profile", default=False, action="store_true", required=False)

args = parser.parse_args()

Solution = getattr(days, "day%s" % args.day).Solution
if args.profile:
  cProfile.run('Solution().run()')
else:
  Solution().run()