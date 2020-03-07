# project: p2
# submitter: beninato
# partner: None

from datetime import datetime
from zipfile import ZipFile
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, asin, sqrt, pi

class BusDay():
    """Given a datetime, interacts with Madison Metro Transit General Transit Feed Specification"""
    dfs = dict() # all DataFrames are static variables, only read once
    with ZipFile('mmt_gtfs.zip') as zf:
        for name in ('calendar', 'trips', 'stop_times', 'stops'):
            with zf.open(f"{name}.txt") as f: # read into dictionary (bool multiply is a fancy if statement)
                dfs[name] = pd.read_csv(f, parse_dates=['start_date', 'end_date'] * (name == 'calendar'))

    def __init__(self, date):
        """creates a BusDay, sets service_ids, declares variables"""
        self.date = date if isinstance(date, datetime) else datetime(2020, 2, 21)
        weekday = date.strftime('%A').lower()
        df = self.dfs['calendar']
        df = df[(df['start_date'] <= date) & (df['end_date'] >= date) & (df[weekday] == 1)]
        self.service_ids = sorted(df['service_id'].values)
        self.trip_df = pd.DataFrame() # empty df
        self.stops = None # sorted list of stops
        self.trips = dict() # k,v = route_id, trips
        self.tree = None # tree holding stops

    def get_trips(self, route_id=None):
        """sorted list of all Trip objects for self.date"""
        if route_id not in self.trips:
            df = self.get_trip_df()
            if route_id != None:
                df = df[df['route_short_name'] == route_id]
            trips = {Trip(trip_id, name, bool(bikes)) for trip_id, name, bikes # zip with list comp is realy long
                     in zip(df.trip_id, df.route_short_name, df.bikes_allowed)}
            self.trips[route_id] = sorted(trips)
        return self.trips[route_id]

    def get_stops(self):
        """sorted list of all Stop objects for self.date"""
        if self.stops == None:
            stop_times_df = self.dfs['stop_times'] # filter down stops
            stop_ids_df = self.dfs['stops']
            trip_ids = self.get_trip_df()['trip_id'].unique()
            stop_times_df = stop_times_df[stop_times_df['trip_id'].isin(trip_ids)]
            stop_ids = stop_times_df['stop_id'].unique()
            stop_ids_df = stop_ids_df[stop_ids_df['stop_id'].isin(stop_ids)]
            # list comprehension is very wide but fast
            stops = {Stop(stop_id, Location(latlon=(lat, lon)), bool(wheelchair)) for stop_id, lat, lon, wheelchair
                     in zip(stop_ids_df.stop_id, stop_ids_df.stop_lat, stop_ids_df.stop_lon, stop_ids_df.wheelchair_boarding)}
            self.stops = sorted(stops)
        return self.stops

    def get_trip_df(self):
        """filter global trips df by current date"""
        if self.trip_df.empty:
            self.trip_df = self.dfs['trips'][self.dfs['trips']['service_id'].isin(self.service_ids)]
        return self.trip_df

    def get_tree(self):
        """get/generate tree"""
        if self.tree == None:
            self.tree = Node(self.get_stops())
        return self.tree

    def get_stops_rect(self, px, py):
        """search tree for stops in rectange"""
        return sorted(self.get_tree().get_stops(px, py))

    def get_stops_circ(self, origin, radius):
        """search tree for stops in rectange, filter down to circle"""
        x1, y1 = tuple(coord - radius for coord in origin)
        x2, y2 = tuple(coord + radius for coord in origin)
        stops = self.get_stops_rect((x1, x2), (y1, y2))
        return sorted(s for s in stops if s.location.dist(Location(xy=origin)) < radius)

    def scatter_stops(self, ax):
        """scatter all stops"""
        df = pd.DataFrame.from_records([s.to_dict() for s in self.get_stops()])
        df[df['wheelchair_boarding'] == True].plot.scatter(x='x',y='y', color='red', ax=ax)
        df[df['wheelchair_boarding'] == False].plot.scatter(x='x',y='y', color='0.7', ax=ax)

    def draw_tree(self, ax, tree=None, minx=-8, maxx=8, miny=-8, maxy=8):
        """recursively draw tree"""
        if tree == None: # root
            tree = self.get_tree()
        if tree.left == None or tree.right == None: # hit leaf, stop recursion
            return
        if tree.depth % 2 == 0: # east west
            ax.plot((tree.split_loc, tree.split_loc), (miny, maxy), lw=1.4**(6.3-tree.depth), color="purple", zorder=-10)
            self.draw_tree(ax=ax, tree=tree.left, minx=minx, maxx=tree.split_loc, miny=miny, maxy=maxy)
            self.draw_tree(ax=ax, tree=tree.right, minx=tree.split_loc, maxx=maxx, miny=miny, maxy=maxy)
        else:
            ax.plot((minx, maxx), (tree.split_loc, tree.split_loc), lw=1.4**(6.3-tree.depth), color="purple", zorder=-10)
            self.draw_tree(ax=ax, tree=tree.left, minx=minx, maxx=maxx, miny=miny, maxy=tree.split_loc)
            self.draw_tree(ax=ax, tree=tree.right, minx=minx, maxx=maxx, miny=tree.split_loc, maxy=maxy)

