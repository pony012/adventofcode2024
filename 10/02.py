# --- Part Two ---

# The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.

# The paper describes a second way to measure a trailhead called its rating. A trailhead's rating is the number of distinct hiking trails which begin at that trailhead. For example:

# .....0.
# ..4321.
# ..5..2.
# ..6543.
# ..7..4.
# ..8765.
# ..9....

# The above map has a single trailhead; its rating is 3 because there are exactly three distinct hiking trails which begin at that position:

# .....0.   .....0.   .....0.
# ..4321.   .....1.   .....1.
# ..5....   .....2.   .....2.
# ..6....   ..6543.   .....3.
# ..7....   ..7....   .....4.
# ..8....   ..8....   ..8765.
# ..9....   ..9....   ..9....

# Here is a map containing a single trailhead with rating 13:

# ..90..9
# ...1.98
# ...2..7
# 6543456
# 765.987
# 876....
# 987....

# This map contains a single trailhead with rating 227 (because there are 121 distinct hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on the bottom edge):

# 012345
# 123456
# 234567
# 345678
# 4.6789
# 56789.

# Here's the larger example from before:

# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732

# Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic map is 81.

# You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. What is the sum of the ratings of all trailheads?

import pprint
class Node():
    def __init__(self, id, value, row, col):
        self.id = id
        self.value = value
        self.row = row
        self.col = col
        self.score = 0
        self.visited_by = []
    
    def __repr__(self):
        return f"({self.row}, {self.col})"

def should_walk(node_1, node_2):
    return node_2.value == node_1.value + 1

lava_map = []
global_score = 0
PATH_START = 0
PATH_END = 9
with open('10/input.txt') as fp:
    id = 0
    for row_index, row in enumerate(fp):
        row = row.strip()
        column_index = 0
        columns = []
        for col_index, col in enumerate(row):
            columns.append(Node(id, int(col), row_index, col_index))
            id += 1
        lava_map.append(columns)

for row_index, row in enumerate(lava_map):
    for col_index, start_node in enumerate(row):
        if start_node.value == PATH_START:
            path = [start_node]
            
            while(len(path)):
                current_node = path.pop()
                if current_node.value == PATH_END:
                    # End of trail, add 1 to its score
                    # print(f"{PATH_END} found on {current_node}, path: {path}")
                    # Remove validation from part 1
                    # if not (start_node.id in current_node.visited_by):
                    start_node.score += 1
                    global_score += 1
                        # current_node.visited_by.append(start_node.id)
                else:
                    current_value = current_node.value
                    # Right
                    if (current_node.col < len(lava_map[0]) - 1):
                        next_node = lava_map[current_node.row][current_node.col + 1]
                        if (should_walk(current_node, next_node)):
                            path.append(next_node)
                    # Down
                    if (current_node.row < len(lava_map) - 1):
                        next_node = lava_map[current_node.row + 1][current_node.col]
                        if (should_walk(current_node, next_node)):
                            path.append(next_node)
                    # Left
                    if (current_node.col > 0):
                        next_node = lava_map[current_node.row][current_node.col - 1]
                        if (should_walk(current_node, next_node)):
                            path.append(next_node)
                    # Up
                    if (current_node.row > 0):
                        next_node = lava_map[current_node.row - 1][current_node.col]
                        if (should_walk(current_node, next_node)):
                            path.append(next_node)
# for row in lava_map:
#     for node in row:
#         if node.value == PATH_START:
#             print(node)
print(global_score)
