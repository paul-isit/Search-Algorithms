import sys
from collections import deque

from utils import *

class Problem:
  
  def  __init__(self, initial, goal=None):
    self.initial = initial
    self.goal = goal
    
  def actions(self, state):
    raise NotImplementedError
    
  def result(self, state, action):
    raise NotImplementedError
    
  def goal_test(self, state):
    if isinstance(self.goal, list):
        return is_in(state, self.goal)
    else:
        return state == self.goal
    #override the method if there are more than  one possible goals
    
  def path_cost(self, c, state1, action, state2):
    """Return the cost of a solution path that arrives at state2 from
    state1 via action, assuming cost c to get up to state1. If the problem
    is such that the path doesn't matter, this function will only look at
    state2. If the path does matter, it will consider c and maybe state1
    and action. The default method costs 1 for every step in the path."""
    return c + 1
    
    
  def value(self, state):
    raise NotImplementedError
