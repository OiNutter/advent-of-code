
from template import Day
from time import time
import json

ROCK = "#"
SAND = "+"
AIR = "."
STOPPED_SAND = "o"

class Solution(Day):
  
  cave = {}

  sand = [500,0]
  min_x = None
  min_y = None
  max_x = None
  max_y = None
  can_fall = True

  def __init__(self):
    super().__init__(__file__)

  def draw_cave(self):
    for y in range(self.min_y, self.max_y+1):
      row = []
      for x in range (self.min_x, self.max_x+1):
        row.append(self.cave[x][y] if x in self.cave and y in self.cave[x] else AIR)
      print("".join(row))

  def prep_data(self, data):
    self.data = data

  def build_cave(self):
    self.cave = {}
    self.sand = [500,0]
    self.min_x = None
    self.min_y = None
    self.max_x = None
    self.max_y = None
    self.can_fall = True

    for line in self.data:
      coords = [json.loads("[%s]" % x) for x in line.strip().split(" -> ")]
      for i in range(1, len(coords)):
        start = coords[i-1]
        end = coords[i]
        step_x = (-1 if end[0] < start[0] else 1)
        for x in range(start[0], end[0] + step_x, step_x):
          if x not in self.cave:
            self.cave[x] = {}
          if self.min_x is None or x < self.min_x:
            self.min_x = x
          if self.max_x is None or x > self.max_x:
            self.max_x = x

          step_y = (-1 if end[1] < start[1] else 1)
          for y in range(start[1], end[1] + step_y, step_y):
            self.cave[x][y] = ROCK
            if self.min_y is None or y < self.min_y:
              self.min_y = y
            if self.max_y is None or y > self.max_y:
              self.max_y = y

    sand_x = self.sand[0]
    sand_y = self.sand[1]

    if self.min_x is None or sand_x < self.min_x:
      self.min_x = sand_x
    if self.max_x is None or sand_x > self.max_x:
      self.max_x = sand_x

    if self.min_y is None or sand_y < self.min_y:
      self.min_y = sand_y
    if self.max_y is None or sand_y > self.max_y:
      self.max_y = sand_y
      
    if sand_x not in self.cave:
      self.cave[sand_x] = {}

    self.cave[sand_x][sand_y] = SAND
  
  def move_sand(self, floor = None, limit_x = True):
    sand_x = self.sand[0]
    sand_y = self.sand[1]
      
    if (sand_y + 1) > self.max_y:
      self.can_fall = False
      return False

    if (sand_y+1) not in self.cave[sand_x]:

      if floor is not None and sand_y+1 == floor:
        self.cave[sand_x][sand_y] = STOPPED_SAND
        self.cave[sand_x][sand_y+1] = ROCK
        return False

      del self.cave[sand_x][sand_y]
      sand_y += 1
    elif (sand_x -1) not in self.cave or (sand_y+1) not in self.cave[sand_x-1]:
      del self.cave[sand_x][sand_y]
      if limit_x and sand_x - 1 < self.min_x:
        self.can_fall = False
        return False
      else:
        if sand_x - 1 < self.min_x:
          self.min_x = sand_x - 1
      
      if floor is not None and sand_y+1 == floor:
        self.cave[sand_x][sand_y] = STOPPED_SAND
        self.cave[sand_x][sand_y+1] = ROCK
        return False

      sand_x -= 1
      sand_y += 1

    elif (sand_x + 1) not in self.cave or (sand_y+1) not in self.cave[sand_x+1]:
      del self.cave[sand_x][sand_y]
      if limit_x and sand_x + 1 > self.max_x:
        self.can_fall = False
        return False
      else:
        if sand_x + 1 > self.max_x:
          self.max_x = sand_x + 1

      if floor is not None and sand_y+1 == floor:
        self.cave[sand_x][sand_y] = STOPPED_SAND
        self.cave[sand_x][sand_y+1] = ROCK
        return False
      sand_x += 1
      sand_y += 1
    else:
      self.cave[sand_x][sand_y] = STOPPED_SAND
      return False

    self.sand = [sand_x, sand_y] 
    if sand_x not in self.cave:
      self.cave[sand_x] = {}

    self.cave[sand_x][sand_y] = SAND
    return True

  def task_1(self):
    start = time()
    self.build_cave()
    count = 0
    self.can_fall = True
    
    while self.can_fall:
      falling = True
      cycles = 0
      
      while falling:
        falling = self.move_sand()
        #self.draw_cave()
        cycles += 1

      
      if cycles > 0:
        count += 1
        self.sand = [500,0]
        self.cave[500][0] = SAND
        cycles = 0
      else:
        print("END")
        self.can_fall = False
      
    self.log_answer(1, count-1, start)

  def task_2(self):
    start = time()
    self.build_cave()
    self.max_y += 2
    for x in range(self.min_x, self.max_x+1):
      self.cave[x][self.max_y] = ROCK

    #self.draw_cave()
    count = 0
    self.can_fall = True
    
    while self.can_fall:
      falling = True
      cycles = 0
      
      while falling:
        falling = self.move_sand(floor = self.max_y, limit_x=False)
        cycles += 1
        if self.sand == [500, 0]:
          self.can_fall = False

      #self.draw_cave()
      if cycles > 0:
        count += 1
        self.sand = [500,0]
        self.cave[500][0] = SAND
        cycles = 0
      else:
        self.can_fall = False
      
    self.log_answer(2, count, start)

  
