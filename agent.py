import random

class Agent:

  def __init__(self, simulation, cell, strategy, ptr, group):
    self.simulation = simulation
    self.cell = cell
    self.strategy = strategy
    self.ptr = ptr
    self.base_ptr = ptr
    self.group = group

  def reset_ptr(self):
    self.ptr = self.base_ptr
  
  def get_strategy(self):
    return self.strategy

  def get_code(self):
    if self.strategy == "altruist":
      return "A" + format(self.group)
    elif self.strategy == "ethnocentric":
      return "E" + format(self.group)
    elif self.strategy == "cosmopolitan":
      return "C" + format(self.group)
    else:
      return "S" + format(self.group)

  def is_cooperate(self, other):
    if self.strategy == "altruist":
      return True
    elif self.strategy == "cosmopolitan" and other.group != self.group:
      return True
    elif self.strategy == "ethnocentric" and other.group == self.group:
      return True
    else:
      return False

  def prisoner_dilemma(self, other):
    if self.is_cooperate(other):
      self.ptr -= self.simulation.get_config().cost
    if not other.is_cooperate(self):
      self.ptr -= self.simulation.get_config().benefit

  def interaction(self):
    cells = self.get_neighbour_cells()

    for cell in cells:
      self.prisoner_dilemma(cell.get_agent())

  def reproduce(self):
    if random.random() < self.ptr:
      cells = self.get_neighbour_cells(True)
      if len(cells) > 0:
        cell = random.sample(cells, 1)[0]
        cell.set_agent(Agent(self.simulation, cell, self.strategy, self.simulation.get_config().base_ptr, self.group))
        self.simulation.agents.append(cell.get_agent())
  
  def get_neighbour_cells(self, empty = False):
    coords_neighbours = self.simulation.get_map().get_neighbour_coordinates(self.cell.x, self.cell.y)

    neighbours = []
    for coords in coords_neighbours:
      cell = self.simulation.get_map().get_cell(coords[0], coords[1])
      if cell.is_empty() == empty:
        neighbours.append(cell)

    return neighbours
