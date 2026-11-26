"""One-line roast gadget.

Angle: your watch throws confetti for a 10,000-step day, but most of those
steps were you wearing a groove in the hallway while the bank kept you on hold.

It writes exactly one line to /output/entry.txt. The write is atomic: stage a
temp file in /output, then rename it into place. Nothing ever chmods the
/output directory itself, because under the grader this process may be an
unprivileged user that does not own that directory.
"""

import os
import tempfile

JOKE = (
    "My smartwatch congratulated me on 10,000 steps; 9,000 of them were just "
    "me pacing the hall on hold with my bank."
)

# Bounds for a sane one-liner.
LOWER = 1
UPPER = 200


def validate(text):
    """Check the roast is present and within bounds; raise ValueError if not."""
    if not isinstance(text, str):
        raise ValueError("roast must be a string")
    if not text.strip():
        raise ValueError("roast must not be blank")
    size = len(text)
    if size < LOWER or size > UPPER:
        raise ValueError("roast is %d chars; expected %d-%d" % (size, LOWER, UPPER))
    return text


def _stage_and_commit(dest_dir, dest_name, text):
    """Stage text in dest_dir, then atomically rename to dest_name.

    chmod is applied only to newly created files, never to dest_dir.
    """
    handle, staged = tempfile.mkstemp(dir=dest_dir, prefix="entry-", suffix=".part")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.chmod(staged, 0o644)
        final = os.path.join(dest_dir, dest_name)
        os.replace(staged, final)
    except BaseException:
        try:
            os.remove(staged)
        except OSError:
            pass
        raise
    os.chmod(final, 0o644)
    return final


def main():
    line = validate(JOKE)
    os.makedirs("/output", exist_ok=True)
    _stage_and_commit("/output", "entry.txt", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
