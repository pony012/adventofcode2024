# --- Part Two ---

# Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

# Whoops!

# After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

# So, these three T-frequency antennas now create many antinodes:

# T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........

# In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

# The original example now has 34 antinodes, including the antinodes that appear on every antenna:

# ##....#....#
# .#.#....0...
# ..#.#0....#.
# ..##...0....
# ....0....#..
# .#...#A....#
# ...#..#.....
# #....#.#....
# ..#.....A...
# ....#....A..
# .#........#.
# ...#......##

# Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?

# import pprint
global_map = []
clusters = {}
EMPTY_CHAR = '.'
ANTINODE_CHAR = '#'

def set_global_antinode(row, column, antinodes_count):
    if global_map[row][column] != ANTINODE_CHAR:
        antinodes_count += 1
        s = list(global_map[row])
        s[column] = ANTINODE_CHAR
        global_map[row] = "".join(s)
    return antinodes_count

def extend_point(p, diff_columns, diff_rows, right, down, right_limit, down_limit, antinodes_count):
    aux_point = [-1, -1]
    aux_point[0] = p[0] + diff_columns if right else p[0] - diff_columns
    aux_point[1] = p[1] + diff_rows if down else p[1] - diff_rows
    while(aux_point[0] < right_limit and aux_point[0] >= 0 and
            aux_point[1] < down_limit and aux_point[1] >= 0):
        antinodes_count = set_global_antinode(aux_point[1], aux_point[0], antinodes_count)
        aux_point[0] = aux_point[0] + diff_columns if right else aux_point[0] - diff_columns
        aux_point[1] = aux_point[1] + diff_rows if down else aux_point[1] - diff_rows
    return antinodes_count

with open('02/input.txt') as fp:
    row_index = 0
    for row in fp:
        row = row.strip()
        column_index = 0
        for column in row:
            if column != EMPTY_CHAR:
                if clusters.get(column) is None:
                    clusters[column] = []
                clusters[column].append((column_index, row_index)) # x, y in cartesian map
            column_index += 1
        global_map.append(row)
        row_index += 1
row_max_size = len(global_map)
column_max_size = len(global_map[0])
antinodes_count = 0

# pprint.pprint(global_map)
for cluster in clusters:
    for p1_index, p1 in enumerate(clusters[cluster][:-1]):
        for p2_index, p2 in enumerate(clusters[cluster][p1_index+1:]):
            diff_cols = abs(p2[0] - p1[0])
            diff_rows = abs(p2[1] - p1[1])
            down = p2[1] >= p1[1]
            right = p2[0] >= p1[0]

            if down:
                if right:
                    antinodes_count = extend_point(p2, diff_cols, diff_rows, False, False, column_max_size, row_max_size, antinodes_count)
                    antinodes_count = extend_point(p1, diff_cols, diff_rows, True, True, column_max_size, row_max_size, antinodes_count)
                else:
                    antinodes_count = extend_point(p2, diff_cols, diff_rows, True, False, column_max_size, row_max_size, antinodes_count)
                    antinodes_count = extend_point(p1, diff_cols, diff_rows, False, True , column_max_size, row_max_size, antinodes_count)
            else:
                if right:
                    antinodes_count = extend_point(p1, diff_cols, diff_rows, False, False, column_max_size, row_max_size, antinodes_count)
                    antinodes_count = extend_point(p2, diff_cols, diff_rows, True, True, column_max_size, row_max_size, antinodes_count)
                else:
                    antinodes_count = extend_point(p1, diff_cols, diff_rows, True, False, column_max_size, row_max_size, antinodes_count)
                    antinodes_count = extend_point(p2, diff_cols, diff_rows, False, True , column_max_size, row_max_size, antinodes_count)

print(antinodes_count)