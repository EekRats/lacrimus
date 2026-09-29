import re
import sys
from wordfreq import top_n_list

# define minimum length basedd on an argument, default to 8
MIN_LEN = int(sys.argv[1]) if len(sys.argv) > 1 else 8

# how many of the top scored onion addrs? Default to 100k
TOP_N = int(sys.argv[2]) if len(sys.argv) > 2 else 100000

LANGS = ["en"]
RATE = 111.6e6

valid = re.compile(r"^[a-z]+$")
words = set()
for lang in LANGS:
  for w in top_n_list(lang, TOP_N):
    if valid.match(w) and len(w) >= MIN_LEN:
      words.add(w)

kept = sorted(w for w in words if not any(w[:i] in words for i in range(MIN_LEN, len(w))))

with open("filters.txt", "w") as f:
  f.write("\n".join(kept) + "\n")

per_sec = RATE * sum(32.0 ** -len(w) for w in kept)

print(f"{len(kept)} filters")
print(f"~{per_sec:.2f} hits/sec/node, ~{per_sec * 86400:,.0f} per node-day")