class Trip():
    """represents a Trip"""
    def __init__(self, trip_id, route_id, bikes_allowed):
        self.trip_id = trip_id
        self.route_id = route_id
        self.bikes_allowed = bikes_allowed
    def __repr__(self):
        return f'Trip({self.trip_id}, {self.route_id}, {self.bikes_allowed})'
    def __hash__(self):
        return hash(str(self))
    def __lt__(self, other):
        return isinstance(other, Trip) and self.trip_id < other.trip_id

class Stop():
    """represents a Stop"""
    def __init__(self, stop_id, location, wheelchair_boarding):
        self.stop_id = stop_id
        self.location = location
        self.wheelchair_boarding = wheelchair_boarding
    def __hash__(self):
        return hash(str(self))
    def __repr__(self):
        return f'Stop({self.stop_id}, {self.location}, {self.wheelchair_boarding})'
    def __lt__(self, other):
        return isinstance(other, Stop) and self.stop_id < other.stop_id
    def to_dict(self): # https://stackoverflow.com/a/41762270/7203518
        return { 'stop_id': self.stop_id, 'x': self.location.x, 'y': self.location.y, 
                 'wheelchair_boarding': self.wheelchair_boarding }

class Node():
    """recursively stores stops in tree"""
    def __init__(self, stops, depth=0):
        self.left = None
        self.right = None
        self.depth = depth
        if self.depth > 5:
            self.stops = stops
        else:
            idx = len(stops)//2
            if self.depth % 2 == 0: # east west
                stops = sorted(stops, key=lambda stop: stop.location.x)
                self.split_loc = stops[idx].location.x
            else:
                stops = sorted(stops, key=lambda stop: stop.location.y)
                self.split_loc = stops[idx].location.y
            self.left = Node(stops[:idx], depth=self.depth+1)
            self.right = Node(stops[idx:], depth=self.depth+1)

    def get_stops(self, px, py):
        """recursively get stops in rectangle"""
        def in_rect(stop, x1, x2, y1, y2):
            x0, y0 = stop.location.x, stop.location.y
            return x0 > x1 and x0 < x2 and y0 > y1 and y0 < y2
        x1, x2 = px
        y1, y2 = py
        if self.depth == 6:
            return [stop for stop in self.stops if in_rect(stop, x1, x2, y1, y2)]

        if self.depth % 2 == 0: # split east west
            min_value, max_value = x1, x2
        else:
            min_value, max_value = y1, y2

        if self.split_loc > max_value: # all stops are less than (east/south) split location
            return self.left.get_stops(px, py)
        elif self.split_loc < min_value: # all stops are greater than (west/north) split location
            return self.right.get_stops(px, py)
        else:
            return self.left.get_stops(px, py) + self.right.get_stops(px, py)

def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on earth using the
    harversine distance (distance between points on a sphere)
    See: https://en.wikipedia.org/wiki/Haversine_formula

    :param lat1: latitude of point 1
    :param lon1: longitude of point 1
    :param lat2: latitude of point 2
    :param lon2: longitude of point 2
    :return: distance in miles between points
    """
    lat1, lon1, lat2, lon2 = (a/180*pi for a in [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(min(1, sqrt(a)))
    d = 3956 * c
    return d

class Location:
    """Location class to convert lat/lon pairs to
    flat earth projection centered around capitol
    """
    capital_lat = 43.074683
    capital_lon = -89.384261

    def __init__(self, latlon=None, xy=None):
        if xy is not None:
            self.x, self.y = xy
        else:
            # If no latitude/longitude pair is given, use the capitol's
            if latlon is None:
                latlon = (Location.capital_lat, Location.capital_lon)

            # Calculate the x and y distance from the capital
            self.x = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     Location.capital_lat, latlon[1])
            self.y = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     latlon[0], Location.capital_lon)

            # Flip the sign of the x/y coordinates based on location
            if latlon[1] < Location.capital_lon:
                self.x *= -1

            if latlon[0] < Location.capital_lat:
                self.y *= -1

    def dist(self, other):
        """Calculate straight line distance between self and other"""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return "Location(xy=(%0.2f, %0.2f))" % (self.x, self.y)