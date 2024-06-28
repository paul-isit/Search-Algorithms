import sys
from collections import deque

from utils import *
from Node import *
from Problem import *
from RobotNavigation import *
from algorithms import *
from RobotNavGUI import *


def main():

  if(len(sys.argv) != 3):
    print("Please follow the following format to run the program\npython \"path_to_your_python_script\" <filename> <method>")
  else:
    filename = sys.argv[1]
    algorithm = sys.argv[2]
    
    try:
      
      root = tk.Tk()
      robot_nav_gui = RobotNavGUI(root, filename, algorithm)
      root.mainloop()
      
    except FileNotFoundError:
        print("File not found. Please make sure the filename is correct.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
