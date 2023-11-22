import os

from ecoindex.utils.sync_version import read_version_from_file

current_directory = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(current_directory, "VERSION")

ecoindex_api_version = read_version_from_file(filename)
