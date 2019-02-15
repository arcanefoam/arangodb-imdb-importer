#README

Importing this way takes a LOT of time. To make it easier to do this in separate batches, I recommend splitting the
source files in chunks of 100k lines. The split_csv.sh script can be used for this. It accepts the name of the file to
split and the number of lines per chunk. If you use this script, the importer script will use the split file name
pattern to intelligently process only files that have not been processed yet.