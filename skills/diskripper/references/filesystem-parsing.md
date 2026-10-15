# Filesystem parsing notes — diskripper-core

Detection lives in `diskripper-core/src/filesystem/mod.rs::detect_filesystem`.
Verified offsets (2048-byte sectors, absolute byte offsets):

- ISO 9660 Primary Volume Descriptor: LBA 16 (0x8000), signature `CD001` at
  0x8001.
- Joliet Supplementary Volume Descriptor: LBA 17 (0x8800), signature `CD001`
  at 0x8801, escape sequences at SVD offset 0x58 → absolute **0x8858**.
  Joliet levels begin with bytes `25 2F` ("%/").
- UDF: `NSR02` / `NSR03` signature at 0x8001.

Rule: SVD-relative offsets are relative to the sector start (0x8800) —
convert to absolute before indexing. Reading the escape sequence from any
other offset silently misdetects Joliet discs as plain ISO 9660; a Joliet
round-trip test that detects plain `Iso9660` means the escape offset is wrong.
