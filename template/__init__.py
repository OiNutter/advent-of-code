from utils import load
from os import path
from time import time

class Day():
  
  def __init__(self, filename=__file__):
    self.filename = filename

  def log_answer(self, task, answer, start_time):
    print("The answer to task %i is:" % task, answer)
    self.log_time(start_time)

  def log_time(self, start):
    print("--- %f seconds ---\n" % (time() - start))

  def prep_data(self, data):
    pass

  def task_1(self):
    pass

  def task_2(self):
    pass

  def run(self):
    data = load(path.join(path.dirname(path.realpath(self.filename)), "input.txt"))
    
    start = time()
    prep_start = time()
    self.prep_data(data)
    print("--- Data Prep ---")
    self.log_time(prep_start)

    self.task_1()
    self.task_2()
    
    print("--- Total Time ---")
    self.log_time(start)