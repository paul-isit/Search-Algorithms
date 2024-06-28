import tkinter as tk
from tkinter import filedialog, messagebox
from RobotNavigation import RobotNav
from algorithms import *
import time

class RobotNavGUI:
    def __init__(self, master, filename, algorithm):
        self.master = master
        master.title("Robot Navigation")

        self.algorithm_var = tk.StringVar(value=algorithm)
        self.filename_var = tk.StringVar(value=filename)
        self.result_var = tk.StringVar()
        self.nodes_explored_var = tk.StringVar()
        self.path_var = tk.StringVar()
        self.stop_search = False

        self.create_widgets()

    def create_widgets(self):
        # Algorithm selection
        algorithm_label = tk.Label(self.master, text="Select Algorithm:")
        algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        algorithm_options = ["bfs", "dfs", "gbfs", "astar", "iddfs", "idastar"]
        algorithm_dropdown = tk.OptionMenu(self.master, self.algorithm_var, *algorithm_options)
        algorithm_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # File input
        filename_label = tk.Label(self.master, text="Enter File Name:")
        filename_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        filename_entry = tk.Entry(self.master, textvariable=self.filename_var)
        filename_entry.grid(row=1, column=1, padx=5, pady=5)


        # Play/Pause button
        self.play_button = tk.Button(self.master, text="Play", command=self.toggle_play_pause)
        self.play_button.grid(row=2, column=0, padx=5, pady=5)

        # Grid display
        self.grid_canvas = tk.Canvas(self.master)
        self.grid_canvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Configure grid weights to allow resizing
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Result display
        result_label = tk.Label(self.master, text="")
        result_label.grid(row=4, column=0, padx=0, pady=0, sticky="w")

        self.result_text = tk.Text(self.master, wrap=tk.WORD)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configure grid weights for result text
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Bind canvas to window resizing
        self.master.bind("<Configure>", self.resize_grid)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.filename_var.set(filename)

    def toggle_play_pause(self):
      if self.play_button["text"] == "Play":
          self.play_button["text"] = "Pause"
          self.stop_search = False
          self.run_search()
      else:
          if self.grid_canvas.winfo_exists():
              messagebox.showinfo("Info", "Search cannot be paused midway through.")
          else:
              self.play_button["text"] = "Play"
              self.stop_search = True


    def run_search(self):
      filename = self.filename_var.get()
      algorithm = self.algorithm_var.get()

      if filename:
          try:
              problem = RobotNav(filename)
              self.draw_grid(problem)

              if algorithm == "bfs":
                  result, nodes_explored = breadth_first_search(problem)
              elif algorithm == "dfs":
                  result, nodes_explored = depth_first_graph_search(problem)
              elif algorithm == "gbfs":
                  result, nodes_explored = greedy_best_first_graph_search(problem)
              elif algorithm == "astar":
                  result, nodes_explored = astar_search(problem)
              elif algorithm == 'iddfs':
                  result, nodes_explored = iterative_deepening_depth_first_search(problem)
              elif algorithm == "idastar":
                  result, nodes_explored = iterative_deepening_astar_search(problem)
              print(f"{filename} {algorithm}")
              if result is not None:
                  path = problem.get_path_action(result)
                  self.display_result(result, len(nodes_explored), path)
                  self.draw_path(problem, nodes_explored, result)
                  self.play_button["text"] = "Play"
                  
                  
                  path = problem.get_path_action(result)
                  print(f"{result} {len(nodes_explored)}\n{path}")
                  
                    
              else:
                  print(f"No goal is reachable; {len(nodes_explored)}")
                  if not self.stop_search:
                      messagebox.showinfo("Result", "No goal is reachable.")
          except FileNotFoundError:
              messagebox.showerror("Error", "File not found.")
      else:
          messagebox.showwarning("Warning", "Please enter a file name.")

    def draw_grid(self, problem):
        self.grid_canvas.delete("all")
        rows, cols = problem.rows, problem.columns
        cell_width = self.grid_canvas.winfo_width() // cols
        cell_height = self.grid_canvas.winfo_height() // rows

        for i in range(rows):
            for j in range(cols):
                x1, y1 = j * cell_width, i * cell_height
                x2, y2 = (j + 1) * cell_width, (i + 1) * cell_height
                if (j, i) == problem.start_position:
                    self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                elif (j, i) in problem.goals:
                    self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="red")
                elif (j, i) in problem.individual_obstacle:
                    self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                else:
                    self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white")


    def draw_path(self, problem, nodes_explored, result):
      cell_width = self.grid_canvas.winfo_width() // problem.columns
      cell_height = self.grid_canvas.winfo_height() // problem.rows

      if self.grid_canvas.winfo_exists():
          path_set = problem.get_path_key(result)
          path = result.path()
          current_position = problem.start_position

          for cell in nodes_explored:
              if isinstance(cell, tuple):
                  x, y = cell
              else:
                  x, y = cell.state
              x1, y1 = x * cell_width, y * cell_height
              x2, y2 = (x + 1) * cell_width, (y + 1) * cell_height

              if (x, y) == current_position:
                  self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

                  if current_position != problem.start_position:
                      self.grid_canvas.update()
                      time.sleep(0.3)  # Delay between each move (in seconds)

                  if tuple(current_position) in path:
                      index = path.index(tuple(current_position))
                      if index < len(path_set):
                          action = path_set[index]

                          if action == (0, -1):
                              current_position = (current_position[0], current_position[1] - 1)
                          elif action == (0, 1):
                              current_position = (current_position[0], current_position[1] + 1)
                          elif action == (-1, 0):
                              current_position = (current_position[0] - 1, current_position[1])
                          elif action == (1, 0):
                              current_position = (current_position[0] + 1, current_position[1])

              else:
                  self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")

              self.grid_canvas.update()
              time.sleep(0.3)  # Delay between each explored cell (in seconds)

    def display_result(self, result, nodes_explored, path):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"{self.filename_var.get()} {self.algorithm_var.get()}\n")
        self.result_text.insert(tk.END, f"{result} {nodes_explored}\n")
        self.result_text.insert(tk.END, f"{path}\n")

    def resize_grid(self, event):
      filename = self.filename_var.get()
      if filename:
          try:
              problem = RobotNav(filename)
              self.grid_canvas.delete("all")
              self.draw_grid(problem)
          except FileNotFoundError:
              pass
