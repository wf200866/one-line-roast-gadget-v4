"""A one-liner about fitness tracking gone sideways: the wrist tells you
you crushed ten thousand steps, but most of those laps were paced while
stuck on hold with a bank's phone tree."""

import os
import tempfile

JOKE = "My smartwatch congratulated me on 10,000 steps; 9,000 of them were just me pacing the hall on hold with my bank."

OUT_PATH = "/output"
TARGET_NAME = "entry.txt"
TARGET_PATH = os.path.join(OUT_PATH, TARGET_NAME)
LO = 1
HI = 200


def validate(text):
    """Guard the payload: non-blank and within the allowed span."""
    if not text or text.strip() == "":
        raise ValueError("empty roast rejected")
    n = len(text)
    if not (LO <= n <= HI):
        raise ValueError("roast length %d outside %d..%d" % (n, LO, HI))
    return text


def ensure_output_dir():
    """Make sure /output exists and can be entered; return the final path."""
    os.makedirs(OUT_PATH, mode=0o755, exist_ok=True)
    os.chmod(OUT_PATH, 0o755)
    return TARGET_PATH


def atomic_write(text):
    """Write through a temp sibling inside /output, then rename over target."""
    final_path = ensure_output_dir()
    fd, tmp = tempfile.mkstemp(prefix="entry-", suffix=".tmp", dir=OUT_PATH)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(text.encode("utf-8"))
        os.chmod(tmp, 0o644)
        os.replace(tmp, final_path)
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass
    os.chmod(final_path, 0o644)
    return final_path


def main():
    line = validate(JOKE)
    where = atomic_write(line)
    print("length=%d file=%s" % (len(line), where))


if __name__ == "__main__":
    main()
