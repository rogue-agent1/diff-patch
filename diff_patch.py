#!/usr/bin/env python3
"""Unified diff generator and patch applier."""
import sys, difflib

def diff(file1, file2, context=3):
    a = open(file1).readlines(); b = open(file2).readlines()
    return ''.join(difflib.unified_diff(a, b, fromfile=file1, tofile=file2, n=context))

def apply_patch(original, patch_text):
    lines = open(original).readlines()
    result = list(lines)
    offset = 0
    for line in patch_text.split('\n'):
        if line.startswith('@@'):
            import re
            m = re.search(r'\+(\d+)', line)
            if m: pos = int(m[1]) - 1
        elif line.startswith('+'): result.insert(pos + offset, line[1:] + '\n'); offset += 1
        elif line.startswith('-'): 
            if pos + offset < len(result): result.pop(pos + offset); offset -= 1
    return ''.join(result)

def stat(file1, file2):
    a = open(file1).readlines(); b = open(file2).readlines()
    d = list(difflib.unified_diff(a, b))
    added = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    removed = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    print(f"{file1} → {file2}: +{added} -{removed} lines")

if __name__ == '__main__':
    if len(sys.argv) < 3: print("Usage: diff_patch.py diff <file1> <file2>\n       diff_patch.py stat <file1> <file2>"); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'diff': print(diff(sys.argv[2], sys.argv[3]))
    elif cmd == 'stat': stat(sys.argv[2], sys.argv[3])
