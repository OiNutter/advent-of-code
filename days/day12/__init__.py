
from template import Day
from time import time
from heapq import *
import itertools

class Coord:
  x = 0
  y = 0

  def __init__(self, x, y):
    self.x = x
    self.y = y

class PriorityQueue(object):

  REMOVED = "<removed-task>"

  def __init__(self):
    self.queue = []
    self.mapping = {}
    self.counter = itertools.count()

  def __str__(self):
    return ' '.join([str(i) for i in self.queue])

  # for checking if the queue is empty
  def isEmpty(self):
    return len(self.queue) == 0

  # for inserting an element in the queue
  def insert(self, item, priority=0):
    if item in self.mapping:
      self.remove(item)
    count = next(self.counter)
    entry = [priority, count, item]
    self.mapping[item] = entry
    heappush(self.queue, entry)

  def remove(self, item):
    entry = self.mapping.pop(item)
    entry[-1] = self.REMOVED

  def pop(self):
    while self.queue:
      priority, count, item = heappop(self.queue)
      if item is not self.REMOVED:
        del self.mapping[item]
        return item
    raise KeyError("pop from an empty priority queue")

  
class Solution(Day):
  relief_map = None

  def __init__(self):
    super().__init__(__file__)

  def build_map(self, lines):
    relief_map = []
    start = None
    for i, line in enumerate(lines):
      relief_map.append([])
      for n, char in enumerate(line.strip()):
        relief_map[i].append((Coord(n,i), char))

    relief_map = list(zip(*relief_map))

    return relief_map

  def get_height(self, char):
    if char == "S":
      char = "a"
    elif char == "E":
      char = "z"

    return ord(char)

  def get_neighbours(self, current):
    min_x = max(current.x - 1,0)
    max_x = min(current.x + 1, len(self.relief_map)-1)
    min_y = max(current.y - 1, 0)
    max_y = min(current.y + 1, len(self.relief_map[0])-1)

    current_height = self.get_height(self.relief_map[current.x][current.y][1])
    neighbours = []
    for x in range(min_x, max_x+1):
      if x == current.x:
        continue

      new_height = self.get_height(self.relief_map[x][current.y][1])

      if new_height <= current_height+1:
        neighbours.append(self.relief_map[x][current.y][0])

    for y in range(min_y, max_y+1):
      if y == current.y:
        continue

      new_height = self.get_height(self.relief_map[current.x][y][1])

      if new_height <= current_height+1:
        neighbours.append(self.relief_map[current.x][y][0])

    return neighbours

  def djikstra(self, start, end):
    distances = {}
    queue = PriorityQueue()
    target = None

    for x, row in enumerate(self.relief_map):
      for y, val in enumerate(row):
        point = val[0]
        distances[point] =  0 if val[1] in start else float('inf')
        queue.insert(point, distances[point])
        if val[1] in end:
          target = val[0]

    while not queue.isEmpty():
      current = queue.pop()
      if current == target:
        break

      for n in self.get_neighbours(current):
        alt = distances[current] + 1
        if alt < distances[n]:
          distances[n] = alt
          queue.insert(n, alt)

    return distances[target]

  def prep_data(self, data):
    self.relief_map = self.build_map(data)

  def task_1(self):
    start = time()
    shortest = self.djikstra(["S"], ["E"])
    self.log_answer(1, shortest, start)

  def task_2(self):
    start = time()
    shortest = self.djikstra(["a","S"], ["E"])
    self.log_answer(2, shortest, start)

  
