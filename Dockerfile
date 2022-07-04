FROM i386/ubuntu:18.04

RUN apt-get update && \
   apt-get -y install ncbi-blast+

#downloading sequences during docker build fails   
#RUN apt-get update && \
#   apt-get -y install python3 python3-aiohttp

#will copy into image from the host as we need to get GI_index seq on the host before
#RUN mkdir /sable && \
#   curl -L https://sourceforge.net/projects/meller-sable/files/sable_v4_distr.tar.gz/download | tar -C /sable -zxf - 

ADD resources/sable_v4_distr.tar.gz /sable

RUN [ $(find /sable -name "run.sable" | wc -l) -eq 1 ] && \
   sed -i '/export SABLE_DIR=.*/a export SABLE_DIR="'"$(dirname "$(find /sable -name "run.sable")")"'"' "$(dirname "$(find /sable -name "run.sable")")/run.sable" && \
   sed -i '/export PRIMARY_DATABASE=.*/a export PRIMARY_DATABASE="${SABLE_DIR}/GI_indexes/pfam_index"' "$(dirname "$(find /sable -name "run.sable")")/run.sable" && \
   sed -i '/export SECONDARY_DATABASE=.*/a export SECONDARY_DATABASE="${SABLE_DIR}/GI_indexes/swissprot_index"' "$(dirname "$(find /sable -name "run.sable")")/run.sable" && \
   sed -i '/export BLAST_DIR=.*/a export BLAST_DIR="'"$(dirname /usr/bin/psiblast)"'"' "$(dirname "$(find /sable -name "run.sable")")/run.sable" && \
   ln -s "$(find /sable -name "run.sable")" "/bin/run.sable"

#downloading sequences during docker build fails
#RUN mkdir -p /database/ncbi && \
#   cat "$(dirname "$(find /sable -name "run.sable")")/GI_indexes/pfam_index" "$(dirname "$(find /sable -name "run.sable")")/GI_indexes/swissprot_index" | sort -u > /database/ncbi/gi.txt
#COPY fetch_sequences.py /tmp
#RUN python3 /tmp/fetch_sequences.py /database/ncbi/gi.txt > /database/ncbi/sequences.fasta

RUN mkdir -p /database/ncbi
COPY resources/sequences.fasta /database/ncbi/sequences.fasta
RUN makeblastdb -in /database/ncbi/sequences.fasta -out /database/ncbi/nr -dbtype prot -parse_seqids && \
   rm /database/ncbi/sequences.fasta

RUN apt-get update && \
   apt-get -y install patch

COPY sable.pl.patch /tmp
RUN patch "$(dirname "$(find /sable -name "run.sable")")/sable.pl" /tmp/sable.pl.patch && \
   rm /tmp/sable.pl.patch

RUN mkdir /workdir
COPY sable /workdir
WORKDIR /workdir
CMD ["./sable"]

