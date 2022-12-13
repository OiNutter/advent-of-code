from template import Day
from time import time



class Solution(Day):

  letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  def __init__(self):
    super().__init__(__file__)

  @staticmethod
  def get_value(char):
    return Solution.letters.index(char) + 1

  def prep_data(self, data):
    self.data = data

  def task_1(self):
    start = time()
    total = 0
  
    for line in self.data:
      pack = line.strip()
      half = int(len(pack)/2)
      a = pack[:half]
      b = pack[half:]

      shared = []
      for char in a:
        if char in b and char not in shared:
          shared.append(char)

      for char in shared:
        total += self.get_value(char)
    
    self.log_answer(1, total, start)
    
  def task_2(self):
    start = time()
    groups = []
    group = 0
    for (i, line) in enumerate(self.data):
      if group + 1 > len(groups):
        groups.append([])
        
      groups[group].append(line)

      if (i+1)%3 == 0:
        group += 1

    score = 0
    for group in groups:
      for char in group[0]:
        if char in group[1] and char in group[2]:
          score += self.get_value(char)
          break
    
    self.log_answer(1, score, start)
