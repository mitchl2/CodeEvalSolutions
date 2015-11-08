'''
Functions that determine which buildings have Wi-Fi hotspots.

The corresponding CodeEval challenge for this module is called "Where is Wi-Fi"
(https://www.codeeval.com/open_challenges/159/).

Created on Oct 19, 2015

@author: Mitchell Lee
'''

from itertools import izip

from math import cos, sin, radians, pi

# Tolerance for comparing floating point numbers.
POINT_CMP_TOL = 1e-5


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
        self.name = name
        self.pts = pts
        self.has_confirmed_wifi = False


def is_line_segment_intersected(pt1, pt2, pt3):
    """Checks if the line segment formed from pt1 to pt2 is intersected
    by the ray starting at pt3 and extends indefinitely in the direction
    <1, 0>.

    Args:
        pt1: A 2D point as a pair of numbers. Starting point of the line
            segment.
        pt2: A 2D point as a pair of numbers. End point of the line segment.
        pt3: A 2D point as a pair of numbers. Starting point of the ray.

    Returns:
        True if the line segment is intersected, else False.
    """
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3

    if abs(y1 - y2) < POINT_CMP_TOL:
        # Horizontal line segment, no intersection.
        return False
    else:
        # Treat the line segment as parameterized line with respect to t.
        # Compute t for which the ray from pt3 in the direction <1, 0>
        # intersects the line.
        t = (y3 - y1) / (-y1 + y2)
        x_t = ((1 - t) * x1) + (t * x2)

        if x_t < x3:
            # Intersection occurs to the left of the point being tested
            # for ray intersection.
            return False
        elif abs(t) < POINT_CMP_TOL or abs(1 - t) < POINT_CMP_TOL:
            # A line segment vertex is intersected, check here that the
            # intersected vertex is vertically at or below the other vertex.
            y_t = ((1 - t) * y1) + (t * y2)

            y_other_vertex = y2 if t < 0.5 else y1
            return (y_other_vertex < y_t
                    or abs(y_t - y_other_vertex) < POINT_CMP_TOL)
        else:
            # Check that the ray-line segment intersection occured within
            # the parameterized line between pt1 and pt2.
            return t > 0.0 and t < 1.0


def is_hotspot_in_building(cb, pt):
    """Checks if the hotspot is located within the building.

    Args:
        cb: A CityBuilding.
        pt: A hotspot location.

    Returns:
        True if the hotspot location resides within the building, else False.
    """
    # Crossing number algorithm is used to determine if the point is within
    # the polygon defined by the building points. We check how many sides
    # of the polygon are intersected by a ray that starts at pt and has the
    # direction <1, 0>. If the number of crossings is odd, then the point
    # is within the polygon, else it is not.
    line_segment_crossings = []
    for pt_a, pt_b in izip(cb.pts[:-1], cb.pts[1:]):
        line_segment_crossings.append(
            is_line_segment_intersected(pt_a, pt_b, pt))

    return len([x for x in line_segment_crossings if x]) % 2 == 1


def azimuth_to_vector(azi_deg):
    """Converts an azimuth to a vector.

    Args:
        azi_deg: A direction in terms of an angles in degrees, where 0 degrees
            corresponds to the positive y-axis direction.

    Returns:
        A normalized 2D direction vector as a pair of numbers.
    """
    return (-cos(radians(azi_deg) + pi / 2.0), sin(radians(azi_deg) + pi / 2.0))


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
    radar_locations = {}

    for pt, detected_hotspots in radar_data:
        for mac, azi_deg in detected_hotspots:
            if mac not in radar_locations:
                radar_locations[mac] = []

            radar_locations[mac].append((pt, azimuth_to_vector(azi_deg)))

    return radar_locations


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
    # Check if the radar lines point in the same direction (no intersection).
    dx1, dy1 = dxdy1
    dx2, dy2 = dxdy2

    if abs(dx1 - dx2) < POINT_CMP_TOL and abs(dy1 - dy2) < POINT_CMP_TOL:
        # Can't compute intersection, lines are practically identical.
        return None
    else:
        # Compute intersection point of the lines.
        x1, y1 = pt1
        x2, y2 = pt2

        if abs(dx1) < POINT_CMP_TOL:
            # First radar line is vertical.
            m2 = dy2 / dx2
            b2 = y2 - (m2 * x2)
            y_inter = m2 * x1 + b2
            return (x1, y_inter)
        elif abs(dx2) < POINT_CMP_TOL:
            # Second radar line is vertical.
            m1 = dy1 / dx1
            b1 = y1 - (m1 * x1)
            y_inter = m1 * x2 + b1
            return (x2, y_inter)
        else:
            # Both lines are non-vertical.
            m1 = dy1 / dx1
            b1 = y1 - (m1 * x1)

            m2 = dy2 / dx2
            b2 = y2 - (m2 * x2)

            x_inter = (b2 - b1) / (m1 - m2)
            y_inter = m1 * x_inter + b1
            return x_inter, y_inter