
from template import Day
from time import time
from functools import cmp_to_key
from math import prod

class Solution(Day):
  pairs = [[]]

  def __init__(self):
    super().__init__(__file__)

  @staticmethod
  def compare_lists(a, b):
    count = 0
    for i in range(len(a)):
      if i >= len(b):
        return -1

      result = Solution.compare_pairs(a[i], b[i])

      if result != 0:
        return result

      count += 1

    if count < len(b):
      return 1

    return 0 

  @staticmethod
  def compare_pairs(a, b):
    if isinstance(a, list) and isinstance(b, list):
      return Solution.compare_lists(a,b)
    elif isinstance(a, list) and not isinstance(b, list):
      return Solution.compare_lists(a, [b])
    elif isinstance(b, list) and not isinstance(a, list):
      return Solution.compare_lists([a], b)
    else:
      if a < b:
        return 1
      elif a > b:
        return -1
    
    return 0

  def prep_data(self, data):
    for line in data:
      if line.strip() != "":
        self.pairs[-1].append(eval(line.strip()))
      else:
        self.pairs.append([])

  def task_1(self):
    start = time()

    correct = []
    for i, pair in enumerate(self.pairs):
      if self.compare_pairs(pair[0], pair[1]) > 0:
        correct.append(i+1)

    self.log_answer(1, sum(correct), start)

  def task_2(self):
    start = time()

    dividers = [[2], [6]]
    ordered = dividers + []
    for i, pair in enumerate(self.pairs):
      if self.compare_pairs(pair[0], pair[1]) > 0:
        ordered+= pair
      else:
        ordered += list(reversed(pair))

    ordered = sorted(ordered, key = cmp_to_key(self.compare_pairs), reverse=True)

    indices = []
    for divider in dividers:
      indices.append(ordered.index(divider)+1)

    self.log_answer(2, prod(indices), start)

  
