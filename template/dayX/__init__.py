
from template import Day
from time import time

class Solution(Day):
  
  def __init__(self):
    super().__init__(__file__)


  def prep_data(self, data):
    self.data = data

  def task_1(self):
    start = time()

    self.log_answer(1, "", start)

  def task_2(self):
    start = time()

    self.log_answer(2, "", start)

  
