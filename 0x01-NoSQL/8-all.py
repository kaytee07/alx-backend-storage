#!/usr/bin/env python3
"""
python script that list all collection in the document
"""


def list_all(mongo_collection):
    """
    what this function does is list all collections in a db
    """
    return mongo_collection.find()
