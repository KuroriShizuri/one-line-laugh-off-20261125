#!/usr/bin/env python3
"""One-line laugh-off: explaining the job to grandma.

The entry is one joke line: grandma asks what the job is, the answer is
"arguing with a robot for money", and her nod lands as if it finally
explains the whole childhood. This program is the delivery mechanism —
it checks the line fits the 200-character, single-line limit and writes
it to entry.txt for the make.fun harness.

    python3 main.py              write entry.txt
    python3 main.py --check      validate only, no file written
    python3 main.py --self-test  validate, write, read back, compare

Output goes to MAKEFUN_OUTPUT_DIR when set, otherwise the working
directory. Deterministic, standard library only, no network use.
"""

import os
import sys

ENTRY = (
    "My grandma asked what I do for a living, so I said 'I argue with a "
    "robot for money' \u2014 she nodded like that finally explained my "
    "childhood."
)

MAX_LEN = 200
OUT_NAME = "entry.txt"


def fail(msg):
    print("error: %s" % msg, file=sys.stderr)
    sys.exit(1)


def validate(text):
    """Return True when the text satisfies every competition rule.

    Rules are checked in order of how likely an edit is to break them:
    length first, then the single-line shape, then stray control bytes.
    """
    if text == "":
        fail("entry is empty")
    if len(text) > MAX_LEN:
        fail("entry is %d chars, over the %d limit" % (len(text), MAX_LEN))
    if "\n" in text:
        fail("entry must be a single line")
    if "\r" in text:
        fail("entry contains a carriage return")
    return True


def write_out():
    validate(ENTRY)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, OUT_NAME)
    data = (ENTRY + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        reread = fh.read()
    if reread != data:
        fail("entry.txt bytes do not match the entry")
    text_back = reread.decode("utf-8")
    if text_back != ENTRY + "\n":
        fail("entry.txt text does not match the entry")
    validate(text_back.rstrip("\n"))
    print("wrote %s (%d bytes)" % (path, len(data)))


def main():
    args = sys.argv[1:]
    if args == ["--check"]:
        validate(ENTRY)
        print("check ok: %d chars, single line" % len(ENTRY))
    elif args == ["--self-test"]:
        write_out()
        print("self-test ok")
    elif args == []:
        write_out()
    else:
        fail("unknown arguments: %s" % " ".join(args))


if __name__ == "__main__":
    main()
