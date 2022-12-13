import re
from template import Day
from time import time

class Directory:

  def __init__(self, name, parent, files = [], size= 0):
    self.name = name
    self.parent = parent
    self.files = files.copy()
    self.size = size

class File:

  def __init__(self, name, size):
    self.name = name
    self.size = size

class Solution(Day):
  command_regex = re.compile("\$ (?P<cmd>(cd|ls))( (?P<args>[a-z0-9/.]+))?", re.IGNORECASE)
  dir_regex = re.compile("dir (?P<dir>[a-z0-9]+)", re.IGNORECASE)
  file_regex = re.compile("(?P<size>[0-9]+) (?P<name>[a-z0-9.]+)")
  filesystem = [Directory("/",None)]

  def __init__(self):
    super().__init__(__file__)

  def prep_data(self, data):
    current = 0
    for line in data:
      output = Solution.parse_line(line)

      if output["type"] == "COMMAND":
        current = self.run_command(output["cmd"], output["args"], current)
      elif output["type"] == "DIR":
        self.filesystem.append(
          Directory(
            output["dir"],
            current
          )
        )
      elif output["type"] == "FILE":
        self.filesystem[current].files.append(
          File(
            output["name"],
            output["size"]
          )
        )

   
    self.calc_sizes()
  
  @staticmethod
  def parse_command(line):
    m = Solution.command_regex.match(line)
    result = {
      "type": "COMMAND"
    }
    result.update(m.groupdict())
    return result

  @staticmethod
  def parse_dir(line):
    m = Solution.dir_regex.match(line)
    result = {
      "type": "DIR"
    }
    result.update(m.groupdict())
    return result

  @staticmethod
  def parse_file(line):
    m = Solution.file_regex.match(line)
    result = {
      "type": "FILE"
    }
    result.update(m.groupdict())
    result["size"] = int(result["size"])
    return result

  @staticmethod
  def parse_line(line):
    if line.startswith("$"):
      return Solution.parse_command(line)
    elif line.startswith("dir"):
      return Solution.parse_dir(line)
    else:
      return Solution.parse_file(line)

  def find_dir(self, name, current):
    return next((i for i, x in enumerate(self.filesystem) if x.name == name and (x.parent == current or x.parent is None)), None)

  def run_command(self, cmd, args, current):
    if cmd == "cd":
      if args == "..":
        return self.filesystem[current].parent
      elif args != ".":
        return self.find_dir(args, current)
    
    return current

  def calc_sizes(self):
    for d in reversed(self.filesystem):
      for f in d.files:
        d.size += f.size

      if d.parent is not None:
        self.filesystem[d.parent].size += d.size

  def task_1(self):
    start = time()
    SIZE_LIMIT = 100000

    sizes = []
    for d in self.filesystem:
      if d.size <= SIZE_LIMIT:
        sizes.append(d.size)

    self.log_answer(1, sum(sizes), start)

  def task_2(self):
    start = time()
    TOTAL_SIZE = 70000000
    NEEDED_SIZE = 30000000
    to_remove = self.filesystem[0]
    total_free = TOTAL_SIZE - self.filesystem[0].size
    to_free = NEEDED_SIZE - total_free

    for d in self.filesystem:
      if d.size >= to_free and d.size < to_remove.size:
        to_remove = d

    self.log_answer(2, to_remove.size, start)