# SABLE v4 - Docker
Docker image for SABLE v4 http://sable.cchmc.org/

The images packages SABLE v4 and the required BLAST databases.

### How to build this image
The image can be build on linux (curl is required to be installed on the docker host) by running
```console
./build.sh
```

During the build process sequences required for the BLAST database used by SABLE are automatically downloaded and built into a BLAST database. The BLAST database is included into the final docker image. Therefore, the resulting image will be quite large.

## How to run this image
Once the image has been built predictions can be run by executing
```console
docker -i --rm sable < input_seq.fasta > result.txt
```
Single and multiple sequence FASTA files are supported. Prediction results (OUT_SABLE_RES) are written to stdout.

## Some words of caution
### Results differ from official SABLE server
Prediction from this image differ from the prediction made by the official SABLE server hosted at http://sable.cchmc.org/. At the moment I can unfortunately only speculated why the results are different. The most obvious difference between SABLE v4, which is packed into this docker image, and the SABLE server is that SABLE v4 makes use of much smaller BLAST databases. This is also mentioned in the SABLE v4 README along with a note on improved prediction quality due to reduced sequence database size - [check it out](http://sourceforge.net/projects/meller-sable/files/sable_v4_distr.tar.gz/download). 

Comparison of predictions from SABLE server and SABLE v4 packaged into this image using 250 randomly selected human proteins have shown a high agreement for random coil but for alpha helix and beta sheet agreement was less than 90% and 80%, respectively:
<table style="color: black; font-weight: bold; text-align:center; border-spacing: 10px;" border = "1">
<tr style="font-weight: bold" >
<td>SABLE<br>server/docker</td><td>C</td><td>E</td><td>H</td>
</tr>
<tr>
<td style="font-weight: bold">C</td>
<td style="background: rgb(255, 18.0, 18.0)">93%<br>80460</td><td style="background: rgb(255, 250.0, 250.0)">2%<br>1390</td><td style="background: rgb(255, 242.0, 242.0)">5%<br>4209</td>
</tr>
<tr>
<td style="font-weight: bold">E</td>
<td style="background: rgb(255, 204.0, 204.0)">20%<br>2938</td><td style="background: rgb(255, 61.0, 61.0)">76%<br>11138</td><td style="background: rgb(255, 245.0, 245.0)">4%<br>527</td>
</tr>
<tr>
<td style="font-weight: bold">H</td>
<td style="background: rgb(255, 224.0, 224.0)">12%<br>4976</td><td style="background: rgb(255, 252.0, 252.0)">1%<br>294</td><td style="background: rgb(255, 33.0, 33.0)">87%<br>36364</td>
</tr>
</table>

