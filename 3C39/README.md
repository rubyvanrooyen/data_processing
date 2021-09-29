## get 4k data and image occultation source

### wideband data (4k)
mvftoms.py -f --flags cam https://archive-gw-1.kat.ac.za/1627186156/1627186156_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhc
mNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjMyMTQzODM0LCJwcmVmaXgiOlsiMTYyNzE4NjE1NiJdLCJleHAiOjE2MzI3NDg2MzQsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.iYVYOJ38Pc-AtLCLK86SAT7MTLW
24zMc-EpyxZb0rT5F9ae51mwXzyN4kQ0NYdaUu3mQQNA0U1z2WP98Ulxm4g

### narrow band data (54M)
mvftoms.py -f --flags cam https://archive-gw-1.kat.ac.za/1627186165/1627186165_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhc
mNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjMyMTQzODM0LCJwcmVmaXgiOlsiMTYyNzE4NjE2NSJdLCJleHAiOjE2MzI3NDg2MzQsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.Zr3Jkpw9BDWCOm4D4qrDmWHHFku
sxbBALwJP70oidzDtkzThQRXOZfUfqmOJb1oilzuUllWYr_Xj3UTvb1693g


./getms.sh -r 163,3885 -s 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61 https://archive-gw-1.kat.ac.za/1627186156/1627186156_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI3MzAyMDc4LCJwcmVmaXgiOlsiMTYyNzE4NjE1NiJdLCJleHAiOjE2Mjc5MDY4NzgsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.zuCafamYKB4HqP24oWEr5pWFOhfqQP0Ya2iSJYS5t-uMTksLA1liPhkCH9TD9BMVIz3kDDA0X_oXqysa8pK-4Q

mvftoms.py -f --flags cam
Autocorrs can be a useful diagnostic, and cutting out the band rolloff saves very little,
I'd rather keep uniform channelization in the original MS.
And I understand the CAM flags are actually useful

mvftoms.py -f -a --flags '' -C 163,3885 --scans=1,3,5,7,9,11,13,15,17,19,21 https://archive-gw-1.kat.ac.za/1626935818/1626935818_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJp
c3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI2OTU2NjMwLCJwcmVmaXgiOlsiMTYyNjkzNTgxOCJdLCJleHAiOjE2Mjc1NjE0MzAsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJz
Y29wZXMiOlsicmVhZCJdfQ.wye2P0SprT-13CZLcWLYhhyeg_NLwgUWFOJUoku2BcKuEnKcUTPQ3uh_AoyY05tUdD0Wvy7WkaNRdLYkvub6Og

Targets: 3 selected out of 3 in catalogue
  ID  Name        Type      RA(J2000)     DEC(J2000)  Tags                    Dumps  ModelFlux(Jy)
   0  J0408-6545  radec      4:08:20.38  -65:45:09.1  fluxcal bpcal delaycal    135  
   1  J0108+0134  radec      1:08:38.77    1:35:00.3  gaincal                   208  
   2  3c39        radec      1:21:00.05    3:44:20.7  target                   1438 


## make measurement read only to prevent CASA from corrupting the MS
chmod -w 1627186156_sdp_l0.ms/


## run caracal pipeline
caracal -c run-3c39-4k.yml

-fin-
