# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.open

from math import sin, cos, asin, sqrt, pi

from zipfile import ZipFile
from collections import defaultdict
from functools import partial
import pandas as pd


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
    c = 2 * asin(min(1.0, sqrt(a)))
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
        # Note: These are f-strings, they make formatting way easier and they are faster!
        return f"Location(xy=({self.x:0.2f}, {self.y:0.2f}))"


class Stop:
    def __init__(self, stop_id, loc, wheelchair_boarding):
        self.stop_id = stop_id
        self.loc = loc
        self.wheelchair_boarding = bool(wheelchair_boarding)

    def __repr__(self):
        return f"Stop({self.stop_id}, {self.loc}, {self.wheelchair_boarding})"


class Trip:
    def __init__(self, trip_id, route_id, bikes_allowed):
        self.trip_id = trip_id
        self.route_id = route_id
        self.bikes_allowed = bool(bikes_allowed)
        self.stop_times = []

    def __repr__(self):
        return f"Trip({self.trip_id}, {self.route_id}, {self.bikes_allowed})"


class Node:
    """Simple data container class for the tree"""
    def __init__(self, left=None, right=None, is_leaf=True, split_x=True, data=None):
        self.left, self.right, self.is_leaf = left, right, is_leaf
        self.split_x, self.data = split_x, data