In the same set of sequences concordance of solvent accessibility prediction result from SABLE server and SABLE v4 is even lower:
<table style="color: black; font-weight: bold; text-align:center; border-spacing: 10px;" border ="1">
<tr style="font-weight: bold">
<td>SABLE<br>server/docker</td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td>
</tr>
<tr>
<td style="font-weight: bold">0</td>
<td style="background: rgb(255, 43.0, 43.0)">83%<br>20602</td><td style="background: rgb(255, 222.0, 222.0)">13%<br>3311</td><td style="background: rgb(255, 247.0, 247.0)">3%<br>645</td><td style="background: rgb(255, 252.0, 252.0)">1%<br>267</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>118</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>29</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>0</td>
</tr>
<tr>
<td style="font-weight: bold">1</td>
<td style="background: rgb(255, 219.0, 219.0)">14%<br>2927</td><td style="background: rgb(255, 115.0, 115.0)">55%<br>11661</td><td style="background: rgb(255, 204.0, 204.0)">20%<br>4339</td><td style="background: rgb(255, 237.0, 237.0)">7%<br>1516</td><td style="background: rgb(255, 247.0, 247.0)">3%<br>664</td><td style="background: rgb(255, 252.0, 252.0)">1%<br>229</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>3</td>
</tr>
<tr>
<td style="font-weight: bold">2</td>
<td style="background: rgb(255, 250.0, 250.0)">2%<br>356</td><td style="background: rgb(255, 212.0, 212.0)">17%<br>3698</td><td style="background: rgb(255, 150.0, 150.0)">41%<br>8875</td><td style="background: rgb(255, 184.0, 184.0)">28%<br>6015</td><td style="background: rgb(255, 229.0, 229.0)">10%<br>2197</td><td style="background: rgb(255, 250.0, 250.0)">2%<br>532</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>7</td>
</tr>
<tr>
<td style="font-weight: bold">3</td>
<td style="background: rgb(255, 255.0, 255.0)">0%<br>98</td><td style="background: rgb(255, 245.0, 245.0)">4%<br>1123</td><td style="background: rgb(255, 214.0, 214.0)">16%<br>4366</td><td style="background: rgb(255, 150.0, 150.0)">41%<br>10977</td><td style="background: rgb(255, 179.0, 179.0)">30%<br>7968</td><td style="background: rgb(255, 237.0, 237.0)">7%<br>1912</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>39</td>
</tr>
<tr>
<td style="font-weight: bold">4</td>
<td style="background: rgb(255, 255.0, 255.0)">0%<br>36</td><td style="background: rgb(255, 252.0, 252.0)">1%<br>436</td><td style="background: rgb(255, 242.0, 242.0)">5%<br>1505</td><td style="background: rgb(255, 207.0, 207.0)">19%<br>5595</td><td style="background: rgb(255, 127.0, 127.0)">50%<br>15118</td><td style="background: rgb(255, 194.0, 194.0)">24%<br>7331</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>99</td>
</tr>
<tr>
<td style="font-weight: bold">5</td>
<td style="background: rgb(255, 255.0, 255.0)">0%<br>8</td><td style="background: rgb(255, 252.0, 252.0)">1%<br>172</td><td style="background: rgb(255, 247.0, 247.0)">3%<br>488</td><td style="background: rgb(255, 240.0, 240.0)">6%<br>1027</td><td style="background: rgb(255, 181.0, 181.0)">28%<br>4949</td><td style="background: rgb(255, 107.0, 107.0)">57%<br>9838</td><td style="background: rgb(255, 247.0, 247.0)">3%<br>479</td>
</tr>
<tr>
<td style="font-weight: bold">6</td>
<td style="background: rgb(255, 255.0, 255.0)">0%<br>1</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>1</td><td style="background: rgb(255, 250.0, 250.0)">2%<br>13</td><td style="background: rgb(255, 247.0, 247.0)">3%<br>23</td><td style="background: rgb(255, 232.0, 232.0)">9%<br>67</td><td style="background: rgb(255, 112.0, 112.0)">56%<br>415</td><td style="background: rgb(255, 179.0, 179.0)">30%<br>221</td>
</tr>
</table>

## Benchmark
The SABLE v4 distribution includes benchmark datasets that were used to evaluate prediction accuracy using different BLAST databases. According to the results included in theSABLE v4 distribution archive the authors observed a prediction accuracy of 79.1% for the dataset of 135 sequences using sequences included in the PFAM database as primary BLAST database. Using this docker image prediction accuracy for the same dataset was 79%. Agreement for random coil and alpha helix was above 80%, but almost 30% of residues annotated with beta sheet in the reference data were predicted as random coil by SABLE v4.
<table style="color: black; font-weight: bold; text-align:center; border-spacing: 10px;">
<tr style="font-weight: bold">
<td>expected/actual</td><td>C</td><td>E</td><td>H</td><td>X</td>
</tr>
<tr>
<td style="font-weight: bold">C</td>
<td style="background: rgb(255, 48.0, 48.0)">81%<br>10308</td><td style="background: rgb(255, 235.0, 235.0)">8%<br>990</td><td style="background: rgb(255, 227.0, 227.0)">11%<br>1361</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>0</td>
</tr>
<tr>
<td style="font-weight: bold">E</td>
<td style="background: rgb(255, 181.0, 181.0)">28%<br>2041</td><td style="background: rgb(255, 84.0, 84.0)">67%<br>4757</td><td style="background: rgb(255, 245.0, 245.0)">4%<br>269</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>0</td>
</tr>
<tr>
<td style="font-weight: bold">H</td>
<td style="background: rgb(255, 217.0, 217.0)">15%<br>1839</td><td style="background: rgb(255, 252.0, 252.0)">1%<br>172</td><td style="background: rgb(255, 43.0, 43.0)">83%<br>10096</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>0</td>
</tr>
<tr>
<td style="font-weight: bold">X</td>
<td style="background: rgb(255, 13.0, 13.0)">95%<br>296</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>1</td><td style="background: rgb(255, 242.0, 242.0)">5%<br>16</td><td style="background: rgb(255, 255.0, 255.0)">0%<br>0</td>
</tr>
</table>