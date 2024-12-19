# --- Part Two ---

# The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

# The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

# Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

# More of the above example's reports are now safe:

#     7 6 4 2 1: Safe without removing any level.
#     1 2 7 8 9: Unsafe regardless of which level is removed.
#     9 7 6 2 1: Unsafe regardless of which level is removed.
#     1 3 2 4 5: Safe by removing the second level, 3.
#     8 6 4 4 1: Safe by removing the third level, 4.
#     1 3 6 7 9: Safe without removing any level.

# Thanks to the Problem Dampener, 4 reports are actually safe!

# Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?

def is_safe_report(levels):
    is_increasing = levels[1] > levels[0]
    current_index = 0
    while(current_index < len(levels) - 1):
        current_level = levels[current_index]
        next_level = levels[current_index + 1]
        if not is_valid_pair(is_increasing, current_level, next_level):
            return False
        current_index += 1
    return True
        
def is_valid_pair(asc, current_level, next_level):
    if not valid_diff(current_level, next_level):
        return False
    if asc and next_level > current_level:
        return True
    if (not asc) and next_level < current_level:
        return True
    return False

def valid_diff(current_level, next_level):
    diff = abs(next_level - current_level)
    return diff >= 1 and diff <= 3

def is_asc(current_level, next_level):
    return next_level > current_level

with open('02/input.txt') as fp:
    safe_reports = 0
    for report in fp:
        levels = [int(level) for level in report.strip().split(" ")]
        if is_safe_report(levels):
            safe_reports += 1
        else:
            current_index = 0
            while(current_index < len(levels)):
                current_value = levels.pop(current_index)
                if is_safe_report(levels):
                    safe_reports += 1
                    break
                levels.insert(current_index, current_value)
                current_index += 1
print(safe_reports)
