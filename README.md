# README

Importing this way takes a LOT of time. To make it easier I recomend splitting the
source files in chunks of 100k lines (or so) so it is easier to skip information already processed.

## Getting the imdb data

You can get the latest version of the imdb from [IMDB](https://www.imdb.com/interfaces/). You can expand the downloads
into any location in your pc.

## Splitting the files

The split_csv.sh script can be used for splitting the huge csv files. It accepts the name of the file to
split and the number of lines per chunk. If you use this script, the importer script will use the split file name
pattern to intelligently process only files that have not been processed yet.

## Running the importer

The commited version has only some of the files included for importing and some of them are commented. To do a full import, uncomment and add missing data you want to import. Alternatively comment/uncomment specifc portions of data. On systems with low memory (or to avoid distruptig your usual work) I recommend importing one data set at a time. 

