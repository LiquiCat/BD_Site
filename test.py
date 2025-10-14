import re

def verify_lines_start_with(beg, lines):
    reg = re.compile(beg)
    return all(map(lambda x: reg.search(x), lines))

a = """1. aaaaaa
2. aaaaaaaaaa
3. aaaaaaaaa
4. aaaaaaa"""

b = """> aaaaaa
> aaaaaaaaaa
aaaaaaaaa
> aaaaaaa"""


print(verify_lines_start_with(r"^\d+. ", a.split("\n")))
print(verify_lines_start_with(r"^> ", b.split("\n")))