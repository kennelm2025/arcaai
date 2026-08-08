---
name: hash-verify
description: SHA256 hash-pinned transfer verification for an artefact. Compute the hash of a file and compare against the pinned value. Use whenever an artefact crosses a machine or session boundary.
allowed-tools: Bash(python:*)
---

# Hash verify — pinned transfer check

Arguments: $ARGUMENTS
(Form: `<path> [expected-sha256]`. If no expected hash is given,
compute and report only.)

# Your task

1. Compute the SHA256 of the file using Python stdlib
   (cross-platform; do not use certutil or shasum):
   `python -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <path>`
2. If an expected hash was provided, compare **the full digest,
   character for character** — never a prefix. Report VERIFIED or
   MISMATCH in those words.
3. On MISMATCH: stop. Do not open, ingest, list, or act on the
   artefact. Report both digests and hand back to the operator.
4. On VERIFIED: report the digest so it can be recorded in the
   relevant governed record.