class KDTree:
    """Searching for neighbors or points in a given region is commonly
    done through a data structure called a KDTree (K-Dimensional Tree)
    because it makes the search very efficient.

    In this lab, the binary tree you've implemented technically is a
    two dimensional KDTree!
    """
    def __init__(self, stops, max_depth=6):
        self.max_depth = max_depth
        self.root = Node(left=None, right=None, is_leaf=True, split_x=True, data=None)
        self.build(stops)

    @staticmethod
    def is_in_bounds(stop, xlim, ylim):
        """This is a simple helper method that does not depend on
        any instance attributes, so self is not passed in. However,
        since it is something that is related to the class it makes
        sense that it should be within it. Adding the @staticmethod
        decorator allows for this. These are advanced concepts that
        aren't required but are very commonly used."""
        x_min, x_max = xlim
        y_min, y_max = ylim
        in_range_x = (x_min <= stop.loc.x <= x_max)
        in_range_y = (y_min <= stop.loc.y <= y_max)
        return in_range_x and in_range_y

    def build(self, stops):
        """It is common to have 'external' facing functions such as this
        one, that are simple wrappers around the actual recursive function
        call. This is useful as it allows me to pass in defaults without
        exposing them to the user."""
        self._build_helper(stops, head=self.root, split_x=True, depth=1)

    def _build_helper(self, stops, head, split_x, depth):
        """The main tree building method. Note that this is very similar to the
        pseudo code we have released except this is done in a separate class

        :param stops: List of stops objects to split up
        :param head: Current head of the subtree we are 'looking' at
            this starts off as the root of the tree and then it becomes
            its two children in the recursive call and so forth all the way down.
        :param split_x: Boolean that keeps track of whether or not we split on x.
            Note: This could have been done in a number of ways including by
            finding the remainder of the depth divided by two (mod 2 or %2)
            but I chose to be more explicit.
        :param depth: Current depth of the tree, goes from 1 to 6, helps determine
            when to stop the recursion (base case).
        """
        if depth <= self.max_depth and stops:
            # Sort data based on x or y, find median
            split_idx = len(stops) // 2
            stops = sorted(stops, key=lambda stop: stop.loc.x if split_x else stop.loc.y)

            # Populate fields of current head node (which is not a leaf since we are splitting)
            head.is_leaf, head.split_x = False, split_x
            head.left = Node(left=None, right=None, is_leaf=True, split_x=not split_x, data=None)
            head.right = Node(left=None, right=None, is_leaf=True, split_x=not split_x, data=None)
            head.data = stops[split_idx].loc.x if split_x else stops[split_idx].loc.y

            # Recurse on left and right child nodes
            self._build_helper(stops[split_idx:], head.left, not split_x, depth + 1)
            self._build_helper(stops[:split_idx], head.right, not split_x, depth + 1)
        else:
            # If we do not split, we are at a child node.
            # We just need to populate it's fields
            head.is_leaf, head.split_x = True, None
            head.data = stops

    def search(self, xlim, ylim):
        """Same as above, this is just a wrapper"""
        return self._search_helper(self.root, xlim, ylim)

    def _search_helper(self, head, xlim, ylim):
        """The main recursive search function"""
        if head.is_leaf:
            # Return only the stops that are within the bounds.

            # "partial" is just a handy shortcut, it allows us to
            # define a function based on another with some default
            # arguments set. In this case it is handy because the
            # "filter" built-in calls a function on every element
            # of the list (head.data) to determine whether or not
            # to keep it. This function is expected to return a
            # bool and only accept a single argument: the element.
            check_bounds = partial(self.is_in_bounds, xlim=xlim, ylim=ylim)
            results = list(filter(check_bounds, head.data))
        else:
            # Otherwise recurse on all sides for which the
            # rectangle overlaps. We then accumulate these
            # results together into a bigger list.
            results = []
            xy_min, xy_max = xlim if head.split_x else ylim
            if head.data >= xy_min:
                results += self._search_helper(head.right, xlim, ylim)
            if head.data <= xy_max:
                results += self._search_helper(head.left, xlim, ylim)
        return sorted(results, key=lambda stop: stop.stop_id)

    def draw_tree(self, ax, xlim=None, ylim=None, lw=10):
        """The draw tree entrypoint, again just a wrapper that sets
        defaults, in this case those are the x/ylims and root."""
        xlim = ax.get_xlim() if xlim is None else xlim
        ylim = ax.get_ylim() if ylim is None else ylim
        self._draw_tree_helper(self.root, ax, xlim, ylim, lw)

    def _draw_tree_helper(self, head, ax, xlim, ylim, lw):
        """Main tree drawing method.

        :param head: Current head of the tree as we recurse down.
        :param ax: The axis on which to plot the lines.
        :param xlim: The x limits of that axis (helps determine the length of the line)
        :param xlim: The y limits of that axis (helps determine the length of the line)
        :param lw: The line width to plot.
        """
        if not head.is_leaf:
            x_min, x_max = xlim
            y_min, y_max = ylim

            if head.split_x:
                x = head.data
                self._draw_tree_helper(head.right, ax, xlim=(x_min, x), ylim=ylim, lw=lw * 2/3)
                self._draw_tree_helper(head.left, ax, xlim=(x, x_max), ylim=ylim, lw=lw * 2/3)
                ax.plot((x, x), ylim, 'y', lw=lw, zorder=-10)
            else:
                y = head.data
                self._draw_tree_helper(head.right, ax, xlim=xlim, ylim=(y_min, y), lw=lw * 2/3)
                self._draw_tree_helper(head.left, ax, xlim=xlim, ylim=(y, y_max), lw=lw * 2/3)
                ax.plot(xlim, (y, y), 'y', lw=lw, zorder=-10)


