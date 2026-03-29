from diff_patch import diff, _lcs
a = ["line1", "line2", "line3"]
b = ["line1", "line2b", "line3"]
d = diff(a, b)
assert "-line2" in d
assert "+line2b" in d
print("Diff tests passed")