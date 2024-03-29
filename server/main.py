"""
Main file for the project
"""

# Standard Library Imports

# Third Party Imports
from flask import Flask, session, request, redirect, url_for as urlFor, render_template as renderTemplate
from flask_cors import CORS
from flask_socketio import SocketIO

# Local Imports

