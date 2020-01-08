import numpy as np


board = [
    [3,7,0,0,0,9,0,0,6],
    [8,0,0,1,0,3,0,7,0],
    [0,0,0,0,0,0,0,0,8],
    [0,2,0,0,8,0,0,0,5],
    [1,8,7,0,0,0,6,4,2],
    [5,0,0,0,2,0,0,1,0],
    [7,0,0,0,0,0,0,0,0],
    [0,5,0,6,0,2,0,0,7],
    [2,0,0,3,0,0,0,6,1]
]


def valid(b, pos):
    t = []
    # check row
    for i in range(len(b[0])):
        if i!=pos[1]:
            t.append(b[pos[0]][i])            

    # check column
    for i in range(len(b)):
        if i!=pos[0]:
            t.append(b[i][pos[1]])

    # check box
    box_x = pos[0]//3
    box_y = pos[1]//3

    for i in range(3*box_x, 3*box_x + 3):
        for j in range(3*box_y, 3*box_y + 3):
            if i!=pos[0] and j!=pos[1]:
                t.append(b[i][j])

    f = np.arange(1, 10)
    f = np.setdiff1d(f, t)
    return f


def solve(b):
    if empty_cell(b) is None:
        return True

    cell = empty_cell(b)
    r, c = cell
    t = valid(b, cell)
    np.random.shuffle(t)

    for i in t:
        b[r][c] = i
        if solve(b):
            return True

        b[r][c] = 0

    return False


def unique_solution(b, count):
    # if empty_cell(b) is None:
    #     print(b)
    #     return (count==0), count+1

    cell = empty_cell(b)
    r, c = cell
    t = valid(b, cell)
    np.random.shuffle(t)

    counter = 0
    for i in t:
        b[r][c] = i
        if empty_cell(b) is None:
            print(b, count, counter)
            counter += 1
            if counter+count>1:
                return False, count+counter
        else:
            ans = unique_solution(b, count+counter)
            if ans[0]:
                print(b, count, counter)
                counter += 1
                if counter+count>1:
                    return False, count+counter
            elif ans[1]>1:
                return False, count+ans[1]+counter

        b[r][c] = 0

    return (count+counter==1), count+counter



def empty_cell(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return (i, j)

    return None


def print_board(b):

    for i in range(len(b)):
        if i%3==0 and i!=0:
            print("- - - - - - - - - - -")

        for j in range(len(b[0])):
            if j%3==0 and j!=0:
                print("| ", end="")

            if j==8:
                print(b[i][j])
            else:
                print(str(b[i][j])+" ", end="")



if __name__ == '__main__':
    # print_board(board)
    # print("#############################################")
    # solve(board)
    # print_board(board)
    print(unique_solution(np.array(board), 0))