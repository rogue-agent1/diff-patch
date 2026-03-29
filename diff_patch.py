#!/usr/bin/env python3
"""Myers diff algorithm with unified diff output and patch application."""
import sys

def myers_diff(a, b):
    n, m = len(a), len(b); max_d = n + m
    v = {1: 0}; trace = []
    for d in range(max_d + 1):
        trace.append(dict(v))
        for k in range(-d, d+1, 2):
            if k == -d or (k != d and v.get(k-1, 0) < v.get(k+1, 0)):
                x = v.get(k+1, 0)
            else: x = v.get(k-1, 0) + 1
            y = x - k
            while x < n and y < m and a[x] == b[y]: x += 1; y += 1
            v[k] = x
            if x >= n and y >= m:
                return _backtrack(trace, a, b, n, m)
    return []

def _backtrack(trace, a, b, n, m):
    edits = []; x, y = n, m
    for d in range(len(trace)-1, 0, -1):
        v = trace[d-1]; k = x - y
        if k == -d or (k != d and v.get(k-1, 0) < v.get(k+1, 0)):
            prev_k = k + 1
        else: prev_k = k - 1
        prev_x = v.get(prev_k, 0); prev_y = prev_x - prev_k
        while x > prev_x and y > prev_y:
            edits.append((' ', a[x-1])); x -= 1; y -= 1
        if x > prev_x: edits.append(('-', a[x-1])); x -= 1
        elif y > prev_y: edits.append(('+', b[y-1])); y -= 1
    edits.reverse(); return edits

def unified_diff(a_lines, b_lines, a_name="a", b_name="b"):
    edits = myers_diff(a_lines, b_lines)
    output = [f"--- {a_name}", f"+++ {b_name}"]
    for op, line in edits:
        if op == ' ': output.append(f" {line}")
        elif op == '-': output.append(f"-{line}")
        elif op == '+': output.append(f"+{line}")
    return "\n".join(output)

def apply_patch(original, edits):
    result = []; orig_idx = 0
    for op, line in edits:
        if op == ' ': result.append(line); orig_idx += 1
        elif op == '-': orig_idx += 1
        elif op == '+': result.append(line)
    return result

def main():
    a = ["the","quick","brown","fox","jumps","over","the","lazy","dog"]
    b = ["the","quick","red","fox","jumps","over","the","happy","dog","!"]
    edits = myers_diff(a, b)
    print("Edits:")
    for op, line in edits: print(f"  {op} {line}")
    print(f"\nUnified diff:")
    print(unified_diff(a, b))
    patched = apply_patch(a, edits)
    print(f"\nPatched matches b: {patched == b}")

if __name__ == "__main__": main()
