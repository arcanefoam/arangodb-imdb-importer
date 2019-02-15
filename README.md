#README

Importing this way takes a LOT of time. To make it easier to do this in separate batches, I recommend splitting the
source files in chunks of 100k lines.

## Getting the imdb data

You can get the latest version of the imdb from [IMDB](https://www.imdb.com/interfaces/). You can expand the downloads
into any location in your pc.
The split_csv.sh script can be used for splitting the huge csv files. It accepts the name of the file to
split and the number of lines per chunk. If you use this script, the importer script will use the split file name
pattern to intelligently process only files that have not been processed yet.

