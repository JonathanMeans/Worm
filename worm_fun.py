import math

def distance(x1, y1, obj):
    x2 = obj.x
    y2 = obj.y
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def get_adjacent(x,y):
    left   =(x-10, y)
    right  =(x+10, y)
    up     =(x, y-10)
    down   =(x, y+10)
    return [left, right, up, down]

def direction(x, y, obj):
    if x + 10 == obj.x:
        return 'left'
    if x - 10 == obj.x:
        return 'right'
    if y + 10 == obj.y:
        return 'up'
    return 'down'

def star_search(worm_list, food):
    head = worm_list[0]
    dest = food.x, food.y
    path = [head.x, head.y]
    while dest not in path:
        cost = {}
        current = path[-1]
        adj = get_adjacent(current.x, current.y)
        for square in adj:
            cost[square] = distance(current[0], current[1], food)
            for segment in worm_list:
                if segment.x == current[0] and segment.y == current[1]:
                    cost[square] = 10000
        mini = 100001
        next = ''
        for square in cost.keys():
            if cost[square] < mini:
                mini = cost[square]
                next = square
        path.append(square)

    return path[1][0], path[1][1]


