from pyArango.collection import Collection, Edges, Field
from pyArango.graph import Graph, EdgeDefinition

"""
This module defines the classes requried by pyArango to handle the graph data
"""


class Titles(Collection):
    _fields = {
        "tconst": Field(),         # alphanumeric unique identifier of the title
        "titleType": Field(),      # the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
        "primaryTitle": Field(),   # the more popular title / the title used by the filmmakers on promotional materials at the point of release
        "originalTitle": Field(),  # original title, in the original language
        "isAdult": Field(),        # 0: non-adult title; 1: adult title
        "startYear": Field(),      # represents the release year of a title. In the case of TV Series, it is the series start year
        "endYear": Field(),        # TV Series end year. ‘\N’ for all other title types
        "runtimeMinutes": Field(), # primary runtime of the title, in minutes
        "genres": Field(),         # includes up to three genres associated with the title
    }
    _csv_headers = ["_key", "titleType", "primaryTitle", "originalTitle", "isAdult", "startYear", "endYear", "runtimeMinutes", "genres"]


class People(Collection):
    # Edges knownFor (tconst)
    _fields = {
        "nconst": Field(),
        "primaryName": Field(),
        "birthYear": Field(),
        "deathYear": Field(),
        "primaryProfession": Field()
    }
    _csv_headers = ["_key", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles", ]

    _edges = [{'collection': 'KnownFor',
               'to': 'Titles',
               'key': 'knownForTitles'}]


class TitleAlias(Collection):
    _fields = {
        "ordering": Field(),         # a number to uniquely identify rows for a given titleId
        "title": Field(),         # the localized title
        "region": Field(),         # the region for this version of the title
        "language": Field(),         # the language of the title
        "types": Field(),         # Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
        "attributes": Field(),         # Additional terms to describe this alternative title, not enumerated
        "isOriginalTitle": Field(),         # 0: not original title; 1: original title
    }


class Crews(Collection):
    pass


class Episodes(Collection):
    # Edge series(tconst)  # alphanumeric identifier of the parent TV Series
    _fields = {
        "seasonNumber": Field(),         # season number the episode belongs to
        "episodeNumber": Field(),         # episode number of the tconst in the TV series
    }


class Principals(Collection):
    _fields = {
        "ordering": Field(),         # a number to uniquely identify rows for a given titleId
        "category": Field(),         # the category of job that person was in
        "job": Field(),              # the specific job title if applicable, else '\N'
        "characters": Field(),       # the name of the character played if applicable, else '\N'
    }


class Ratings(Collection):
    _fields = {
        "averageRating": Field(),       # weighted average of all the individual user ratings
        "numVotes": Field(),            # number of votes the title has received
    }


class Alias(Edges):
    pass


class Crew(Edges):
    pass


class Principal(Edges):
    pass


class Director(Edges):
    pass


class Writer(Edges):
    pass


class EpisodeInfo(Edges):
    pass


class Worker(Edges):
    pass


class KnownFor(Edges):
    pass


class IMDB(Graph):
    _edgeDefinitions = [EdgeDefinition("Alias", fromCollections=["Titles"], toCollections=["TitleAlias"]),
                        EdgeDefinition("Crew", fromCollections=["Titles"], toCollections=["Crews"]),
                        EdgeDefinition("EpisodeInfo", fromCollections=["Titles"], toCollections=["Episodes"]),
                        EdgeDefinition("Principal", fromCollections=["Titles"], toCollections=["Principals"]),
                        EdgeDefinition("Worker", fromCollections=["Principals"], toCollections=["People"]),
                        EdgeDefinition("Director", fromCollections=["Crews"], toCollections=["People"]),
                        EdgeDefinition("Writer", fromCollections=["Crews"], toCollections=["People"]),
                        EdgeDefinition("KnownFor", fromCollections=["People"], toCollections=["Titles"]),

                        ]
    _orphanedCollections = []


collections = ["Titles", "TitleAlias", "Crews", "Episodes", "Principals", "People", "Alias", "Crew", "EpisodeInfo",
               "Principal", "Worker", "Director", "Writer", "KnownFor"]
