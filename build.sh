#!/bin/bash

set -e

WORK="resources"
[ -d "${WORK}" ] && (echo "ABORTING - directory ${WORK} already exists" >&2; exit 1)
mkdir "${WORK}"
echo "downloading into: ${WORK}"

curl -L "https://sourceforge.net/projects/meller-sable/files/sable_v4_distr.tar.gz/download" > "${WORK}/sable_v4_distr.tar.gz"
tar -C "${WORK}" -zxf "${WORK}/sable_v4_distr.tar.gz"
find "${WORK}" -wholename "*GI_indexes/*index" -print0 | xargs -0 cat | sort -u > "${WORK}/sequence_ids.txt"
cp fetch_sequences.py "${WORK}"
docker run -i --rm -v "$(readlink -f "${WORK}")":/data python:3.10-alpine \
    /bin/ash -c 'pip -q install "aiohttp" && python /data/fetch_sequences.py /data/sequence_ids.txt' > "${WORK}/sequences.fasta" 2> "${WORK}/sequences.err"

docker build -t sable .
