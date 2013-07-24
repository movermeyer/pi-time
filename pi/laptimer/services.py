# API for interacting with models.

#from laptimer import Rider
#from laptimer import Track
#from laptimer import Session
#from laptimer import Lap
#from laptimer import Setting


# Rider related functions

def rider_add(name):
	pass

def rider_change(old_name, new_name):
	pass

def rider_remove(name):
	pass


# Track related functions

def track_add(name, distance, timeout):
	pass

def track_change(name, distance, timeout):
	pass

def track_remove(name):
	pass


# Session related functions

def session_start(track, name, started):
	pass

def session_finish(name, finished):
	pass

def session_remove(name):
	pass


# Lap related functions

def lap_start(session, rider, started):
	pass

def lap_finish(session, finished):
	pass

def lap_timeout(session):
	pass


# Query related functions

def get_fastest_lap_times(top=None, track=None, session=None, rider=None):
	pass

def get_average_lap_times(top=None, track=None, session=None, rider=None):
	pass

def get_lap_counts(top=None, track=None, session=None, rider=None):
	pass

def get_distance_ridden(top=None, track=None, session=None, rider=None):
	pass