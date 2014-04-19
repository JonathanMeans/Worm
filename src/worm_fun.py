import math

def distance(x1, y1, tup):
    x2 = tup[0]
    y2 = tup[1]
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def get_adjacent(x,y):
    left   =(x-10, y)
    right  =(x+10, y)
    up     =(x, y-10)
    down   =(x, y+10)
    return [left, right, up, down]

def in_bounds(x,y):
    if 0 <= x < 300 and 0 <= y < 300:
        return True
    return False

def direction(x, y, obj):
    if x + 10 == obj.x:
        return 'left'
    if x - 10 == obj.x:
        return 'right'
    if y + 10 == obj.y:
        return 'up'
    return 'down'

def dict_min(open_set, f_score):
    cur_min = 1000000
    next = ''
    for node in open_set:
        if f_score[node] < cur_min:
            cur_min = f_score[node]
            next = node
    return next

def star_search(worm_list, food):
    head = worm_list[0]
    start = (head.x, head.y)
    dest = food.x, food.y
    searched = []
    open_set = [start]
    f_score = {}
    g_score = {}
    traveled = {}

    g_score[start] = 0
    f_score[start] = g_score[start] + distance(start[0], start[1], dest)

    while dest not in searched:
        current = dict_min(open_set, f_score)
        searched.append(current)
        open_set.remove(current)

        tent_f = {}
        tent_g = {}
        for node in get_adjacent(current[0], current[1]):
            tent_g[node] = g_score[current] + distance(current[0], current[1], start)
            tent_f[node] = tent_g[node] + distance(current[0], current[1], dest)
            for segment in worm_list:
                if segment.x == node[0] and segment.y == node[1]:
                    tent_f[node] += 100000
            if node in searched:
                pass
            elif node not in open_set or tent_f[node] < f_score[node]:
                g_score[node] = tent_g[node]
                f_score[node] = tent_f[node]
                traveled[node] = current
                if node not in open_set:
                    open_set.append(node)
    return reconstruct_path(traveled, dest, start)

def reconstruct_path(traveled, dest, start):
    #This is recursion. It works by magic.
    if dest == start:
        return dest
    p = traveled[dest]
    if p == start: return dest
    return reconstruct_path(traveled, traveled[dest], start)



