"""Turn TTS-spelled numbers back into digits for subtitles."""
import re
U = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split())}
T = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "_"}
SCALE = {"hundred": 100, "thousand": 1000, "million": 10**6, "billion": 10**9}
NUMW = set(U) | set(T) | set(SCALE)
KEEP_WORDS = {"one", "two", "three", "four", "five"}  # small standalone counts stay words unless a unit follows

def small(tok):  # "twenty-five" / "seventy" / "five"
    if "-" in tok:
        a, b = tok.split("-", 1)
        if a in T and b in U: return T[a] + U[b]
        return None
    return U.get(tok, T.get(tok))

def parse(words):
    total = cur = 0
    for w in words:
        if w == "and": continue
        if w in SCALE:
            if w == "hundred": cur = (cur or 1) * 100
            else: total += (cur or 1) * SCALE[w]; cur = 0
        else: cur += small(w)
    return total + cur

def isnum(w): return w in SCALE or small(w) is not None

def convert(text):
    toks = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?|[^A-Za-z]+", text)
    out = []; i = 0
    while i < len(toks):
        w = toks[i]; lw = w.lower()
        if isnum(lw) and lw not in SCALE:
            # gather run of number words separated by spaces / 'and'
            run = [lw]; j = i + 1
            while j + 1 < len(toks) and toks[j] == " " and (isnum(toks[j + 1].lower()) or (toks[j + 1].lower() == "and" and j + 3 < len(toks) and isnum(toks[j + 3].lower()))):
                run.append(toks[j + 1].lower()); j += 2
            # look ahead for unit / decimal
            nxt = toks[j + 1].lower() if j + 1 < len(toks) and toks[j] == " " else ""
            # years: "twenty twenty-two", "twenty fifteen"
            if len(run) == 2 and run[0] == "twenty" and small(run[1]) is not None and 10 <= small(run[1]) <= 99:
                out.append(str(2000 + small(run[1]))); i = j; continue
            # "seven fifty" / "three fifty" style prices: two smalls, second is tens
            pair_price = len(run) == 2 and small(run[0]) is not None and small(run[0]) < 10 and run[1] in T
            val = (small(run[0]) * 100 + T[run[1]]) if pair_price else parse(run)
            dec = ""
            if nxt == "point" and j + 3 < len(toks) and small(toks[j + 3].lower()) is not None:
                dec = "." + str(small(toks[j + 3].lower())); j += 4; nxt = toks[j + 1].lower() if j + 1 < len(toks) and toks[j] == " " else ""
            scale_word = ""
            if run[-1] in ("billion", "million"):
                scale_word = " " + run[-1]; val = parse(run[:-1])
            num = f"{val:,}" if val >= 10000 else str(val)
            if pair_price: num = f"{small(run[0])}.{T[run[1]]:02d}" if nxt == "dollars" or (out and out[-1].strip().endswith("$")) else str(val)
            s = num + dec + scale_word
            if nxt in ("pounds", "pound"): out.append("£" + s); i = j + 2; continue
            if nxt in ("dollars", "dollar"): out.append("$" + s); i = j + 2; continue
            if nxt == "percent": out.append(s + "%"); i = j + 2; continue
            if len(run) == 1 and lw in KEEP_WORDS and not dec:
                out.append(w); i += 1; continue
            out.append(s if not w[0].isupper() or len(run) > 1 or lw not in KEEP_WORDS else w); i = j; continue
        out.append(w); i += 1
    return "".join(out)

if __name__ == "__main__":
    import json, sys
    for l in json.load(open(sys.argv[1])):
        c = convert(l["text"])
        if c != l["text"]: print(l["id"], "|", c)
