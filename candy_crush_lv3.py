from random import randint
import matplotlib.pyplot as plt


def grid_init(n, m, nb=int):
    grid = []
    for i in range(n):
        grid.append([])
        for j in range(m):
            grid[i].append(randint(1, nb))
    return grid


def grid_display(grid, nb_type_candies):
    """
    Displays the game grid "grid" containing at least
    maximum "nb_type_candies" different colors of candies.
    """
    plt.imshow(grid, vmin=0, vmax=nb_type_candies, cmap='jet')
    plt.pause(0.1)
    plt.draw()
    plt.pause(0.1)

def grid_console_display(grid):
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

def create_new_candy(grid, nb=int):
    '''
    from the grid, find the zeroes and replace them with n color numbers
    '''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                grid[i][j] = randint(1, nb)
    return grid


def detect_coordinate_combination_lv3(grid, i, j): #give a list of the candies that are in combinaison with i,j
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


def floodcandy(x, y, grid): #used to find the combinaison of level 3

  combi_list = []
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
      if (0 <= elem[0]) and (elem[0] < len(grid)) and (0 <= elem[1]) and (elem[1] < len(grid[x])):
        if grid[elem[0]][elem[1]] == color and (elem not in queued) and (elem not in combi_list):
          queued.append(elem)

  return combi_list


def candy_delete_combo(grid):
    ###combo of candy combination on the grid
    combo = []
    for row in range(len(grid)):
        for col in range(len(grid)):
            if len(detect_coordinate_combination_lv3(grid, row, col)) >= 3:
                combo.append([row, col])
    return combo


def change_grid_state(grid, move, nb=int):
    ## Initialize the return grid ####
    return_grid = []
    for row in grid:
        return_grid.append(row.copy())

    swap_candies(return_grid, move[0], move[1])

    ### check candy combination of the move ###
    delete_candies = []

    first_combination = detect_coordinate_combination_lv3(return_grid, move[0][0], move[0][1])
    second_combination = detect_coordinate_combination_lv3(return_grid, move[1][0], move[1][1])

    for ele in first_combination:
        delete_candies.append(ele)
    for ele in second_combination:
        if ele in delete_candies:
            pass
        else:
            delete_candies.append(ele)

    ### remove the candy combination by making them into 0(s)

    if delete_candies == []:
        swap_candies(return_grid, move[0], move[1])
        return_point = 0
    else:
        for element in delete_candies:
            return_grid[element[0]][element[1]] = 0

        ### add score ###
        return_point = 0
        point = score(delete_candies)
        print(f'Score: {point:.2f}')
        return_point += point

        delete_candies = []
        move_candy(return_grid)
        create_new_candy(return_grid, nb)

        ###candy combo after create new candy
        combo = candy_delete_combo(return_grid)
        while len(combo) >= 3:
            for ele in combo:
                delete_candies.append(ele)

            for element in delete_candies:
                return_grid[element[0]][element[1]] = 0

            point = score(delete_candies)
            print(f'Combo score: {point:.2f}')
            return_point += point

            delete_candies = []
            move_candy(return_grid)
            create_new_candy(return_grid, nb)

            combo = candy_delete_combo(return_grid)

    return return_grid, return_point


