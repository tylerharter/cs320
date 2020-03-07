# Copyright 2020 Tyler Caraza-Harter
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv, time
from zipfile import ZipFile
from datetime import datetime
from collections import defaultdict
import pandas as pd
from math import sin, cos, asin, sqrt, pi

def haversine_miles(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(lambda a: a/180*pi, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(min(1, sqrt(a)))
    d = 3956 * c
    return d


class Location:
    # WI capital coords
    capital_lat = 43.074683
    capital_lon = -89.384261

    def __init__(self, latlon=None, xy=None):
        if xy != None:
            self.x, self.y = xy
        else:
            if latlon == None:
                latlon = (Location.capital_lat, Location.capital_lon)

            self.x = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     Location.capital_lat, latlon[1])
            if latlon[1] < Location.capital_lon:
                self.x *= -1
            self.y = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     latlon[0], Location.capital_lon)
            if latlon[0] < Location.capital_lat:
                self.y *= -1

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return "Location(xy=(%0.2f, %0.2f))" % (self.x, self.y)


class Stop:
    def __init__(self, stop_id, loc, wheelchair_boarding):
        self.stop_id = stop_id
        self.loc = loc
        self.wheelchair_boarding = wheelchair_boarding

    def __repr__(self):
        return "Stop({}, {}, {})".format(repr(self.stop_id), repr(self.loc),
                                         repr(self.wheelchair_boarding))


class Trip:
    def __init__(self, trip_id, route_id, bikes_allowed):
        self.trip_id = trip_id
        self.route_id = route_id
        self.bikes_allowed = bikes_allowed
        self.stop_times = []

    def __repr__(self):
        s = "Trip({}, {}, {})"
        return s.format(repr(self.trip_id), repr(self.route_id), repr(self.bikes_allowed))


class StopTree:
    splits = "xy"

    def other_attr(attr):
        return "y" if attr == "x" else "x"

    def __init__(self, stops, splits, split_attr="x"):
        split_idx = len(stops)//2 # note: values equal to the mid may go less or more

        if splits > 0 and split_idx < len(stops):
            # split
            stops = sorted(stops, key=lambda stop: getattr(stop.loc, split_attr))
            self.split_attr = split_attr
            self.split_val = getattr(stops[split_idx].loc, split_attr)
            self.less = StopTree(stops[:split_idx], splits-1, StopTree.other_attr(split_attr))
            self.more = StopTree(stops[split_idx:], splits-1, StopTree.other_attr(split_attr))
            self.stops = None
        else:
            self.stops = stops

    def collect(self, xlim, ylim, results):
        if self.stops:
            for s in self.stops:
                if xlim[0] <= s.loc.x <= xlim[1] and ylim[0] <= s.loc.y <= ylim[1]:
                    results.append(s)
        else:
            lim = xlim if self.split_attr == "x" else ylim
            if lim[0] <= self.split_val:
                self.less.collect(xlim, ylim, results)
            if lim[1] >= self.split_val:
                self.more.collect(xlim, ylim, results)

    def search(self, xlim, ylim):
        results = []
        self.collect(xlim, ylim, results)
        results.sort(key=lambda stop: stop.stop_id)
        return results

    def draw_tree(self, ax, xlim=None, ylim=None, lw=10):
        if self.stops != None:
            return

        if xlim == None:
            xlim = ax.get_ylim()

        if ylim == None:
            ylim = ax.get_ylim()

        if self.split_attr == "x":
            x = self.split_val
            y1, y2 = ylim
            self.less.draw_tree(ax, xlim=(xlim[0], x), ylim=ylim, lw=lw*0.66)
            self.more.draw_tree(ax, xlim=(x, xlim[1]), ylim=ylim, lw=lw*0.66)
            ax.plot((x, x), (y1, y2), 'y', lw=lw, zorder=-10)
        else:
            assert self.split_attr == "y"
            x1, x2 = xlim
            y = self.split_val
            self.less.draw_tree(ax, xlim=xlim, ylim=(ylim[0], y), lw=lw*0.66)
            self.more.draw_tree(ax, xlim=xlim, ylim=(y, ylim[1]), lw=lw*0.66)
            ax.plot((x1, x2), (y, y), 'y', lw=lw, zorder=-10)


class BusDay:
    def init_from_files(self, zf, date):
        # PARSE schedule
        with zf.open("calendar.txt") as f:
            cal = pd.read_csv(f)

        datenum = int(date.strftime("%Y%m%d"))
        dayname = date.strftime("%A").lower()

        cal = cal[(cal["start_date"] <= datenum) & (cal["end_date"] >= datenum)]
        cal = cal[cal[dayname] == 1]
        service_ids = sorted(set(cal["service_id"]))

        # PARSE trips
        with zf.open("trips.txt") as f:
            trips_df = pd.read_csv(f)
        trips_df = trips_df[trips_df["service_id"].isin(service_ids)]

        trips = []
        trip_ids = set()
        for _, row in trips_df.iterrows():
            t = Trip(row["trip_id"], row["route_short_name"], bool(row["bikes_allowed"]))
            trips.append(t)
            trip_ids.add(t.trip_id)
        trips.sort(key=lambda t: t.trip_id)

        # index trips by route
        routes = defaultdict(list)
        for t in trips:
            routes[t.route_id].append(t)

        # PARSE stops
        with zf.open("stops.txt") as f:
            stops_df = pd.read_csv(f)
        stops = {}
        for _, row in stops_df.iterrows():
            s = Stop(row["stop_id"],
                     Location(latlon=(row["stop_lat"], row["stop_lon"])),
                     bool(row["wheelchair_boarding"]))
            stops[s.stop_id] = s

        # which stops are visited this day?
        stops_visited = set()
        with zf.open("stop_times.txt") as f:
            stop_times_df = pd.read_csv(f)
            stop_times_df = stop_times_df[stop_times_df["trip_id"].isin(trip_ids)]
            stop_ids = stop_times_df["stop_id"].unique()
            stops = [s for s in stops.values() if s.stop_id in stop_ids]
        stops.sort(key=lambda s: s.stop_id)

        # INIT attributes
        self.service_ids = service_ids
        self.trips = trips
        self.routes = routes
        self.stops = stops
        self.tree = StopTree(self.stops, 6)

    def __init__(self, date):
        with ZipFile("mmt_gtfs.zip") as zf:
            self.init_from_files(zf, date)

    def get_trips(self, route=None):
        if route != None:
            return self.routes[route]
        return self.trips

    def get_stops(self):
        return self.stops

    def scatter_stops(self, ax):
        df = pd.DataFrame({
            "x": [stop.loc.x for stop in self.stops],
            "y": [stop.loc.y for stop in self.stops],
            "w": [stop.wheelchair_boarding for stop in self.stops],
        })
        df[df["w"]].plot.scatter(x="x", y="y", ax=ax, marker="o", s=3, color="red")
        df[~df["w"]].plot.scatter(x="x", y="y", ax=ax, marker="o", s=3, color="0.7")
        ax.set_xlabel("")
        ax.set_ylabel("")

    def draw_tree(self, ax):
        self.tree.draw_tree(ax)

    def get_stops_rect(self, xlim, ylim):
        return self.tree.search(xlim, ylim)

    def get_stops_circ(self, xy, radius):
        stops = self.get_stops_rect(xlim=(xy[0]-radius, xy[0]+radius),
                                    ylim=(xy[1]-radius, xy[1]+radius))
        center = Location(xy=xy)
        return [s for s in stops if center.dist(s.loc) <= radius]
