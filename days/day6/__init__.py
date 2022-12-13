from template import Day
from time import time

class Solution(Day):

  def __init__(self):
    super().__init__(__file__)

  def prep_data(self, data):
    self.data = data
  
  def find_chunk(self, block_size=2):
    for line in self.data:
      for i in range(block_size,len(line)):
        chunk = line[i-block_size:i]
        filtered = set(chunk)

        if len(chunk) == len(filtered):
          return i

  def task_1(self):
    start = time()
    chars = self.find_chunk(4)
    self.log_answer(1, chars, start)

  def task_2(self):
    start = time()
    chars = self.find_chunk(14)
    self.log_answer(2, chars, start)

