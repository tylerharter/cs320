import os, sys, json
from collections import namedtuple

Snippet = namedtuple("Snippet", ["start", "end", "text"])

def chunk(infile, outfile):
    snippets = []
    with open(infile) as f:
        chunks = f.read().split("\n\n")

    for chunk in chunks:
        if not chunk.strip():
            continue
        times, text = chunk.split("\n")
        snippets.append(Snippet(*times.split(","), text.strip()))

    combined = []

    for i in range(0, len(snippets) - 1, 2):
        s1 = snippets[i]
        s2 = snippets[i+1]
        if len(s1.text) + len(s2.text) < 100:
            s3 = Snippet(s1.start, s2.end, s1.text + " " + s2.text)
            combined.append(s3)
        else:
            combined.extend([s1,s2])

    if len(snippets) % 2:
        combined.append(snippets[-1])

    with open(outfile, "w") as f:
        for s in combined:
            f.write(f"{s.start},{s.end}\n{s.text}\n\n")

def main():
    for dirname in os.listdir("."):
        if not os.path.isdir(dirname):
            continue
        for infile in os.listdir(dirname):
            if infile.endswith(".orig"):
                infile = os.path.join(dirname, infile)
                outfile = infile.replace(".orig", ".new")
                print(outfile)
                chunk(infile, outfile)

if __name__ == '__main__':
     main()
