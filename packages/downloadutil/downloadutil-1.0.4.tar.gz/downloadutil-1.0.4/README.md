# downloadutil
A Python module with common utilities for downloading and extracting archives.

Use cases:
- Download an archive from a URL and the expected SHA256 checksum from the same URL with a ".sha256"
  suffix appended. Verify the checksum.
- Download an archive as above and extract it into a target directory, and still keep the archive in
  a special cache directory.

# Usage as a command-line tool

Invoke as `downloadutil` or `python3 -m downloadutil`.

```
usage: downloadutil [-h] --url URL [--dest-dir-parent DEST_DIR_PARENT] [--cache-dir CACHE_DIR] [--no-cache] [--verify-checksum] [--verbose]

options:
  -h, --help            show this help message and exit
  --url URL             URL to download.
  --dest-dir-parent DEST_DIR_PARENT
                        Parent directory in which to extract the archive
  --cache-dir CACHE_DIR
                        Download cache directory on the locally mounted disk. Must have enough space.
  --no-cache            Do not use a cache directory
  --verify-checksum     In addition to downloading the given URL, also download the SHA256 checksum file from the URL obtained by appending an .sha256 suffix, and verifying the checksum.
  --verbose             Verbose logging
```
