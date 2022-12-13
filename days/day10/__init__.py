import re
from template import Day
from time import time

class Solution(Day):

  commands = []
  strengths = []
  rows = []
  SCREEN_WIDTH = 40
  COMMAND_REGEX = re.compile("(?P<noop>noop)|((?P<add>addx) (?P<val>-?\d+))")
  X = 1

  def __init__(self):
    super().__init__(__file__)

  @staticmethod
  def parse_command(line):
    m = Solution.COMMAND_REGEX.match(line)
    result = m.groupdict()
    if result["noop"]:
      return {
        "cmd": "noop"
      }
    elif result["add"]: 
      return {
        "cmd": "add",
        "val": int(result["val"])
      }

  def do_command(self, cmd):
    if cmd["cmd"] == "add":
      self.X += cmd["val"]

  def prep_data(self, data):
    for line in data:
      self.commands.append(self.parse_command(line.strip()))

    self.run_commands()
  
  def run_commands(self):
    to_execute = []
    milestone = 20
    
    
    cycle = 1
    row = []
    
    while len(self.commands) > 0:
      if cycle == milestone:
        self.strengths.append(cycle*self.X)
        milestone += 40

      cycle += 1

      if len(to_execute) > 0:
        cmd = to_execute.pop(0)
        self.do_command(cmd)
        self.commands.pop(0)
      else:
        cmd = self.commands[0]
        if cmd["cmd"] == "add":
          to_execute.append(cmd)
        else:
          self.commands.pop(0)

      i = len(row)+1
      row.append("#" if (i) >= self.X-1 and (i) <= self.X+1 else ".")
      if len(row) == self.SCREEN_WIDTH:
        self.rows.append(row)
        row = []
        
  def task_1(self):
    start = time()
    self.log_answer(1, sum(self.strengths), start)

  def task_2(self):
    start = time()
    print("The answer to task 2 is:\n")
    for row in self.rows:
      print("".join(row))

    self.log_time(start)
