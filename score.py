import os
import sys
from wordfreq import top_n_list
from wordfreq import zipf_frequency

COMMON_TOP = 30000
FULL_TOP = 100000
MIN_SEG = 3
SHOW = 50

def load(n):
  return {w for w in top_n_list("en", n) if w.isascii() and w.isalpha() and len(w) >= MIN_SEG}

common = load(COMMON_TOP)
full = load(FULL_TOP) | common
with open(os.path.expanduser("~/onions/filters.txt")) as f:
  full.update(line.strip() for line in f if line.strip())
maxlen = max(map(len, full))

def segment(s):
  best = [None] * (len(s) + 1)
  best[0] = (0, [])
  for i in range(len(s)):
    if best[i] is None:
      continue
    vocab = full if i == 0 else common
    for j in range(i + MIN_SEG, min(len(s), i + maxlen) + 1):
      w = s[i:j]
      if w in vocab:
        score = best[i][0] + len(w) ** 2
        if best[j] is None or score > best[j][0]:
          best[j] = (score, best[i][1] + [w])
  end = max(range(len(s) + 1), key=lambda k: best[k][0] if best[k] else -1)
  return end, best[end][0], best[end][1]

results = []
for path in sys.argv[1:]:
  with open(path) as f:
    for line in f:
      if line.startswith("hostname:"):
        host = line.split(":", 1)[1].strip()
        cov, score, words = segment(host[:24])
        freq = sum(zipf_frequency(w, "en") for w in words)
        results.append((score, freq, cov, host, words))

results.sort(reverse=True)
for score, freq, cov, host, words in results[:SHOW]:
  print(f"{score:4d} {cov:2d}  {'·'.join(words)}|{host[cov:]}")
