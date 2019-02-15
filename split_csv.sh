name=${1%.*}_
echo $name
tail -n +2 $1 | split -l $2 $1 $name
for file in ${name}*
do
    head -n 1 $1 > tmp_file
    cat "$file" >> tmp_file
    mv -f tmp_file "$file"
done