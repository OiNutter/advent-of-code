import os

dir = os.path.dirname(os.path.abspath(__file__))
modules = [os.path.splitext(_file)[0] for _file in os.listdir(dir) if not _file.startswith('__')]

days = []
for mod in modules:
    exec('from days import {}; days.append({})'.format(mod, mod))