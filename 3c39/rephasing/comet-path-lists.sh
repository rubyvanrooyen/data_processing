
#! /bin/bash


counter=0
DEFAULTIFS=$IFS
# for msfile in `ls -d ../split_integrations/1627186156_sdp_l0-67p-*-rephased.ms`
for msfile in `ls -d ../1627186156_sdp_l0-67p-*-rephased.ms`
do
  echo "counter, $counter"
#   imfile="comet67p.$counter.wsclean"
# 
  # Set dash as delimiter
  IFS='-'
  # Read the split words into an array based on comma delimiter
  read -a msfilearr <<< "$msfile"
  IFS=$DEFAULTIFS
#   # Print each value of the array by using the loop
#   echo "There are ${#msfilearr[*]} words in the text."
#   for val in "${msfilearr[@]}";
#   do
#     printf "$val\n"
#   done
  echo "The value you want from $msfile is ${msfilearr[2]}"

  for fitsim in `ls -d comet67p.$counter.wsclean-MFS-*.fits`
  do
#     echo "update $fitsim"
    IFS='.'
    # Read the split words into an array based on comma delimiter
    read -a fitsfilearr <<< "$fitsim"
    IFS=$DEFAULTIFS
#     echo "There are ${#fitsfilearr[*]} words in the text."
#     echo "${fitsfilearr[0]}.${msfilearr[2]}.${fitsfilearr[2]}.${fitsfilearr[3]}"
    newfitsim="${fitsfilearr[0]}.${msfilearr[2]}.${fitsfilearr[2]}.${fitsfilearr[3]}"
    echo "mv $fitsim $newfitsim"
    mv $fitsim $newfitsim
  done

#   break
  counter=$((counter+1))
done

# - fin-
