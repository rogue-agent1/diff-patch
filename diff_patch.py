#!/usr/bin/env python3
"""diff_patch - Unified diff generation and patch application."""
import sys

def lcs_table(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp

def unified_diff(old_lines, new_lines, old_name="a", new_name="b"):
    dp = lcs_table(old_lines, new_lines)
    ops = []
    i, j = len(old_lines), len(new_lines)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_lines[i-1] == new_lines[j-1]:
            ops.append((" ", old_lines[i-1]))
            i -= 1; j -= 1
        elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
            ops.append(("+", new_lines[j-1]))
            j -= 1
        else:
            ops.append(("-", old_lines[i-1]))
            i -= 1
    ops.reverse()
    lines = [f"--- {old_name}", f"+++ {new_name}"]
    for op, line in ops:
        lines.append(f"{op}{line}")
    return "\n".join(lines)

def apply_patch(old_lines, patch_text):
    result = []
    for line in patch_text.split("\n"):
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("+"):
            result.append(line[1:])
        elif line.startswith("-"):
            continue
        elif line.startswith(" "):
            result.append(line[1:])
    return result

def count_changes(patch_text):
    added = sum(1 for l in patch_text.split("\n") if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in patch_text.split("\n") if l.startswith("-") and not l.startswith("---"))
    return added, removed

def test():
    old = ["line1", "line2", "line3"]
    new = ["line1", "modified", "line3", "line4"]
    diff = unified_diff(old, new)
    assert "+modified" in diff
    assert "-line2" in diff
    assert "+line4" in diff
    # apply
    result = apply_patch(old, diff)
    assert result == new
    # count
    added, removed = count_changes(diff)
    assert added == 2 and removed == 1
    print("OK: diff_patch")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: diff_patch.py test")
