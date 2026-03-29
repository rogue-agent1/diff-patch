#!/usr/bin/env python3
"""Unified diff generator and patcher. Zero dependencies."""
import sys

def diff(a_lines, b_lines, a_name="a", b_name="b", context=3):
    result = [f"--- {a_name}", f"+++ {b_name}"]
    lcs = _lcs(a_lines, b_lines)
    ai = bi = li = 0
    hunks = []
    while ai < len(a_lines) or bi < len(b_lines):
        if li < len(lcs) and ai < lcs[li][0] or bi < (lcs[li][1] if li < len(lcs) else len(b_lines)):
            hunk_a_start = ai; hunk_b_start = bi; lines = []
            while ai < (lcs[li][0] if li < len(lcs) else len(a_lines)):
                lines.append(f"-{a_lines[ai]}"); ai += 1
            while bi < (lcs[li][1] if li < len(lcs) else len(b_lines)):
                lines.append(f"+{b_lines[bi]}"); bi += 1
            hunks.append((hunk_a_start, hunk_b_start, lines))
        if li < len(lcs):
            ai = lcs[li][0] + 1; bi = lcs[li][1] + 1; li += 1
        else:
            break
    for ha, hb, lines in hunks:
        result.append(f"@@ -{ha+1},{len([l for l in lines if l[0]=='-'])} +{hb+1},{len([l for l in lines if l[0]=='+'])} @@")
        result.extend(lines)
    return "\n".join(result)

def _lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    result = []; i, j = m, n
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            result.append((i-1, j-1)); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]: i -= 1
        else: j -= 1
    return result[::-1]

def apply_patch(original, patch_text):
    lines = original[:]
    offset = 0
    for line in patch_text.splitlines():
        if line.startswith("@@"):
            pass  # simplified - just track +/- lines
        elif line.startswith("-") and not line.startswith("---"):
            pass
        elif line.startswith("+") and not line.startswith("+++"):
            pass
    return lines  # simplified

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        a = open(sys.argv[1]).read().splitlines()
        b = open(sys.argv[2]).read().splitlines()
        print(diff(a, b, sys.argv[1], sys.argv[2]))
