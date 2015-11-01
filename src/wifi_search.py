'''
Functions that determine which buildings have Wi-Fi hotspots.

The corresponding CodeEval challenge for this module is called "Where is Wi-Fi"
(https://www.codeeval.com/open_challenges/159/).

Created on Oct 19, 2015

@author: Mitchell Lee
'''


class CityBuilding(object):
    """A building from a city map. Contains functions for checking if an xy
    map location lies within the boundaries of the building.
    """

    def __init__(self, name, pts):
        """Constructs a new CityBuilding.

        Args:
            name: Name of the building.
            pts: A sequence of 2D points, as pairs of numbers, that form
            polygon vertices of the building outline.
        """
        pass


def is_line_segment_intersected(self, pt1, pt2, pt3):
    """Checks if the line segment formed from pt1 to pt2 is intersected
    by the line starts at pt3 and extends indefinitely in the direction
    <1, 0>.

    Args:
        pt1: A 2D point as a pair of numbers.
        pt2: A 2D point as a pair of numbers.
        pt3: A 2D point as a pair of numbers.

    Returns:
        True if the line segment is intersected, else False.
    """
    pass


def is_hotspot_in_building(cb, pt):
    """Checks if the hotspot is located within the building.

    Args:
        cb: A CityBuilding.
        pt: A hotspot location.

    Returns:
        True if the hotspot location resides within the building.
    """
    pass


def azimuth_to_vector(azi_deg):
    """Converts an azimuth to a vector.

    Args:
        azi_deg: A direction in terms of an angles in degrees, where 0 degrees
            corresponds to the positive y-axis direction.

    Returns:
        A 2D direction vector as a pair of numbers.
    """
    pass


def hotspot_radar_locations(radar_data):
    """Determines all Wi-Fi radar points for each MAC address detected by Wi-Fi
    radar.

    Args:
        radar_data: A sequence of tuples. The first object in each tuple
            contains a radar point, which is a 2D point where the Wi-Fi radar
            was currently at when a hotspot(s) was detected. The second object
            in each tuple is a sequence of pairs containing a MAC address as a
            string and azimuth as a number.

    Returns:
        A dictionary where each key is a MAC address and each value is a
        sequence of pairs containing a 2D radar point and a direction vector to
        a hotspot as a pair of numbers.
    """
    pass


def hotspot_location(pt1, dxdy1, pt2, dxdy2):
    """Computes the intersection of two radar lines. Each line consists of
    a point where the Wi-Fi radar was at when a hotspot was detected and
    the direction it was detected in. If an intersection exists between the
    two radar lines then it indicates the presence of a hotspot, otherwise
    if there is no intersection then the hotspot location cannot be
    determined.

    Args:
        pt1: A 2D radar point as a pair of numbers.
        dxdy1: Direction vector to hotspot as a pair of numbers.
        pt2: A 2D radar point as a pair of numbers.
        dxdy2: Direction vector to hotspot as a pair of numbers.

    Returns:
        Hotspot location if two radar lines intersect, else None if the
        lines do not intersect and a hotspot location cannot be determined.
    """
    pass



