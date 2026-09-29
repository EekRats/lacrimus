import sys
from wordfreq import top_n_list

SEG_TOP = 30000
MIN_SEG = 3
SHOW = 50

vocab = {w for w in top_n_list("en", SEG_TOP) if w.isascii() and w.isalpha() and len(w) >= MIN_SEG}
maxlen = max(map(len, vocab))

def segment(s):
  best = [None] * (len(s) + 1)
  best[0] = (0, [])
  for i in range(len(s)):
    if best[i] is None:
      continue
    for j in range(i + MIN_SEG, min(len(s), i + maxlen) + 1):
      w = s[i:j]
      if w in vocab:
        score = best[i][0] + len(w) ** 2
        if best[j] is None or score > best[j][0]:
          best[j] = (score, best[i][1] + [w])
  for i in range(len(s), 0, -1):
    if best[i] is not None:
      return i, best[i][0], best[i][1]
  return 0, 0, []

results = []
for path in sys.argv[1:]:
  with open(path) as f:
    for line in f:
      if line.startswith("hostname:"):
        host = line.split(":", 1)[1].strip()
        cov, score, words = segment(host[:24])
        results.append((cov, score, host, words))

results.sort(reverse=True)
for cov, score, host, words in results[:SHOW]:
  print(f"{cov:2d} {score:4d}  {'·'.join(words)}|{host[cov:]}")
