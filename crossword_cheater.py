#!/usr/bin/env python3
"""
crossword_cheater.py
Usage:
  python crossword_cheater.py th***ly
  python crossword_cheater.py th***ly --wordlist words.txt
  python crossword_cheater.py 't*e' --min 2 --max 8
"""

import argparse
import re
import sys
from pathlib import Path

def load_wordlist(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Wordlist not found: {path}")
    words = []
    with path.open(encoding='utf-8', errors='ignore') as f:
        for line in f:
            w = line.strip()
            if w and w.isalpha():           # only alphabetic words
                words.append(w.lower())
    return words

def pattern_to_regex(pat: str):
    # user uses '*' for unknown letters (one per letter)
    # allow '?' as single wildcard too
    # hey, this is an edit
    pat = pat.strip().lower()
    # validate: must contain letters and '*' or '?'
    if not re.fullmatch(r"[a-z\*\?]+", pat):
        raise ValueError("Pattern may only contain letters a-z and '*' or '?'.")
    # Convert '*' or '?' into exactly one wildcard (.)
    regex = "^" + "".join(("."
                           if ch in "*?" else re.escape(ch)) for ch in pat) + "$"
    return re.compile(regex)

def find_matches(pattern: str, words: list, min_len=None, max_len=None):
    rx = pattern_to_regex(pattern)
    results = []
    for w in words:
        if min_len and len(w) < min_len: continue
        if max_len and len(w) > max_len: continue
        if rx.match(w):
            results.append(w)
    return results

def main():
    ap = argparse.ArgumentParser(description="Crossword Cheater")
    ap.add_argument("pattern", help="Pattern using '*' or '?' for unknown letters, e.g. th***ly")
    ap.add_argument("--wordlist", "-w", default="/usr/share/dict/words",
                    help="Path to wordlist (one word per line). Default: /usr/share/dict/words")
    ap.add_argument("--min", type=int, default=None, dest="min_len", help="Minimum word length")
    ap.add_argument("--max", type=int, default=None, dest="max_len", help="Maximum word length")
    ap.add_argument("--limit", "-n", type=int, default=200, help="Max results to show")
    args = ap.parse_args()

    wl_path = Path(args.wordlist)
    try:
        words = load_wordlist(wl_path)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        print("Tip: create a 'words.txt' with one word per line or install wordlists (e.g. apt-get install wordlists).", file=sys.stderr)
        sys.exit(2)

    matches = find_matches(args.pattern, words, args.min_len, args.max_len)
    if not matches:
        print("No matches found.")
        return
    matches = sorted(set(matches))
    if args.limit and len(matches) > args.limit:
        print(f"{len(matches)} matches (showing first {args.limit}):")
        for m in matches[:args.limit]:
            print(m)
    else:
        print(f"{len(matches)} matches:")
        for m in matches:
            print(m)

if __name__ == "__main__":
    main()
