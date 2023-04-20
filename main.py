from random import randint
from math import floor
from copy import deepcopy
import matplotlib.pyplot as plt

def grid_init(n=10, m=10):
  grid = []
  for i in range(n):
    grid.append([])
    for j in range(m):
      grid[i].append(randint(1, 4))
  return grid


def grid_display(grid):
  for row in grid:
    print(row)


def grid_display2(grid):
  for i in range(len(grid)):
    text = ""
    for j in range(len(grid[i])):
      text += " " + str(grid[i][j])
    print(text)


def grid_convert_display(grid):
  newgrid = []
  for i in range(len(grid)):
    newgrid.append([])
    for j in range(len(grid[1])):
      if grid[i][j] == 1 or grid[i][j] == "1":
        newgrid[i].append('\u001b[31m' + "●" + '\033[0m')
      elif grid[i][j] == 2 or grid[i][j] == "2":
        newgrid[i].append('\u001b[32m' + "●" + '\033[0m')
      elif grid[i][j] == 3 or grid[i][j] == "3":
        newgrid[i].append('\u001b[34m' + "●" + '\033[0m')
      elif grid[i][j] == 4 or grid[i][j] == "4":
        newgrid[i].append('\u001b[35m' + "●" + '\033[0m')
      else:
        newgrid[i].append(grid[i][j])
  grid_display2(newgrid)

def grid_display(grid, nb_type_candies):
  """
  Displays the game grid "grid" containing at least
  maximum "nb_type_candies" different colors of candies.
  """
  plt.imshow(grid, vmin=0, vmax=nb_type_candies-1, cmap='jet')
  plt.pause(0.1)
  plt.draw()
  plt.pause(0.1)


def create_new_candy(grid):
  '''
  from the grid, find the zeroes and replace them with color numbers
  '''
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == 0:
        grid[i][j] = randint(1, 4)
  return grid


def detect_candy_combinaison(grid):
  new_grid = deepcopy(grid)
  combi_list = []
  for i in range(len(new_grid) - 1):
    for j in range(len(new_grid[i]) - 1):
      swap_candies(new_grid, (i, j), (i, j + 1))
      if len(detect_coordinate_combinaison2(i, j, new_grid)) == 0 or len(
          detect_coordinate_combinaison2(i, j + 1, new_grid)) == 0:
        combi_list.append(True)
      else:
        combi_list.append(False)
      swap_candies(new_grid, (i, j + 1), (i, j))

      swap_candies(new_grid, (i, j), (i + 1, j))
      if len(detect_coordinate_combinaison2(i, j, new_grid)) == 0 or len(
          detect_coordinate_combinaison2(i + 1, j, new_grid)):
        combi_list.append(True)
      else:
        combi_list.append(False)
      swap_candies(new_grid, (i, j + 1), (i + 1, j))

  end = True
  for combi in combi_list:
    if combi == False:
      end = False
  return end


def detect_coordinate_combinaison2(i, j, grid):
  color = grid[i][j]
  combi_list = []
  j2 = j
  i2 = i
  changej = 0
  changei = 0

  while j2 < (len(grid[i]) - 1) and color == grid[i][j2 + 1]:
    j2 += 1
    changej += 1

  j2 = j
  while j2 > 0 and color == grid[i][j2 - 1]:
    j2 -= 1
    changej += 1

  j2 = j
  while i2 < (len(grid) - 1) and color == grid[i2 + 1][j2]:
    i2 += 1
    changei += 1

  i2 = i
  while i2 > 0 and color == grid[i2 - 1][j2]:
    i2 -= 1
    changei += 1

  if changei >= 2 or changej >= 2:
    combi_list = floodcandy(i, j, grid)
  else:
    combi_list = []

  return combi_list


