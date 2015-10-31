'''
Verifies the correct behavior of the wifi_search module

Created on Oct 19, 2015

@author: Mitchell Lee
'''

import unittest

from wifi_search import CityBuilding


class TestCityBuilding(unittest.TestCase):
    """Verifies the correct behavior of the CityBuilding class. Contains
    general specification tests of the class as well as implementation
    tests (the crossing number algorithm is used to implement the
    contains_point function).
    """

    def _validate_contains_point(self, cb, test_pts, is_inside_building):
        """Checks that contains_point returns the correct value for a series
        of test points.

        Args:
            cb: A building.
            test_pts: A sequence of points as pairs of numbers.
            is_inside_building: Boolean indicating whether or not the points
                are expected to be in the the building.
        """
        for pt in test_pts:
            self.assertEqual(cb.contains_point(pt),
                             is_inside_building,
                             "Expected to contains_point to return %s for "
                             "test point %s and building %s"
                             % (str(pt), is_inside_building, cb.name))

    def test_contains_point_simple_building(self):
        """Verifies that the contains_point function behaves correctly
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

    def test_contains_point_diamond_building(self):
        """Verifies that the contains_point function behaves correctly
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

    def test_contains_point_arrow_head_building(self):
        """Verifies that the contains_point function behaves correctly
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