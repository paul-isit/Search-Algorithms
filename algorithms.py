import sys
from collections import deque

from utils import *
from Node import *
from Problem import *

# Breadth first Search Algorithm

def breadth_first_search(problem):
  frontier = deque([Node(problem.initial)] )
  explored = []
  while frontier:
    node = frontier.popleft()
    explored.append(node.state)
    
    if problem.goal_test(node.state):
      return node, explored
    for child in node.expand(problem):
      if child.state not in explored and child not in frontier:
        frontier.append(child)
  return None, explored



# Depth First Graph Search Algorithm

def depth_first_graph_search(problem):
  frontier = [Node(problem.initial)]
  
  explored = []
  
  while frontier:
    node = frontier.pop()
    explored.append(node.state)
    if problem.goal_test(node.state):
      return node, explored
    for child in node.expand(problem):
      if child.state not in explored and child not in frontier:
        frontier.append(child)
  return None, explored


# Best First Graph Search Algorithm
def best_first_graph_search(problem, f, display=False):
  f = memoize(f, 'f')
  node = Node(problem.initial)
  frontier = PriorityQueue('min', f)
  frontier.append(node)
  explored = []
  while frontier:
    node = frontier.pop()
    if problem.goal_test(node.state):
        if display:
            print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
        return node, explored
    explored.append(node.state)
    for child in node.expand(problem):
        if child.state not in explored and child not in frontier:
            frontier.append(child)
        elif child in frontier:
            if f(child) < frontier[child]:
                del frontier[child]
                frontier.append(child)
  return None, explored

# Greedy Best First Graph Search Algorithm
def greedy_best_first_graph_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h, display)

# A* Search Algorithm
def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def recursive_dls(node, problem, limit, explored):
  if problem.goal_test(node.state):
    return node
  elif limit == 0:
    return 'cutoff'
  else:
    cutoff_occurred = False
    if node.state not in explored :
      for child in node.expand(problem):
        explored.append(node.state)
        result = recursive_dls(child, problem, limit - 1, explored)
        if result == 'cutoff':
            cutoff_occurred = True
        elif result is not None:
          return result
      if cutoff_occurred:
        return 'cutoff'
      else:
        return None

# Depth Limited Search Algorithm
def depth_limited_search(problem, limit=50):
    explored = []
    root = Node(problem.initial)
    result = recursive_dls(root, problem, limit, explored)
    return result, explored

# Iterative Deepening Depth First Search Algorithm
def iterative_deepening_depth_first_search(problem):
    for depth in range(sys.maxsize):
        result, nodes_explored = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result, nodes_explored

# Iterative Deepening A* Search algorithm
def iterative_deepening_astar_search(problem):
    def recursive_ida(node, problem, limit, explored):
        if problem.goal_test(node.state):
            return node, 0
        elif node.path_cost + problem.h(node) > limit:
            return None, node.path_cost + problem.h(node)
        else:
            min_cutoff = float('inf')
            for child in node.expand(problem):
                if child.state not in explored:
                    explored.append(child.state)
                    result, child_cost = recursive_ida(child, problem, limit, explored)
                    if result is not None:
                        return result, 0
                    elif child_cost > limit:
                        min_cutoff = min(min_cutoff, child_cost)
            return None, min_cutoff

    explored = []
    root = Node(problem.initial)
    limit = problem.h(root)
    while True:
        explored.clear()
        result, cost = recursive_ida(root, problem, limit, explored)
        if result is not None:
            return result, explored
        elif cost == float('inf'):
            return None, explored
        else:
            limit = cost
