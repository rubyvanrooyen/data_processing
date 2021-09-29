#! /bin/bash

# G330 wideband 4k data
## mvftoms.py -f -a --flags cam --target=name -C '0,N' bla
# 67P wideband 4k data
## mvftoms.py -f -a --flags cam --scans=scan,list -C '0,N' bla
# ./getms.sh -r 163,3885 -s 1,3,5,7,9,11,13,15,17,19,21 https://archive-gw-1.kat.ac.za/1626935818/1626935818_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI2OTU2NjMwLCJwcmVmaXgiOlsiMTYyNjkzNTgxOCJdLCJleHAiOjE2Mjc1NjE0MzAsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.wye2P0SprT-13CZLcWLYhhyeg_NLwgUWFOJUoku2BcKuEnKcUTPQ3uh_AoyY05tUdD0Wvy7WkaNRdLYkvub6Og

if [ "$#" -lt 1 ]
then
  echo "katdal token input required: $0 [-s <scan,list>] [-r <chan,range>] [-t <target>] <token>"
  exit
fi

CMD="mvftoms.py -f -a --flags cam"

while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    -r)
      chanrange=$2
      CMD="$CMD -C $chanrange"
      shift # past argument
      shift # past value
      ;;
    -s)
      scanlist=$2
      CMD="$CMD --scans=$scanlist"
      shift # past argument
      shift # past value
      ;;
    -t)
      targetname=$2
      CMD="$CMD -o $targetname.ms --target $targetname"
      shift # past argument
      shift # past value
      ;;
    *) # token remaining
      token=$1
      shift # past value
      ;;
  esac
done

CMD="$CMD $token"
echo
echo $CMD
echo

$CMD

# -fin-
