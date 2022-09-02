import sys
from ActionManager.jscompat.convert import dump
from ActionManager import jprint

if __name__ == '__main__':
  for obj in dump(sys.stdin.read()):
    print('==========')
    print('Executed an object:')
    print('Operation:')
    print(obj[0])
    print('Descriptor:')
    jprint(obj[1])