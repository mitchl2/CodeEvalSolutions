'''
Verifies the correct behavior of the wifi_search module

Created on Oct 19, 2015

@author: Mitchell Lee
'''

import unittest

from wifi_search import (CityBuilding, is_hotspot_in_building,
                         is_line_segment_intersected)


class TestWifiSearch(unittest.TestCase):
    """Verifies the correct behavior of the wifi_search module.
    """

    def _validate_is_hotspot_in_building(self,
                                         cb,
                                         test_pts,
                                         is_inside_building):
        """Checks that is_hotspot_in_building returns the correct value for a
        series of test points.

        Args:
            cb: A building.
            test_pts: A sequence of points as pairs of numbers.
            is_inside_building: Boolean indicating whether or not the points
                are expected to be in the the building.
        """
        for pt in test_pts:
            self.assertEqual(is_hotspot_in_building(cb, pt),
                             is_inside_building,
                             "Expected to is_hotspot_in_building to return %s "
                             "for test point %s and building %s"
                             % (is_inside_building, str(pt), cb.name))

    def test_is_hotspot_in_building_simple_building(self):
        """Verifies that the is_hotspot_in_building function behaves correctly
        with a simple building outline (a rectangle).

                 _______________________
                |                       |
                |                       |
                |                       |
                |_______________________|
        """
        cb = CityBuilding("SimpleRectangle",
                          [(0.0, 0.0), (0.0, 12.83), (34.04, 12.83),
                           (34.04, 0.0), (0.0, 0.0)])

        inside_points = [(17.65, 4.43), (0.1, 0.1), (0.0, 0.0)]
        outside_points = [(36.21, 12.83), (0.0, 12.84), (37.54, 6.76)]

        self._validate_contains_point(cb, inside_points, True)
        self._validate_contains_point(cb, outside_points, False)

    def test_is_hotspot_in_building_diamond_building(self):
        """Verifies that the is_hotspot_in_building function behaves correctly
        with a building outline that forms a diamond shape.

                            /\
                          /    \
                        /        \
                      /            \
                    /                \
                    \                /
                      \            /
                        \        /
                          \    /
                            \/
        """
        cb = CityBuilding("Diamond",
                          [(10.0, 20.0), (20.0, 10.0), (10.0, 0.0),
                           (0.0, 10.0), (10.0, 20.0)])

        inside_points = [(10.0, 10.0), (10.0, 10.01), (10.0, 20.0)]
        outside_points = [(20.01, 10.0), (5.0, 5.0), (9.99, 19.99)]

        self._validate_contains_point(cb, inside_points, True)
        self._validate_contains_point(cb, outside_points, False)

    def test_is_hotspot_in_building_arrow_head_building(self):
        """Verifies that the is_hotspot_in_building function behaves correctly
        with a building outline that forms a L shape (or arrow head).

                 __________________
                |                  |
                |                  |
                |                  |
                |          ________|
                |        |
                |        |
                |        |
                |________|
        """
        cb = CityBuilding("ArrowHead",
                          [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0),
                           (20.0, 10.0), (20.0, 30.0), (0.0, 30.0),
                           (0.0, 0.0)])

        inside_points = [(5.0, 10.0), (15.0, 10.0), (8.0, 25.0)]
        outside_points = [(5.0, 9.99), (10.01, 3.65), (20.01, 10.0)]

        self._validate_contains_point(cb, inside_points, True)
        self._validate_contains_point(cb, outside_points, False)

    def test_is_line_segment_intersected_vertical_line(self):
        """Verifies that the _is_line_segment_intersected function behaves
        correctly for vertical lines.
        """
        # Special case for crossing number algorithm: Ray intersects a vertex
        # of the polygon. To resolve this special case, we only consider a
        # ray/vertex intersection to occur if the other vertex in the line
        # segment has the same vertical position or it's below the intersected
        # vertex. In the case below, we expect this to count as a line segment
        # intersection.
        #
        #         X---------->A
        #                     |
        #                     |
        #                     |
        #                     B
        a1 = (10.0, 10.0)
        b1 = (10.0, 5.0)
        x1 = (3.0, 10.0)
        self.assertTrue(
            is_line_segment_intersected(a1, b1, x1),
            "Expected is_line_segment_intersected to return True for "
            "the intersection with a vertex on a vertical line (where the"
            "non-intersected vertex lies below the intersected vertex)."
            "Line segment starts at %s and ends at %s, and the ray in the "
            "direction <1, 0> starts at %s" % (a1, b1, x1))

        # Opposite case as described above, here we do not expect this case
        # to count as an intersection.
        #
        #                     A
        #                     |
        #                     |
        #                     |
        #          X--------->B
        a2 = (10.0, 10.0)
        b2 = (10.0, 5.0)
        x2 = (3.0, 5.0)
        self.assertFalse(
            is_line_segment_intersected(a2, b2, x2),
            "Expected is_line_segment_intersected to return False for "
            "the intersection with a vertex on a vertical line (where the"
            "non-intersected vertex lies above the intersected vertex)."
            "Line segment starts at %s and ends at %s, and the ray in the "
            "direction <1, 0> starts at %s" % (a2, b2, x2))

        # Non-corner case for vertical line segment intersection.
        #
        #                     A
        #                     |
        #          X--------->|
        #                     |
        #                     B
        a2 = (10.0, 10.0)
        b2 = (10.0, 5.0)
        x2 = (3.0, 7.0)
        self.assertTrue(
            is_line_segment_intersected(a2, b2, x2),
            "Expected is_line_segment_intersected to return True. Line segment "
            "starts at %s and ends at %s, and the ray in the direction <1, 0> "
            "starts at %s" % (a2, b2, x2))

        # Non-corner case for non-vertical line segment intersection.
        #
        #          X--------->
        #
        #                     A
        #                     |
        #                     |
        #                     |
        #                     B
        a2 = (10.0, 10.0)
        b2 = (10.0, 5.0)
        x2 = (3.0, 12.0)
        self.assertFalse(
            is_line_segment_intersected(a2, b2, x2),
            "Expected is_line_segment_intersected to return False. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a2, b2, x2))

    def test_is_line_segment_intersected_horizontal_line(self):
        """Verifies that the _is_line_segment_intersected function behaves
        correctly for horizontal lines.
        """
        # Here we're intersecting two vertices of the line segment. This
        # counts as intersection because both vertices have the same vertical
        # position.
        #
        #          X--------->A------B
        #
        a1 = (10.0, 10.0)
        b1 = (20.0, 10.0)
        x1 = (5.0, 10.0)
        self.assertTrue(
            is_line_segment_intersected(a1, b1, x1),
            "Expected is_line_segment_intersected to return True. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a1, b1, x1))

        # Non-corner case for non-horizontal line segment intersection.
        #
        #          X--------->
        #
        #                     A-------B
        a2 = (10.0, 10.0)
        b2 = (20.0, 10.0)
        x2 = (3.0, 12.0)
        self.assertFalse(
            is_line_segment_intersected(a2, b2, x2),
            "Expected is_line_segment_intersected to return False. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a2, b2, x2))

    def test_is_line_segment_intersected_non_horizontal_or_vertical_line(self):
        """Verifies that the _is_line_segment_intersected function behaves
        correctly for non-horizontal and non-vertical lines.
        """
        pass