def player_input():
    xy1 = input('Enter the coordinates of 1st candy (x y):')
    xy2 = input('Enter the coordinates of 2nd candy (x y):')
    while len(xy1) - 1 != len(xy1.replace(" ", "")) or len(xy2) - 1 != len(xy2.replace(" ", "")) or (xy1[0] == " " or xy1[-1] == " " or xy2[0] == " " or xy2[-1] == " "):
        print("wrong input (too much spaces/ no spaces)")
        xy1 = input('Enter the coordinates of 1st candy (x y):')
        xy2 = input('Enter the coordinates of 2nd candy (x y):')
    xmove_1, ymove_1 = xy1.split()
    xmove_2, ymove_2 = xy2.split()

    while not (xmove_1.isdigit() or xmove_2.isdigit() or ymove_1.isdigit() or ymove_2.isdigit()):
        print("wrong input (input are not integers)")
        xy1 = input('Enter the coordinates of 1st candy (x y):')
        xy2 = input('Enter the coordinates of 2nd candy (x y):')
        while len(xy1) - 1 != len(xy1.replace(" ", "")) or len(xy2) - 1 != len(xy2.replace(" ", "")) and (xy1[0] == " " or xy1[-1] == " " or xy2[0] == " " or xy2[-1] == " "):
            print("wrong input (too much spaces/ no spaces)")
            xy1 = input('Enter the coordinates of 1st candy (x y):')
            xy2 = input('Enter the coordinates of 2nd candy (x y):')
        xmove_1, ymove_1 = xy1.split()
        xmove_2, ymove_2 = xy2.split()

    xmove_1, ymove_1, xmove_2, ymove_2 = int(xmove_1), int(ymove_1), int(xmove_2), int(ymove_2)
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
    elif (abs(move[0][0] - move[1][0]) >= 1) and (abs(move[0][1] - move[1][1]) >= 1) or (
            (abs(move[0][0] - move[1][0]) == 1) and (abs(move[0][1] - move[1][1]) == 1)):
        print('You made an invalid move, please do it again')
        move = player_input()
    return move


def swap_candies(grid, coord1, coord2) -> None:
    save = grid[coord1[0]][coord1[1]]
    grid[coord1[0]][coord1[1]] = grid[coord2[0]][coord2[1]]
    grid[coord2[0]][coord2[1]] = save


def move_candy(grid):
    for j in range(len(grid) - 1, -1, -1):
        row_check = len(grid) - 1
        count = 0
        while (row_check >= 0):
            if grid[row_check][j] == 0:
                count += 1
                row_check -= 1
            elif grid[row_check][j] != 0:
                grid[row_check][j], grid[row_check + count][j] = grid[row_check + count][j], grid[row_check][j]
                row_check -= 1


def score(combi):
    score = 2.7 ** (len(combi) / 3)
    return score


def possible_candy_combination(grid, row, col) -> bool:
    init_coord = [row, col]
    check = False

    ##swap to the above candy
    if row - 1 >= 0:
        check_coord = [row - 1, col]
        swap_candies(grid, init_coord, check_coord)
        check_list = detect_coordinate_combination_lv3(grid, check_coord[0], check_coord[1])
        if len(check_list) >= 3:
            check = True
        swap_candies(grid, init_coord, check_coord)

    ##swap to the left candy
    if col - 1 >= 0:
        check_coord = [row, col - 1]
        swap_candies(grid, init_coord, check_coord)
        check_list = detect_coordinate_combination_lv3(grid, check_coord[0], check_coord[1])
        if len(check_list) >= 3:
            check = True
        swap_candies(grid, init_coord, check_coord)

    ##swap to the below candy
    if row + 1 <= len(grid) - 1:
        check_coord = [row + 1, col]
        swap_candies(grid, init_coord, check_coord)
        check_list = detect_coordinate_combination_lv3(grid, check_coord[0], check_coord[1])
        if len(check_list) >= 3:
            check = True
        swap_candies(grid, init_coord, check_coord)

    ##swap to the right candy
    if col + 1 <= len(grid) - 1:
        check_coord = [row, col + 1]
        swap_candies(grid, init_coord, check_coord)
        check_list = detect_coordinate_combination_lv3(grid, check_coord[0], check_coord[1])
        if len(check_list) >= 3:
            check = True
        swap_candies(grid, init_coord, check_coord)

    return check


def check_all_possible_move(grid) -> bool:
    possible = False
    for row in range(len(grid)):
        for col in range(len(grid)):
            if possible_candy_combination(grid, row, col) == True:
                possible = True

    return possible


########### main ###########
type_candies = 4
current_grid = grid_init(10, 10, type_candies)

end = False
total_score = 0

while end == False:
    grid_display(current_grid, type_candies)

    temp_grid = current_grid  ### address assignment ###
    list_move = player_move(current_grid)

    current_grid, point = change_grid_state(current_grid, list_move, type_candies)
    total_score += point
    print(f'Total score: {total_score:.2f}')

    if temp_grid == current_grid:
        print('Your move is useless!')
        end = False

    if check_all_possible_move(current_grid) == True:
        end = False
    else:
        end = True

print('End game')
