"""Main module."""
from .decays import *
import sqlalchemy as db

from . element import Element

from nuclides.utils.gen_db import Decays, Nuclides, Elements, Base


