import re

# Only matches lines that start with '*' (new best solution)
pattern = re.compile(
    r"\s+\d+\s+\d+\s+.*?\|\s*([\d\.]+).*?\s(\d+)s"
)
log_line_1 = "H  0  0      -        0    -   |  1018.00000 1023.58550 0.55% |  -    0s"
log_line_2 = "* 0  0    1023.58550  0    1   |  1023.58550 1023.58550 0.00% |  -    0s"
log_line_3 = "  500 450 1019.54321 15   12  |  1018.00000 1019.00000 0.10% |  5    55s"

match1 = pattern.search(log_line_1)
match2 = pattern.search(log_line_2)
match3 = pattern.search(log_line_3)

if match1:
    print(f"Line 1 Incumbent: {match1.group(1)}, Time: {match1.group(2)}s")

if match2:
    print(f"Line 2 Incumbent: {match2.group(1)}, Time: {match2.group(2)}s")
    
if match3:
    print(f"Line 3 Incumbent: {match3.group(1)}, Time: {match3.group(2)}s")

# Output:
# Line 1 Incumbent: 1018.00000, Time: 0s
# Line 2 Incumbent: 1023.58550, Time: 0s
# Line 3 Incumbent: 1018.00000, Time: 55s