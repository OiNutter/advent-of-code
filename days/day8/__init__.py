from template import Day
from time import time

class Solution(Day):

  max_x = 0
  max_y = 0

  trees = []

  def __init__(self):
    super().__init__(__file__)

  def is_visible_x(self, x, y):
    visible_left = True
    visible_right = True
    for i in range(x):
      if self.trees[i][y] >= self.trees[x][y]:
        visible_left = False

    for i in range(x+1, self.max_x):
      if self.trees[i][y] >= self.trees[x][y]:
        visible_right = False

    return visible_left or visible_right

  def is_visible_y(self, x, y):
    visible_top = True
    visible_bottom = True
    for i in range(y):
      if self.trees[x][i] >= self.trees[x][y]:
        visible_top = False

    for i in range(y+1, self.max_y):
      if self.trees[x][i] >= self.trees[x][y]:
        visible_bottom = False

    return visible_top or visible_bottom
    

  def is_visible(self, x,y):
    return self.is_visible_x(x, y) or self.is_visible_y(x, y)

  def calculate_view(self, x, y):
    views = {
      "top": 0,
      "bottom": 0,
      "left": 0,
      "right": 0
    }

    count = 0
    for i in range(y-1, -1, -1):
      count += 1
      if self.trees[x][i] >= self.trees[x][y]:
        break
    views["top"] = count

    count = 0
    for i in range(x-1, -1, -1):
      count += 1
      if self.trees[i][y] >= self.trees[x][y]:
        break
    views["left"] = count
      
    count = 0
    for i in range(y+1, self.max_y):
      count += 1
      if self.trees[x][i] >= self.trees[x][y]:
        break
    views["bottom"] = count
        
    count = 0
    for i in range(x+1, self.max_x):
      count += 1
      if self.trees[i][y] >= self.trees[x][y]:
        break
    views["right"] = count
        
    return views["top"] * views["bottom"] * views["left"] * views["right"]

  def prep_data(self, data):
    for _, line in enumerate(data):
      for x, tree in enumerate(line.strip()):
        if x >= len(self.trees):
          self.trees.append([])

        self.trees[x].append(tree)

    self.max_x = len(self.trees)
    if len(self.trees) > 0:
      self.max_y = len(self.trees[0])
  
  def task_1(self):
    start = time()
    count = 0
    for x in range(self.max_x):
      for y in range(self.max_y):
        if self.is_visible(x, y):
          count += 1

    self.log_answer(1, count, start)

  def task_2(self):
    start = time()
    best = 0
    for x in range(self.max_x):
      for y in range(self.max_y):
        score = self.calculate_view(x, y)
        if score > best:
          best = score

    self.log_answer(2, best, start)
