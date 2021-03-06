"""
    ydf/yaml_ext
    ~~~~~~~~~~~~

    Contains extensions to existing YAML functionality.
"""

import collections
import io
import os

from ruamel import yaml
from ruamel.yaml import resolver


__all__ = ['load', 'load_all', 'load_all_gen', 'load_file', 'load_files']


class OrderedRoundTripLoader(yaml.RoundTripLoader):
    """
    Extends the default round trip YAML loader to use :class:`~collections.OrderedDict` for mapping
    types.
    """

    def __init__(self, *args, **kwargs):
        super(OrderedRoundTripLoader, self).__init__(*args, **kwargs)
        self.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, self.construct_ordered_mapping)

    @staticmethod
    def construct_ordered_mapping(loader, node):
        loader.flatten_mapping(node)
        return collections.OrderedDict(loader.construct_pairs(node))


def load_file(path):
    """
    Load a single document from the YAML file at the given path.

    :param path: Path to YAML file on disk.
    :return: An :class:`~collections.OrderedDict` representation of the YAML stream.
    """
    with io.open(os.path.abspath(path), 'r') as f:
        return load(f.read())


def load_files(paths):
    """
    Load and yield a YAML document for each file path given.

    :param paths: Sequence of file paths that point to YAML documents.
    :return: A generator that yields YAML documents from the given file paths.
    """
    for path in paths:
        yield load_file(path)


def load(stream):
    """
    Load a single document within the given YAML string.

    :param stream: A valid YAML stream.
    :return: An :class:`~collections.OrderedDict` representation of the YAML stream.
    """
    return yaml.load(stream, OrderedRoundTripLoader)


def load_all(stream):
    """
    Load all documents within the given YAML string.

    :param stream: A valid YAML stream.
    :return: List that contains all documents found in the YAML stream.
    """
    return list(load_all_gen(stream))


def load_all_gen(stream):
    """
    Load all documents within the given YAML string.

    :param stream: A valid YAML stream.
    :return: Generator that yields each document found in the YAML stream.
    """
    return yaml.load_all(stream, OrderedRoundTripLoader)
