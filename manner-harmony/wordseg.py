#!/usr/bin/env python3

from sys import stdin

for line in stdin:
    cleaned = line.rstrip()
    phonemes = cleaned.split()
    if len(phonemes) > 0:
        print(" ".join(phonemes))