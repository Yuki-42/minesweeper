"""
Database module for the server
"""

# Standard Library Imports
from typing import List

# Third Party Imports
from psycopg2 import connect, sql
from psycopg2.sql import SQL
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictCursor

# Local Imports
from .datatypes import User



