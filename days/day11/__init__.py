
from template import Day
from time import time
import re
from math import floor, prod

class Monkey:
  count = 0
  items = []
  operation = None
  test = None
  actions = {}

  def __init__(self, items, operation, test, actions):
    self.items = items
    self.operation = operation
    self.test = test
    self.actions = actions
    self.count = 0

  def get_worry(self, current):
    self.count += 1
    return self.operation(current)

  def do_test(self, worry):
    return worry % self.test == 0

  def get_target(self, result):
    return self.actions["true" if result else "false"]

class Solution(Day):

  def __init__(self):
    super().__init__(__file__)

  operators = {
    "divisible": "lambda x,y: x % y == 0"
  }

  TEST_REGEX = re.compile("Test: (?P<operation>[a-z]+) by (?P<val>\d+)")
  IF_REGEX = re.compile("If (?P<result>true|false): throw to monkey (?P<target>\d+)")

  @staticmethod
  def parse_monkey(lines):
    items = []
    operation = None
    test = None
    actions = {}
    for line in lines:
      if line.startswith("Starting items: "):
        items = [int(x) for x in line.replace("Starting items: ", "").split(", ")]
      elif line.startswith("Operation: "):
        operation = eval("lambda old: %s" % line.replace("Operation: new = ", ""))
      elif line.startswith("Test: "):
        m = Solution.TEST_REGEX.match(line)
        results = m.groupdict()
        test = float(results["val"])
      elif  line.startswith("If "):
        m = Solution.IF_REGEX.match(line)
        results = m.groupdict()
        actions[results["result"]] = int(results["target"])

    return Monkey(items, operation, test, actions)

  @staticmethod
  def load_monkeys(groups):
    return [Solution.parse_monkey(group) for group in groups]

  @staticmethod
  def do_rounds(monkeys, rounds, worry_operator):
    total_div = 1
    for monkey in monkeys:
      total_div *= monkey.test

    for _ in range(rounds):
      for i, monkey in enumerate(monkeys):
        while len(monkey.items) > 0:
          item = monkey.items.pop(0)
          worry_level = monkey.get_worry(item)
          item = worry_operator(worry_level)
          item %= total_div
          test_result = monkey.do_test(item)
          
          target = monkey.get_target(test_result)
          monkeys[target].items.append(item)

    counts = list(map(lambda x: x.count, monkeys))
    counts.sort(reverse=True)

    return prod(counts[0:2])

  def prep_data(self, data):
    line_groups = []
    for line in data:
      if line.startswith("Monkey"):
        line_groups.append([])
      elif line.strip() != "\n":
        line_groups[-1].append(line.strip())

    self.groups = line_groups
  
  def task_1(self):
    start = time()
    monkeys = self.load_monkeys(self.groups)
    result = self.do_rounds(monkeys, 20, lambda x: floor(x/3))
  
    self.log_answer(1, result, start)

  def task_2(self):
    start = time()
    monkeys = self.load_monkeys(self.groups)
    result = self.do_rounds(monkeys, 10000, lambda x: x)
    
    self.log_answer(2, result, start)

  
