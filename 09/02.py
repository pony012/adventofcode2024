# --- Part Two ---

# Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

# The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

# This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

# The first example from above now proceeds differently:

# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..


# The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

# Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?

FREE_CHAR = '.'

class Block():
    def __init__(self, index, length, is_data=True, is_already_moved=False):
        super()
        self.index = index
        self.length = length
        self.is_data = is_data
        self.is_already_moved = is_already_moved

    def copy(self):
        return Block(self.index, self.length, self.is_data, self.is_already_moved)

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
            idx -= 1
        return idx

    def get_left_most_space_idx(self, from_left):
        idx = from_left
        while(self.full_disk[idx].is_data and idx < (len(self.full_disk) - 1)):
            idx += 1
        return idx
    
    def compute_hash(self):
        sum = 0
        position = 0
        for block in self.full_disk:
            for _ in range(block.length):
                if block.is_data:
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
                pretty_string += FREE_CHAR * block.length
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
    from_left = 0
    right_index = len(disk.full_disk) - 1
    while(right_index > 1):
        current_right_block = disk.full_disk[right_index]
        if(current_right_block.is_data and (not current_right_block.is_already_moved)):
            left_index = disk.get_left_most_space_idx(0)
            while(left_index < right_index):
                current_left_block = disk.full_disk[left_index]
                if ((not current_left_block.is_data) and 
                    (not current_right_block.length > current_left_block.length)):
                    current_right_block.is_already_moved = True
                    if (current_left_block.length == current_right_block.length):
                        # Length is the same on both blocks, swap
                        disk.full_disk[left_index] = current_right_block
                        disk.full_disk[right_index] = current_left_block
                    else:
                        # Data length is less than space length
                        disk.full_disk[left_index].length -= current_right_block.length
                        # We need to make a copy because how Python references work
                        disk.full_disk.insert(left_index, current_right_block.copy())
                        disk.full_disk[right_index + 1].is_data = False
                        right_index += 1
                    break
                left_index += 1         
        right_index -= 1
    # print(disk.to_pretty_string())
    print(disk.compute_hash())
