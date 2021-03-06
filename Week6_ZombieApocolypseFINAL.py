"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
        self._boundary = []
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        self._zombie_list = []
        self._human_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for _zombie in self._zombie_list:
            yield _zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        #print self._human_list
        
        for _human in self._human_list:
            #print _human
            yield _human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        self._visited = poc_grid.Grid(self._grid_height,self._grid_width)
        self._distance_field = [[0 for _i in range(self._grid_width)] for _j in range(self._grid_height)]
        if entity_type == HUMAN:
            for _human in self._human_list:
                self._boundary.append(_human)
                self._visited.set_full(_human[0],_human[1])
                
        if entity_type == ZOMBIE:
            for _zombie in self._zombie_list:
                self._boundary.append(_zombie)
                self._visited.set_full(_zombie[0],_zombie[1])
        #handle obstacles, insert 600 as number         
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self.is_empty(row,col) == False:
                    self._visited.set_full(row,col)
                    self._distance_field[row][col] = 600       
        while len(self._boundary) != 0:
            current_cell = self._boundary.pop(0)
            neighbors = self.four_neighbors(current_cell[0],current_cell[1])
            for neighbor in neighbors:
                if self._visited.is_empty(neighbor[0],neighbor[1]):
                    self._visited.set_full(neighbor[0],neighbor[1])
                    self._boundary.append((neighbor[0],neighbor[1]))
                    self._distance_field[neighbor[0]][neighbor[1]] = self._distance_field[current_cell[0]][current_cell[1]] + 1
        
        
        for dummy_n in range(0,self._grid_height):
            print(self._distance_field[dummy_n])
        return self._distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for dummy_humans in range(0,len(self._human_list)):
            current_human = self._human_list.pop(0)
            neighbors = self.eight_neighbors(current_human[0],current_human[1])
            best_choice = 0
            best_neighbor = None
            for neighbor in neighbors:
                if zombie_distance_field[neighbor[0]][neighbor[1]] > best_choice and self.is_empty(neighbor[0],neighbor[1])==True:
                    best_choice = zombie_distance_field[neighbor[0]][neighbor[1]]
                    best_neighbor = neighbor
            if best_choice > 0:
                self._human_list.append(best_neighbor)
            else:
                self._human_list.append(current_human)
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for dummy_zombies in range(0,len(self._zombie_list)):
            current_zombie = self._zombie_list.pop(0)
            neighbors = self.four_neighbors(current_zombie[0],current_zombie[1])
            current_choice = human_distance_field[current_zombie[0]][current_zombie[1]]
            best_neighbor = None
            better_found = False
            for neighbor in neighbors:
                if human_distance_field[neighbor[0]][neighbor[1]] < current_choice and self.is_empty(neighbor[0],neighbor[1]) == True:
                    better_found = True
                    current_choice = human_distance_field[neighbor[0]][neighbor[1]]
                    best_neighbor = neighbor
            if better_found == False:
                self._zombie_list.append(current_zombie)
            else:
                self._zombie_list.append(best_neighbor)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [(12, 12), (7, 12)], [])
#obj.compute_distance_field(ZOMBIE) 




#poc_zombie_gui.run_gui(Apocalypse(30, 30))
