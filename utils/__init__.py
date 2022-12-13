def load(filename):
  lines = []
  with open(filename, "r") as data:
    for line in data:
      lines.append(line)

  return lines