def floodcandy(x, y, grid):

  combi_list = [] #THERE IS SOME ISSUE HERE IDK WHAT THE HELL
  color = grid[x][y]

  queued = [[x, y]]

  while len(queued) > 0:
    x = queued[0][0]
    y = queued[0][1]

    combi_list.append([x, y])
    queued.remove(queued[0])

    cellcheck = \
      [[x, y + 1],
      [x - 1, y], [x + 1, y],
      [x, y - 1]
      ]
    for elem in cellcheck:
      if (0 <= elem[0]) and (elem[0] < len(grid)) and (0 <= elem[1]) and (
          elem[1] < len(grid[x])):
        if grid[elem[0]][elem[
            1]] == color and elem not in queued and elem not in combi_list:
          queued.append(elem)

  return combi_list


"""
  combi_list = [tuple(t) for t in combi_list]

  combiset = set(combi_list)

  combi_list = [list(t) for t in combiset]  

  return list(set(combi_list))
"""


def check_all_value(grid):
  big_list = []
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if [i, j] not in big_list:
        big_list += detect_coordinate_combinaison2(i, j, grid)
  return big_list


"""
  combi_list = [tuple(t) for t in big_list]

  combiset = set(combi_list)

  combi_list = [list(t) for t in combiset]  
  
  return list(set(combi_list))
"""


def player_input():
  xmove_1, ymove_1 = input('Enter the coordinates of 1st candy:').split()
  xmove_2, ymove_2 = input('Enter the coordinates of 2nd candy:').split()
  xmove_1,ymove_1,xmove_2,ymove_2 =  int(xmove_1),int(ymove_1),int(xmove_2),int(ymove_2)
  move = [[xmove_1, ymove_1], [xmove_2, ymove_2]]
  return move


def player_move(grid):
  move = player_input()
  if (move[0][0] >= len(grid)) or (move[0][1] >= len(grid)) or (
      move[1][0] >= len(grid)) or (move[1][1] >= len(grid)):
    print('Your move is out of table, please do it again')
    move = player_input()
  elif (move[0][0] < 0) or (move[0][1] < 0) or (move[1][0] < 0) or (move[1][1]
                                                                    < 0):
    print('Your move is so small that we can not do it, please do it again')
    move = player_input()
  elif (abs(move[0][0] - move[1][0]) >= 1) and (abs(move[0][1] - move[1][1]) >=
                                                1) or ((abs(move[0][0] - move[1][0]) == 1) and (abs(move[0][1] - move[1][1]) ==
                                                1)):
    print('You made an invalid move, please do it again')
    move = player_input()
  return move


def swap_candies(grid, coord1, coord2):
  save = grid[coord1[0]][coord1[1]]
  grid[coord1[0]][coord1[1]] = grid[coord2[0]][coord2[1]]
  grid[coord2[0]][coord2[1]] = save

  return grid


def replace_candy(grid, coord, color):
  grid[coord[0]][coord[1]] = color


def move_candy(grid):
  for j in range(len(grid) - 1, -1, -1):
    row_check = len(grid) - 1
    count = 0
    while (row_check >= 0):
      if grid[row_check][j] == 0:
        count += 1
        row_check -= 1
      elif grid[row_check][j] != 0:
        grid[row_check][j], grid[row_check +
                                 count][j] = grid[row_check +
                                                  count][j], grid[row_check][j]
        row_check -= 1


def score(combi):
  score = 2.7**(len(combi) / 3)
  return score


########### main ###########
test_grid = grid_init(5, 5)
# grid_display(test_grid, 5)
grid_convert_display(test_grid)
print()

while not detect_candy_combinaison(test_grid):
  move_candy(test_grid)
  
  test_grid = create_new_candy(test_grid)

  all_combi = check_all_value(test_grid)
  while len(all_combi) > 0:
    for coord in all_combi:
      test_grid[coord[0]][coord[1]] = 0
    score(all_combi)
    move_candy(test_grid)
    test_grid = create_new_candy(test_grid)
    all_combi = check_all_value(test_grid)

  # grid_display(test_grid, 5)
  grid_convert_display(test_grid)
  print()

  move = player_move(test_grid)
  swap_candies(test_grid, move[0], move[1])
  combi = detect_coordinate_combinaison2(move[0][0], move[0][1], test_grid)
  for coord in combi:
    test_grid[coord[0]][coord[1]] = 0

else:
  print("end of the game")

test_grid2 = grid_init(5, 5)
print(check_all_value(test_grid2))
