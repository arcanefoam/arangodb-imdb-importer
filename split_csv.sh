#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters. You must provide a file name to split and the split size"
    exit 1
fi
name=${1%.*}_
echo $name
tail -n +2 $1 | split -l $2 $1 $name
for file in ${name}*
do
    head -n 1 $1 > tmp_file
    cat "$file" >> tmp_file
    mv -f tmp_file "$file"
done