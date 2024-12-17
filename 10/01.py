# --- Day 10: Hoof It ---

# You all arrive at a Lava Production Facility on a floating island in the sky. As the others begin to search the massive industrial complex, you feel a small nose boop your leg and look down to discover a reindeer wearing a hard hat.

# The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly.

# Perhaps you can help fill in the missing hiking trails?

# The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest). For example:

# 0123
# 1234
# 8765
# 9876

# Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).

# You look up from the map and notice that the reindeer has helpfully begun to construct a small pile of pencils, markers, rulers, compasses, stickers, and other equipment you might need to update the map with hiking trails.

# A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail. In the above example, the single trailhead in the top left corner has a score of 1 because it can reach a single 9 (the one in the bottom left).

# This trailhead has a score of 2:

# ...0...
# ...1...
# ...2...
# 6543456
# 7.....7
# 8.....8
# 9.....9

# (The positions marked . are impassable tiles to simplify these examples; they do not appear on your actual topographic map.)

# This trailhead has a score of 4 because every 9 is reachable via a hiking trail except the one immediately to the left of the trailhead:

# ..90..9
# ...1.98
# ...2..7
# 6543456
# 765.987
# 876....
# 987....

# This topographic map contains two trailheads; the trailhead at the top has a score of 1, while the trailhead at the bottom has a score of 2:

# 10..9..
# 2...8..
# 3...7..
# 4567654
# ...8..3
# ...9..2
# .....01

# Here's a larger example:

# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732

# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732

# This larger example has 9 trailheads. Considering the trailheads in reading order, they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of all trailheads is 36.

# The reindeer gleefully carries over a protractor and adds it to the pile. What is the sum of the scores of all trailheads on your topographic map?

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
                    if not (start_node.id in current_node.visited_by):
                        start_node.score += 1
                        global_score += 1
                        current_node.visited_by.append(start_node.id)
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
