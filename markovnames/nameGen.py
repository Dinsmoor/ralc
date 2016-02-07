# forked from https://github.com/AlexeyMK/markov-baby-names/blob/master/markovbaby.py

import random

from collections import defaultdict

WORD_SEP = ' '

class MarkovName:
  def __init__(self, input_list):
    """ input file should have one name per line"""
    # markov chain is a dictionary from {(letter) to list-of-letters-seen-after}
    # {c: 'aaoehhhhh   '}
    self.chain = defaultdict(list)
    names = (line for line in input_list if not line[0] == '#')
    for name in names:
      # Alice
      proper_name = name.lower().strip()
      # alice
      pairs = zip(proper_name, proper_name[1:])
      #pairs = [(a,l), (l, i), (i, c), (c, e)]
      for first, second in pairs:
          self.chain[first].append(second)
      # +1 for e as last character
      self.chain[proper_name[-1]].append(WORD_SEP)
      # +1 for a as first character
      self.chain[WORD_SEP].append(proper_name[0])

  def generate_name(self):
    name = []
    current = WORD_SEP  # used to mark both first and last character
    while not (current == WORD_SEP and name):
      current = random.choice(self.chain[current])
      name.append(current)

    return ''.join(name).strip().capitalize()


def get_name(names_list):
    chain = MarkovName(names_list)
    name = ''
    while len(name) < 3 or len(name) > 15:
        name = chain.generate_name()
    return name

