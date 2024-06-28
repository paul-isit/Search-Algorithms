import sys
from collections import deque

from utils import *
from Node import *
from Problem import *
import time

class RobotNav(Problem):
  def __init__(self, filename):
    super().__init__(None, None)
    
    self.rows, self.columns, self.start_position, self.goals, self.obstacles, self.individual_obstacle = self.read_data(filename)
    self.initial = self.start_position
    
    if len(self.goals) == 1:
      self.goal = self.goals[0]
    elif len(self.goals) > 1:
      self.goal  = tuple(self.goals)
    else:
      raise ValueError("No goals provided")
    
    self.all_actions = {
      'up': (0, -1),
      'left': (-1, 0),
      'down': (0, 1),
      'right': (1, 0)
    }
    
    
  def create_grid(self):
    self.grid = []

    for y in range(self.rows):
      row = []
      for x in range(self.columns):
        row.append((x, y))
      self.grid.append(row)
    
    startX = self.start_position[0]
    startY = self.start_position[1]
    self.grid[startY][startX] = 'S'
    
    for goal in self.goals:
      goalX = goal[0]
      goalY = goal[1]
      self.grid[goalY][goalX] = 'G'
      
    for obstacle in self.obstacles:
      x = obstacle[0]
      y = obstacle[1]
      width = obstacle[2]
      height = obstacle[3]
      for i in range(height):
        for j in range(width):
          self.grid[y + i][x + j] = '#'
    
    return self.grid

  def print_grid(self):
    for row in self.grid:
      row_str = ''
      for square in row:
        if isinstance(square, tuple):  
          row_str += '. '  
        else:
          row_str += square + ' '  
      print(row_str)
      
  def update_grid(self, result):
    path = []
    gNode = result
    while gNode.parent:
      path.insert(0, gNode)
      gNode = gNode.parent
    
    for node in path:
      x = node.state[0]
      y = node.state[1]
      self.grid[y][x] = 'o'
    
    self.print_grid()
    
  # def update_grid(self, result):
  #   path = []
  #   gNode = result
  #   # if isinstance(gNode, list):
      
  #   while gNode.parent:
  #     path.insert(0, gNode)
  #     gNode = gNode.parent
    
  #   for node in path:
  #     x, y = node.state
  #     self.grid[y][x] = 'o'
  #     time.sleep(0.5)
  #     self.print_grid()
  #     print("\n")

  
  def get_path_action(self, result):
    path = []
    gNode = result
    while gNode.parent:
      for key, val in  self.all_actions.items():
        if val == gNode.action:
          action = key
      path.insert(0,action)
      gNode = gNode.parent
        
    return path
  
  def get_path_key(self, result):
    path = []
    gNode = result
    while gNode.parent:
      for key, val in  self.all_actions.items():
        if val == gNode.action:
          action = val
      path.insert(0,action)
      gNode = gNode.parent
        
    return path
  
  def read_data(self, filename):
    with open(filename, 'r') as f:
      lines = f.readlines()
      
      # getting the grid dimensions
      grid_dimensions = lines[0].strip()[1:-1].split(',')
      rows = int(grid_dimensions[0])
      columns = int(grid_dimensions[1])
      
      if not (rows > 1 and columns > 1):
        raise ValueError("Error! The grid dimensions need to be greater than 1 unit each for x and y axes.")
      
      # getting the starting point
      start_position = tuple(map(int, lines[1].strip()[1:-1].split(',')))
      
      # getting the goal positions
      goals_line = lines[2].strip().split('|')
      goals = []
      for goal in goals_line:
        goals.append(tuple(map(int, goal.strip()[1:-1].split(','))))
        
      # getting the obstacle positions
      obstacles = []
      for line in lines[3:]:
        anObstacle = tuple(map(int, line.strip()[1:-1].split(',')))
        obstacles.append(anObstacle)
      
      # getting the coordinates of individual squares that are blocked
      individual_obstacle = []
      for obstacle in obstacles:
        x = obstacle[0]
        y = obstacle[1]
        width = obstacle[2]
        height = obstacle[3]
        for i in range(height):
          for j in range(width):
            individual_obstacle.append((x + j, y + i))
            
        
      return rows, columns, start_position, goals, obstacles, individual_obstacle
  
  
  
  def h(self, node):
    """Heuristic function for A* search.
    Estimates the cost from the current state to the goal state."""
    x, y = node.state
    if isinstance(self.goal, tuple):
      distances = []
      for goal in self.goals:
        distance = manhattan_distance((x,y), goal)
        distances.append(distance)
        
      heuristic = min(distances)
    else:
      heuristic = manhattan_distance((x,y),self.goal)
    
    return heuristic
    
  def actions(self, state):
    available_actions = []
    
    x = state[0]
    y = state[1]
    
    for value in self.all_actions:
      new_x = x + self.all_actions[value][0]
      new_y = y + self.all_actions[value][1]
      #Checks if the next position is an empty square and within the bounds of the grid
      if(new_x, new_y) not in self.individual_obstacle and 0 <= new_x < self.columns and 0 <= new_y < self.rows:
        available_actions.append((self.all_actions[value][0],self.all_actions[value][1]))
    return available_actions
  
  
  def result(self, state, action):
    x_add, y_add = action
    x, y = state
    next_x, next_y = x + x_add, y + y_add
    return (next_x, next_y)
  
  
  def goal_test(self, state):
    if len(self.goals) > 1:
      return any([goal == state for goal in self.goals])
    else:
      return self.goal == state

