from template import Day
from time import time

class Solution(Day):

  def __init__(self):
    super().__init__(__file__)

  def prep_data(self, data):
    pairs = []
    for line in data:
      pairs.append(self.get_zones(line))

    self.pairs = pairs
  
  def get_zones(self, line):
    pairs = []
    for col in line.strip().split(','):
      (start,end) = col.split("-")
      pairs.append({"start": int(start), "stop": int(end)})

    return pairs

  def find_overlaps(self, check_overlap):
    overlaps = 0
    for ranges in self.pairs:
      overlap = check_overlap(ranges)
      overlaps += 1 if overlap else 0

    return overlaps

  def task_1(self):
    start = time()
    def check_overlap(ranges):
      return(
        (
          (
            ranges[0]["start"] >= ranges[1]["start"] and 
            ranges[0]["start"] <= ranges[1]["stop"]
          ) 
          and
          (
            ranges[0]["stop"] >= ranges[1]["start"] and
            ranges[0]["stop"] <= ranges[1]["stop"]
          )
        )
        or
        ( 
          (
            ranges[1]["start"] >= ranges[0]["start"] and 
            ranges[1]["start"] <= ranges[0]["stop"]
          )
          and
          (
            ranges[1]["stop"] >= ranges[0]["start"] and
            ranges[1]["stop"] <= ranges[0]["stop"]
          )
        )
      )
    overlaps = self.find_overlaps(check_overlap)

    self.log_answer(1, overlaps, start)

  def task_2(self):
    start = time()
    def check_overlap(ranges):
      return(
        (
          ranges[0]["start"] >= ranges[1]["start"] and 
          ranges[0]["start"] <= ranges[1]["stop"]
        ) 
        or
        (
          ranges[0]["stop"] >= ranges[1]["start"] and
          ranges[0]["stop"] <= ranges[1]["stop"]
        )
        or 
        (
          ranges[1]["start"] >= ranges[0]["start"] and 
          ranges[1]["start"] <= ranges[0]["stop"]
        )
        or
        (
          ranges[1]["stop"] >= ranges[0]["start"] and
          ranges[1]["stop"] <= ranges[0]["stop"]
        )
      )
    overlaps = self.find_overlaps(check_overlap)

    self.log_answer(2, overlaps, start)