class BusDay:
    def __init__(self, date, date_format="%Y%m%d"):
        """Build the BusDay object while pre-computing everything so that
        subsequent calls to get_trips/get_stops/etc... are faster."""
        with ZipFile("mmt_gtfs.zip") as zf:
            self.service_ids = self.get_all_service_ids(zf, date, date_format=date_format)
            self.all_trips, self.trip_ids = self.get_all_trips(zf)
            self.stops = self.get_all_stops(zf)
        self.routes = self.get_trips_per_route()
        self.tree = KDTree(self.stops, 6)

    @staticmethod
    def get_all_service_ids(zf, date, date_format="%Y%m%d"):
        """The most correct implementation of this function as it uses
        a vectorized approach (no slow for-loops) to convert columns
        into datetime objects."""
        # Open calendar.txt and create dataframe
        with zf.open("calendar.txt") as f:
            cal = pd.read_csv(f)

        # Convert columns to datetime objects, find out weekday of date
        day_name = date.strftime("%A").lower()
        cal["start_date"] = pd.to_datetime(cal["start_date"], format=date_format)
        cal["end_date"] = pd.to_datetime(cal["end_date"], format=date_format)

        # Filter based on range and day of week, get service ids
        cal = cal[(cal["start_date"] <= date) & (cal["end_date"] >= date)]
        cal = cal[cal[day_name] == 1]
        return sorted(set(cal["service_id"]))

    @staticmethod
    def get_all_service_ids_(zf, date, **kwargs):
        """An alternative to the previous method that is slightly faster as it does
        not use datetime at all. This works here but in general will not.

        Speed tests between the two methods:
            get_service_ids_:
            2.92 ms ± 42.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

            get_service_ids:
            4.39 ms ± 112 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

        Given this (only slight) speed-up, we recommend you use the more general method."""
        # Open calendar.txt and create dataframe
        with zf.open("calendar.txt") as f:
            cal = pd.read_csv(f)

        # We interpret each date as an integer. Since the format of the
        # date is year, month, day this comparison will work.
        # Note that this is done for efficiency purposes as it is a vectorized
        # operation (i.e: applies to the whole dataframe at once). A more correct
        # approach is shown above.
        date_num = int(date.strftime("%Y%m%d"))
        day_name = date.strftime("%A").lower()

        # Filter based on range and day of week, get service ids
        cal = cal[(cal["start_date"] <= date_num) & (cal["end_date"] >= date_num)]
        cal = cal[cal[day_name] == 1]
        return sorted(set(cal["service_id"]))

    def get_all_trips(self, zf):
        """Now that we have all the service ids, we can find all the trips.
        Note that we do this before ever calling get_trips, this is because
        this data will always be the same (it only depends on date) so we
        can compute it only once"""
        # Open trips.txt and create dataframe
        with zf.open("trips.txt") as f:
            trips_df = pd.read_csv(f)

        # Filter out trips that do not are not on this day
        trip_idxs = trips_df["service_id"].isin(self.service_ids)
        trips_df = trips_df[trip_idxs]

        # Now that we have a dataframe, we can create a list of Trip objects
        columns = ["trip_id", "route_short_name", "bikes_allowed"]
        columns = [trips_df[col] for col in columns]
        trips = [Trip(*data) for data in zip(*columns)]
        trip_ids = set(trips_df["trip_id"])
        trips.sort(key=lambda t: t.trip_id)
        return trips, trip_ids

    def get_trips_per_route(self):
        """Bucketize all trips by their route, this way get_trips will
        be very fast because we have precomputed this."""
        routes = defaultdict(list)
        for t in self.all_trips:
            routes[t.route_id].append(t)
        return routes

    def get_all_stops(self, zf):
        """Now that we have all the trips, we can get all the stops.
        Note that we call this method in init because the stops only
        depend on the date and so can be precomputed"""
        # Open stops.txt, stop_time.txt and create dataframes
        with zf.open("stops.txt") as f:
            stops_df = pd.read_csv(f)

        with zf.open("stop_times.txt") as f:
            stop_times_df = pd.read_csv(f)

        # Convert dataframe to a list of Stop objects
        columns = ["stop_id", "stop_lat", "stop_lon", "wheelchair_boarding"]
        columns = [stops_df[col] for col in columns]
        stops = [Stop(stop_id, Location(latlon=latlon), access)
                 for stop_id, *latlon, access in zip(*columns)]

        # Filter stops based on time
        stops_in_trips_idx = stop_times_df["trip_id"].isin(self.trip_ids)
        stop_times_df = stop_times_df[stops_in_trips_idx]
        stop_ids = stop_times_df["stop_id"].unique()
        stops = [s for s in stops if s.stop_id in stop_ids]
        stops.sort(key=lambda s: s.stop_id)
        return stops

    def get_trips(self, route=None):
        """We precomputed everything so we can just return
        the requested data immediately"""
        if route is not None:
            return self.routes[route]
        return self.all_trips

    def get_stops(self):
        """We precomputed everything so we can just return
        the requested data immediately"""
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
        """In order to find stops in circle efficiently we first find all
        the stops in the rectangle that encompasses the circle, then we filter."""
        x, y = xy
        center = Location(xy=xy)
        stops = self.get_stops_rect(xlim=(x-radius, x+radius), ylim=(y-radius, y+radius))
        return [s for s in stops if center.dist(s.loc) <= radius]
