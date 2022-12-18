
from template import Day
from time import time
import re
import numpy as np

class Sensor:

  def __init__(self, sensor, beacon):
    self.px = sensor[0]
    self.py = sensor[1]
    self.bx = beacon[0]
    self.by = beacon[1]
    self.distance = self.calc_distance(self.bx, self.by)

  #@functools.lru_cache(maxsize=128)
  def calc_distance(self, x, y):
    return (abs(x - self.px) + abs(y - self.py))

class Solution(Day):
  
  sensors = []
  beacons = {}
  line_regex = re.compile("Sensor at x=(?P<sensor_x>(-)?\d+), y=(?P<sensor_y>(-)?\d+)\: closest beacon is at x=(?P<beacon_x>(-)?\d+), y=(?P<beacon_y>(-)?\d+)")
  min_x = None
  max_x = None
  min_y = None
  max_y = None

  def __init__(self):
    super().__init__(__file__)

  

  @staticmethod
  def parse_line(line):
    m = Solution.line_regex.match(line.strip())
    result = {}
    for key in m.groupdict():
      result[key] = int(m[key])

    return result

  def check_limits(self, x, y):
    if self.min_x is None or x < self.min_x:
        self.min_x = x
      
    if self.max_x is None or x > self.max_x:
      self.max_x = x

    if self.min_y is None or y < self.min_y:
        self.min_y = y
      
    if self.max_y is None or y > self.max_y:
      self.max_y = y

  #@functools.lru_cache(maxsize=128)
  def is_visible(self, x, y):
    for sensor in self.sensors:

      distance = sensor.distance
      if sensor.calc_distance(x,y) <= distance:
        return False
    return True

  def prep_data(self, data):
    
    for line in data:
      details = self.parse_line(line)
    
      sensor = (details["sensor_x"], details["sensor_y"])
      beacon = (details["beacon_x"], details["beacon_y"])
      self.sensors.append(Sensor(sensor, beacon))
      
      self.check_limits(*sensor)
      self.check_limits(*beacon)

    self.sensors = np.array(self.sensors) 

  def draw_tunnels(self, tunnels):
    for y in range(self.min_y, self.max_y+1):
      row = []
      for x in range(self.min_x, self.max_x+1):
        row.append(tunnels[y][x] if y in tunnels and x in tunnels[y] else ".")

      print(str(y).ljust(3) + "".join(row))

  def task_1(self):
    start = time()
    row = 2000000
    tunnels = {
      row: {}
    }
    
    #sensors = iter(self.sensors)
    for sensor in self.sensors:
      
      if sensor.py not in tunnels:
        tunnels[sensor.py] = {}
      tunnels[sensor.py][sensor.px] = 1
      if sensor.by not in tunnels:
        tunnels[sensor.by] = {}
      tunnels[sensor.by][sensor.bx] = 2    

    sensors = iter(self.sensors)

    while 1:
      try:
        sensor = next(sensors)
      except StopIteration:
        break

      distance = sensor.distance
      '''  min_y, max_y = max(sensor.py-(distance+1), self.min_y), min(sensor.py+(distance+1), self.max_y)

      if min_y > row or max_y < row:
        continue '''

      offset = abs(row-sensor.py)
      start_x, end_x = sensor.px - (distance - offset), sensor.px + (distance - offset)
      for x in range(start_x, end_x+1):
        if row in tunnels and x in tunnels[row]:
          continue
        
        tunnels[row][x] = "#"

    #print(tunnels[row])
    count = sum([1 if tunnels[row][x] == "#" else 0 for x in tunnels[row]])  
    self.log_answer(1, count, start)

  def task_2(self):
    start = time()

    min_coord = 0
    max_coord = 4000000

    locations = []

    def scan_quadrant(sensor, y_offset, x_inc, y_inc, min_coord, max_coord):
      x, y = sensor.px, sensor.py + y_offset
      while 1:
        if max_coord > x >= min_coord and max_coord > y >= min_coord:
          
          if self.is_visible(x, y):
            locations.append((x,y))

        if y == sensor.py:
          break
          
        x += x_inc
        y += y_inc

    for sensor in self.sensors:

      distance = sensor.distance
            
      if (
        sensor.px + distance < min_coord or 
        sensor.px - distance >= max_coord or
        sensor.py + distance < min_coord or 
        sensor.py - distance >= max_coord
      ):
        continue
      
      border_distance = distance + 1
      # Top Right
      scan_quadrant(sensor, -border_distance, 1, 1, min_coord, max_coord)

      # Top Left
      scan_quadrant(sensor, -border_distance, -1, 1, min_coord, max_coord)

      # Bottom Right
      scan_quadrant(sensor, +border_distance, 1, -1, min_coord, max_coord)

      # Bottom Left
      scan_quadrant(sensor, +border_distance, -1, -1, min_coord, max_coord)

    print("LOCATIONS", len(locations), len(set(locations)))
    result = sum([(x[0] * 4000000) + x[1] for x in set(locations)])
    self.log_answer(2, result, start)

  
