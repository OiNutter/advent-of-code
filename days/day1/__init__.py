
from template import Day
from time import time

class Solution(Day):

  elves = None

  def __init__(self):
    super().__init__(__file__)

  def prep_data(self, data):
    elves = [0]
    elf=0
    for line in data:
      if line != "\n":
        elves[elf] += int(line)
      else:
        elf += 1
        elves.append(0)

    elves.sort(reverse = True)
    self.elves = elves
 
  def task_1(self):
    start = time()
    self.log_answer(1, max(self.elves), start)

  def task_2(self):
    start = time()    
    tops = 0
    for index in range(3):
      tops += self.elves[index]

    self.log_answer(2, tops, start)

  
