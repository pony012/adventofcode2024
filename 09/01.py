# --- Day 9: Disk Fragmenter ---

# Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

# While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

# He shows you the disk map (your puzzle input) he's already generated. For example:

# 2333133121414131402

# The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

# So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

# Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

# 0..111....22222

# The first example above, 2333133121414131402, represents these individual blocks:

# 00...111...2...333.44.5555.6666.777.888899

# The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

# 0..111....22222
# 02.111....2222.
# 022111....222..
# 0221112...22...
# 02211122..2....
# 022111222......

# The first example requires a few more steps:

# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............

# 00...111...2...333.44.5555.6666.777.888899
# 00998111

# 00...111...2...333.44.5555.6666.777.888899
# 14
# 2
# 
# 0099811188827773336446555566
# 0099811188827773336446555566
# 00998111888277733364465555.6
# 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32
# 1928

# The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

# Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

# Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)


# Part I
FREE_CHAR = '.'

class Block():
    def __init__(self, index, length, is_data=True):
        super()
        self.index = index
        self.length = length
        self.is_data = is_data

    def __str__(self):
        return f"(Index: {self.index}, Length: {self.length})"

    def __repr__(self):
        return str(self)

class Disk:
    def __init__(self):
        super()
        self.data_blocks = []
        self.free_space_blocks = []
        self.full_disk = []
        self.current_insert_index = 0
        self.spaces = 0
    
    def __str__(self):
        return f"Data: {self.data_blocks},\nFree: {self.free_space_blocks}"


    def insert_data_block(self, length):
        data_block = Block(self.current_insert_index, length, True)
        self.data_blocks.append(data_block)
        self.current_insert_index += 1

    def insert_free_memory(self, length):
        free_space = Block(self.current_insert_index, length, False)
        self.free_space_blocks.append(free_space)
        self.spaces += length

    def organize(self):
        _data = self.data_blocks
        _spaces = self.free_space_blocks
        while(len(_data) > 0 or len(_spaces) > 0):
            if len(_data) > 0:
                self.full_disk.append(_data.pop(0))
            if len(_spaces) > 0:
                self.full_disk.append(_spaces.pop(0))
        return self.full_disk
    
    def get_right_most_data_idx(self, from_right):
        idx = from_right if from_right < len(self.full_disk) else len(self.full_disk) - 1
        while(not self.full_disk[idx].is_data and idx > 0):
            # print(f"right: {idx}")
            idx -= 1
        return idx

    def get_left_most_space_idx(self, from_left):
        idx = from_left
        while(self.full_disk[idx].is_data and idx < (len(self.full_disk) - 1)):
            # print(f"left: {idx}")
            idx += 1
        return idx
    
    def compute_hash(self):
        sum = 0
        position = 0
        for block in self.full_disk:
            for i in range(block.length):
                # print(f"{position} * {block.index} = {position*block.index}")
                sum += position * block.index
                position += 1
        return sum
    
    def remove_right_most_spaces(self):
        spaces = 0
        while(not self.full_disk[-1].is_data):
            block = self.full_disk.pop()
            spaces += block.length
        return spaces
    
    def to_pretty_string(self):
        data_index = 0
        data_length = len(self.full_disk)
        pretty_string = ''
        while(data_index < data_length):
            block = self.full_disk[data_index]
            if block.is_data:
                pretty_string += str(block.index) * block.length
            if (not block.is_data):
                pretty_string += '.' * block.length
            data_index += 1
        return pretty_string

with open('09/input.txt') as fp:
    numbers = fp
    disk = Disk()
    is_data = True
    numbers = fp.readline()
    for number in numbers:
        number = int(number)
        if is_data:
            disk.insert_data_block(number)
        else:
            disk.insert_free_memory(number)
        is_data = not is_data
    disk.organize()
    # print(numbers)
    # print(str(disk))
    # print(disk.to_pretty_string())
    
    # print(disk.to_pretty_string())
    from_left = 0
    from_right = len(disk.full_disk) - 1
    while(disk.spaces > 0):
        # right_data_idx = disk.get_right_most_data_idx(from_right + 1)
        # left_space_idx = disk.get_left_most_space_idx(from_left)
        # Unused "optimization"
        right_data_idx = disk.get_right_most_data_idx(len(disk.full_disk) - 1)
        left_space_idx = disk.get_left_most_space_idx(0)
        from_left = left_space_idx
        from_right = right_data_idx

        right_data_length = disk.full_disk[right_data_idx].length
        left_space_length = disk.full_disk[left_space_idx].length
        if right_data_length == left_space_length:
            # Data can be stored completley and exactly
            disk_data = disk.full_disk.pop(right_data_idx)
            disk.full_disk.pop(left_space_idx)
            disk.full_disk.insert(left_space_idx, disk_data)
            from_left -= 1
            disk.spaces -= disk_data.length
        elif right_data_length < left_space_length:
            # Data can be stored completly but space left
            disk_data = disk.full_disk.pop(right_data_idx)
            space_data = disk.full_disk.pop(left_space_idx)
            space_data.length -= disk_data.length
            disk.full_disk.insert(left_space_idx, space_data)
            disk.full_disk.insert(left_space_idx, disk_data)
            from_left -= 1
            disk.spaces -= disk_data.length
        else:
            # Data cannot be stored completly
            available_space = disk.full_disk[left_space_idx].length
            data_block = disk.full_disk[right_data_idx]
            disk.full_disk[right_data_idx].length -= available_space

            disk.full_disk[left_space_idx].index = data_block.index
            disk.full_disk[left_space_idx].length = available_space
            disk.full_disk[left_space_idx].is_data = True
            disk.spaces -= available_space
        remove_right_most_spaces = disk.remove_right_most_spaces()
        disk.spaces -= remove_right_most_spaces
        # print(disk.to_pretty_string())
    # print(disk.to_pretty_string())
    print(disk.compute_hash())