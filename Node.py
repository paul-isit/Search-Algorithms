import sys
from collections import deque

from utils import *

class Node:
  def  __init__(self, state, parent=None, action=None, path_cost=0):
    self.state = state
    self.parent = parent
    self.action = action
    self.path_cost = path_cost
    self.depth = 0
    if parent:
      self.depth = parent.depth + 1
      
  def __repr__(self):
    return  "<Node {}>".format(self.state)
  
  def __lt__(self, node):
    return self.state < node.state
  
  
  def expand(self, problem):
    expansion = []
    for action in problem.actions(self.state):
        child = self.child_node(problem, action)
        expansion.append(child)
    return expansion

  
  def  child_node(self, problem, action):
    next_state = problem.result(self.state, action)
    next_node = Node(next_state, self, action, self.path_cost + problem.path_cost(0, self.state, action, next_state))
    return next_node
  
  def solution(self):
    return [node.action for node in self.path()[1:]]
  
  def path(self):
    node, path_back = self, []
    
    while node:
      path_back.append(node.state)
      node = node.parent
    return list(reversed(path_back))
  
  def __eq__(self, other):
    return isinstance(other, Node) and self.state == other.state
   
  def __hash__(self):
    return hash(self.state)