from random import randint
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

def detect_coordinate_combination_lv2(grid,row,col):
  """
  check row combination
  """
  row_candies = [[row,col]]
  col_dec = col-1
  col_inc = col+1
  int_candy = grid[row][col]
  
  while (col_inc <= (len(grid)-1) ) and (grid[row][col_inc] == int_candy):
    row_candies.append([row,col_inc])
    col_inc += 1

  while (col_dec >= 0) and (grid[row][col_dec] == int_candy):
    row_candies.append([row,col_dec])
    col_dec -= 1

  """
  check column combination
  """
  col_candies = [[row,col]]
  row_dec = row-1
  row_inc = row+1
  while (row_dec >= 0) and grid[row_dec][col] == int_candy:
    col_candies.append([row_dec,col])
    row_dec -= 1

  while (row_inc <= (len(grid)-1) ) and grid[row_inc][col] == int_candy:
    col_candies.append([row_inc,col])
    row_inc += 1

  """
  check the length of the combination and return the highest combination direction
  """
  print(row_candies)
  print(col_candies)
  
  delete_candies = []

  if len(row_candies) >= 3 and len(row_candies) >= len(col_candies):
    delete_candies = row_candies
  elif len(col_candies) >= 3 and len(col_candies) >= len(row_candies):
    delete_candies = col_candies

  return delete_candies


def change_grid_state(grid,move,final_score):
  """
  input player move
  """
  grid = swap_candies(grid,move[0],move[1])

  """
  check candy combination of the move
  """
  delete_candies = []
  
  first_combination = detect_coordinate_combination_lv2(grid,move[0][0],move[0][1])
  second_combination = detect_coordinate_combination_lv2(grid,move[1][0],move[1][1])
  
  for ele in first_combination:
    delete_candies.append(ele)
  for ele in second_combination:
    if ele in delete_candies:
      pass
    else:
      delete_candies.append(ele)
  print(delete_candies)
    
  """
  remove the candy combination by making them into 0(s)
  """
  if delete_candies == []:
    grid = swap_candies(grid,move[0],move[1])
  else:
    for element in delete_candies:
      grid[element[0]][element[1]] = 0
    
    final_score += score(delete_candies)
    print(f'Score: {final_score:.2f}')
    
    delete_candies = []
    move_candy(grid)
    create_new_candy(grid)

  return grid


def check_all_value(grid):
  big_list = []
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if [i, j] not in big_list:
        big_list += detect_coordinate_combinaison2(i, j, grid)
  return big_list


def player_input():
  xmove_1, ymove_1 = input('Enter the coordinates of 1st candy:').split()
  xmove_2, ymove_2 = input('Enter the coordinates of 2nd candy:').split()
  xmove_1,ymove_1,xmove_2,ymove_2 =  int(xmove_1),int(ymove_1),int(xmove_2),int(ymove_2)
  move = [[xmove_1, ymove_1], [xmove_2, ymove_2]]
  return move


def player_move(grid):
  move = player_input()
  if (move[0][0] >= len(grid)) or (move[0][1] >= len(grid)) or (move[1][0] >= len(grid)) or (move[1][1] >= len(grid)):
    print('Your move is out of table, please do it again')
    move = player_input()
  elif (move[0][0] < 0) or (move[0][1] < 0) or (move[1][0] < 0) or (move[1][1] < 0):
    print('Your move is so small that we can not do it, please do it again')
    move = player_input()
  elif (abs(move[0][0] - move[1][0]) >= 1) and (abs(move[0][1] - move[1][1]) >= 1) or ((abs(move[0][0] - move[1][0]) == 1) and (abs(move[0][1] - move[1][1]) == 1)):
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

def pattern_1(grid,i,j):
  if grid[i][j] == grid[i][j+1] == grid[i+1][j+2]:
    return True
  return False

def pattern_2(grid,i,j):
  if grid[i][j] == grid[i][j+1] == grid[i-1][j+2]:
    return True
  return False

def pattern_3(grid,i,j):
  if grid[i][j] == grid[i-1][j+1] == grid[i][j+2]:
    return True
  return False

def pattern_4(grid,i,j):
  if grid[i][j] == grid[i+1][j+1] == grid[i][j+2]:
    return True
  return False

def pattern_5(grid,i,j):
  if grid[i-1][j] == grid[i][j+1] == grid[i][j+2]:
    return True
  return False

def pattern_6(grid,i,j):
  if grid[i+1][j] == grid[i][j+1] == grid[i][j+2]:
    return True
  return False

def pattern_7(grid,i,j):
  if grid[i][j-1] == grid[i+1][j] == grid[i+2][j]:
    return True
  return False

def pattern_8(grid,i,j):
  if grid[i][j+1] == grid[i+1][j] == grid[i+2][j]:
    return True
  return False

def pattern_9(grid,i,j):
  if grid[i][j] == grid[i+1][j-1] == grid[i+2][j]:
    return True
  return False

def pattern_10(grid,i,j):
  if grid[i][j] == grid[i+1][j+1] == grid[i+1][j]:
      return True
  return False

def pattern_11(grid,i,j):
  if grid[i][j] == grid[i+1][j] == grid[i+2][j-1]:
      return True
  return False

def pattern_12(grid,i,j):
  if grid[i][j] == grid[i+1][j] == grid[i+2][j+1]:
      return True
  return False

def pattern_13(grid,i,j):
  if grid[i][j] == grid[i+1][j] == grid[i+3][j]:
      return True
  return False

def pattern_14(grid,i,j):
  if grid[i][j] == grid[i+2][j] == grid[i+3][j+1]:
      return True
  return False

def pattern_15(grid,i,j):
  if grid[i][j] == grid[i][j+1] == grid[i][j+3]:
      return True
  return False

def pattern_16(grid,i,j):
  if grid[i][j] == grid[i][j+2] == grid[i][j+3]:
      return True
  return False

def check_all_possible_move(grid):
  for row in range(len(grid)):
    for column in range(len(grid[row])):
      if (pattern_1(grid,row,column) == True) or (pattern_2(grid,row,column) == True) or (pattern_3(grid,row,column) == True) or (pattern_4(grid,row,column) == True) or (pattern_5(grid,row,column) == True) or (pattern_6(grid,row,column) == True) or (pattern_7(grid,row,column) == True) or (pattern_8(grid,row,column) == True) or (pattern_9(grid,row,column) == True) or (pattern_10(grid,row,column) == True) or (pattern_11(grid,row,column) == True) or (pattern_12(grid,row,column) == True) or (pattern_13(grid,row,column) == True) or (pattern_14(grid,row,column) == True) or (pattern_15(grid,row,column) == True) or (pattern_16(grid,row,column) == True):
        return True
      else:
        return False
          

########### main ###########
current_grid = grid_init(5, 5)

end = False
total_score = 0

while end == False:
  grid_convert_display(current_grid)
  
  temp_grid = current_grid
  list_move = player_move(current_grid)
  

  current_grid = change_grid_state(current_grid,list_move,total_score)
  
  if current_grid == temp_grid:
    print('Your move is useless!')
    end = False
    
  elif check_all_possible_move(current_grid) == False:
    end = True
  else:
    end = False

print('End game') 
