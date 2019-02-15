import csv
import glob
import os

import progressbar
from pyArango.connection import Connection
from pyArango.theExceptions import CreationError

from imdb import collections as imdbCols, Titles, People


def rawcount(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines


def connect_to_db(dbname, url='http://127.0.0.1:8529', username=None, password=None, createdb=False):
    conn = Connection(arangoURL=url, username=username, password=password)
    if createdb:
        conn.createDatabase(name=dbname)
    db = conn[dbname]
    return db


def create_collections(db, names):
    for c in names:
        try:
            db.createCollection(c)
        except CreationError:
            pass
        if c in db.collections:
            db.collections[c].deactivateCache()


def create_vertices(vertex_type, file, g):
    lines = rawcount(filename=file)
    collection_name = vertex_type.__name__
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect=csv.excel_tab, fieldnames=vertex_type._csv_headers)
        next(reader, None)  # skip the headers
        # label = click.style(f"Processing {collection_name}", fg='green')
        with progressbar.ProgressBar(max_value=lines, redirect_stdout=True) as bar:
            for row in reader:
                bar.update(reader.line_num)
                try:
                    g.createVertex(collection_name, row)
                except CreationError:
                    pass    # Ignore duplicate info FIXME this should be configurable
                try:
                    for e in vertex_type._edges:
                        values = row[e['key']].split(',')
                        try:
                            if 'to' in e:
                                for v in values:
                                    theGraph.createEdge(e['collection'],
                                                        _fromId=f"{collection_name}/{row['_key']}",
                                                        _toId=f"{e['to']}/{v}",
                                                        edgeAttributes=dict())
                            elif 'from' in e:
                                for v in values:
                                    theGraph.createEdge(e['collection'],
                                                        _toId=f"{collection_name}/{row['_key']}",
                                                        _fromId=f"{e['from']}/{v}",
                                                        edgeAttributes=dict())
                        except CreationError:
                            pass  # Ignore duplicate info FIXME this should be configurable
                except AttributeError:
                    pass


def files_for(path):
    """
    Looks for existing files created with the split.sh script and returns the files that have not been processed.
    If no file chunks are found, it returns the original file.
    :param path:
    :return:
    """
    files = glob.glob(f"{os.path.splitext(path)[0]}_*")
    if not files:
        files.append(path)
    files.sort()
    lines = []
    try:
        with open('.history', 'r') as h:
            lines = h.read().splitlines()
    except FileNotFoundError:
        pass
    for f in files:
        if f not in lines:
            yield f
            with open('.history', 'w') as h:
                h.write(f)


def process_file(vertex_type, path):
    for file in files_for(path):
        print(f"Processing {file}")
        create_vertices(vertex_type, file, theGraph)


if __name__ == '__main__':
    db = connect_to_db("epsilon", username='epsilon', password='epsilon')
    create_collections(db, imdbCols)
    theGraph = None
    try:
        theGraph = db.createGraph("IMDB")
    except CreationError:
        pass
    if theGraph is None:
        theGraph = db.graphs["IMDB"]
    # process_file(Titles, 'data/title.basics.tsv', theGraph)
    process_file(People, 'data/name.basics.tsv')

