'''
Verifies the correct behavior of the wifi_search module

Created on Oct 19, 2015

@author: Mitchell Lee
'''

import unittest

from wifi_search import (CityBuilding, is_hotspot_in_building,
                         is_line_segment_intersected, azimuth_to_vector,
                         hotspot_location, hotspot_radar_locations)


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

        self._validate_is_hotspot_in_building(cb, inside_points, True)
        self._validate_is_hotspot_in_building(cb, outside_points, False)

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

        self._validate_is_hotspot_in_building(cb, inside_points, True)
        self._validate_is_hotspot_in_building(cb, outside_points, False)

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

        self._validate_is_hotspot_in_building(cb, inside_points, True)
        self._validate_is_hotspot_in_building(cb, outside_points, False)

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

        # Non-special case for vertical line segment intersection.
        #
        #                     A
        #                     |
        #          X--------->|
        #                     |
        #                     B
        a3 = (10.0, 10.0)
        b3 = (10.0, 5.0)
        x3 = (3.0, 7.0)
        self.assertTrue(
            is_line_segment_intersected(a3, b3, x3),
            "Expected is_line_segment_intersected to return True. Line segment "
            "starts at %s and ends at %s, and the ray in the direction <1, 0> "
            "starts at %s" % (a3, b3, x3))

        # Non-special case for vertical line segment non-intersection.
        #
        #          X--------->
        #
        #                     A
        #                     |
        #                     |
        #                     |
        #                     B
        a4 = (10.0, 10.0)
        b4 = (10.0, 5.0)
        x4 = (3.0, 12.0)
        self.assertFalse(
            is_line_segment_intersected(a4, b4, x4),
            "Expected is_line_segment_intersected to return False. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a4, b4, x4))

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

        # Non-special case for horizontal line segment non-intersection.
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
        # Special case: Vertex is intersected, this is expected to count
        # as an intersection because the non-intersected vertex is below
        # the intersected vertex.
        #
        #       X---------> A
        #                    \
        #                     \
        #                      \
        #                       B
        a1 = (10.0, 10.0)
        b1 = (20.0, 2.0)
        x1 = (5.0, 10.0)
        self.assertTrue(
            is_line_segment_intersected(a1, b1, x1),
            "Expected is_line_segment_intersected to return True. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a1, b1, x1))

        # Non-special case for non-horizontal/vertical line segment intersection.
        #
        #                   A
        #                    \
        #          X--------->\
        #                      \
        #                       B
        a2 = (10.0, 10.0)
        b2 = (20.0, 2.0)
        x2 = (5.0, 5.0)
        self.assertTrue(
            is_line_segment_intersected(a2, b2, x2),
            "Expected is_line_segment_intersected to return True. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a2, b2, x2))

        # Special case for non-horizontal/vertical line segment intersection.
        #
        #                   A
        #                    \
        #          X--------->\
        #                      \
        #                       B
        a2 = (10.0, 10.0)
        b2 = (20.0, 2.0)
        x2 = (5.0, 5.0)
        self.assertTrue(
            is_line_segment_intersected(a2, b2, x2),
            "Expected is_line_segment_intersected to return True. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a2, b2, x2))

        # Special case for non-horizontal/vertical line segment intersection
        # (ray/vertex intersection).
        #
        #                   A
        #                    \
        #                     \
        #                      \
        #            X--------->B
        a3 = (10.0, 10.0)
        b3 = (20.0, 2.0)
        x3 = (5.0, 2.0)
        self.assertFalse(
            is_line_segment_intersected(a3, b3, x3),
            "Expected is_line_segment_intersected to return False. Line  "
            "segment starts at %s and ends at %s, and the ray in the direction "
            "<1, 0> starts at %s" % (a3, b3, x3))

    def _validate_azimuth_to_vector(self,
                                    azi_deg,
                                    expected_dxdy):
        """Checks that azimuth_to_vector returns the expected values.

        Args:
            azi_deg: Azimuth angle in degrees.
            expected_dxdy: Expected vector returned by azimuth_to_vector.
        """
        actual_dxdy = azimuth_to_vector(azi_deg)
        self.assertAlmostEqual(actual_dxdy[0],
                               expected_dxdy[0],
                               7,
                               "Expected azimuth_to_vector to return dx value "
                               "of %.3f, but returned dx value of %.3f instead"
                               % (expected_dxdy[0], actual_dxdy[0]))

        self.assertAlmostEqual(actual_dxdy[1],
                               expected_dxdy[1],
                               7,
                               "Expected azimuth_to_vector to return dy value "
                               "of %.3f, but returned dy value of %.3f instead"
                               % (expected_dxdy[1], actual_dxdy[1]))

    def test_azimuth_to_vector(self):
        """Verifies that the azimuth_to_vector function behaves correctly.
        """
        self._validate_azimuth_to_vector(0, [0, 1])
        self._validate_azimuth_to_vector(90, [1, 0])
        self._validate_azimuth_to_vector(180, [0, -1])
        self._validate_azimuth_to_vector(270, [-1, 0])

    def test_hotspot_location_radar_lines_with_same_direction(self):
        """Verifies that the hotspot_location function behaves correctly
        for radar lines that have the same direction.
        """
        # These lines should not intersect because they point in the same
        # direction.
        #                          ^
        #                        /
        #                      /
        #                    /
        #                   B
        #
        #                ^
        #              /
        #            /
        #          /
        #         A
        pt1 = (10.0, 10.0)
        pt2 = (20.0, 20.0)
        dxdy = (0.7071, 0.7071)
        actual_hotspot_location = hotspot_location(pt1, dxdy, pt2, dxdy)
        expected_hotspot_location = None
        self.assertEqual(actual_hotspot_location, expected_hotspot_location,
                         "Expected hotspot_location to return %s, but "
                         "returned %s instead. pt1 is %s and pt2 is %s, "
                         "both radar lines have the direction vector %s"
                         % (None,
                            actual_hotspot_location,
                            str(pt1),
                            str(pt2),
                            str(dxdy)))

    def test_hotspot_location_intersecting_radar_lines(self):
        """Verifies that the hotspot_location function behaves correctly
        for intersecting radar lines.
        """
        #               ^
        #             / |
        #           /   |
        #         /     |
        #        A      B
        pt1 = (10.0, 10.0)
        dxdy1 = (0.7071, 0.7071)
        pt2 = (20.0, 10.0)
        dxdy2 = (0, 1)
        actual_hotspot_location = hotspot_location(pt1, dxdy1, pt2, dxdy2)
        expected_hotspot_location = (20.0, 20.0)

        self.assertAlmostEqual(expected_hotspot_location[0],
                               actual_hotspot_location[0],
                               msg="Expected hotspot location x-value (%.3f) "
                               "differs from actual hotspot location x-value (%.3f)"
                               % (expected_hotspot_location[0],
                                  actual_hotspot_location[0]),
                               delta=2e-3)

        self.assertAlmostEqual(expected_hotspot_location[1],
                               actual_hotspot_location[1],
                               msg="Expected hotspot location y-value (%.3f) "
                               "differs from actual hotspot location y-value (%.3f)"
                               % (expected_hotspot_location[1],
                                  actual_hotspot_location[1]),
                               delta=2e-3)

    def test_hotspot_radar_locations(self):
        """Verifies that the hotspot_radar_locations function behaves
        correctly.
        """
        radar_data = [((5, 3), [("56-4c-18-eb-13-8b", 0),
                                ("88-fe-14-a4-aa-2a", 45)]),
                      ((2, 3), [("56-4c-18-eb-13-8b", 45),
                                ("88-fe-14-a4-aa-2a", 60)])]

        expected_radar_locations = {
            "56-4c-18-eb-13-8b": [((5, 3), (0, 1)),
                                  ((2, 3), (0.7071, 0.7071))],
            "88-fe-14-a4-aa-2a": [((5, 3), (0.7071, 0.7071)),
                                  ((2, 3), (0.866, 0.499))]}

        actual_radar_locations = hotspot_radar_locations(radar_data)

        for (exp_mac,
             expected_detected_hotspots) in expected_radar_locations.iteritems():
            self.assertTrue(exp_mac in actual_radar_locations,
                            "'%s' MAC address missing from radar locations "
                            "returned by hotspot_radar_locations (%s)"
                            % (exp_mac, str(actual_radar_locations)))

            actual_detected_hotspots = actual_radar_locations[exp_mac]

            self.assertEqual(len(expected_detected_hotspots),
                             len(actual_detected_hotspots),
                             "Expected number of detected hotspots (%d) for "
                             "the MAC address %s doesn't match the actual "
                             "number of MAC addresses (%d)"
                             % (len(expected_detected_hotspots),
                                exp_mac,
                                len(actual_detected_hotspots)))

            for ((exp_pt, exp_azi_vec),
                 (act_pt, act_azi_vec)) in zip(expected_detected_hotspots,
                                               actual_detected_hotspots):
                self.assertAlmostEqual(
                   exp_pt[0], act_pt[0], 7,
                   "Expected radar point x-value (%.3f) differs from actual "
                   "radar point x-value (%.3f) for MAC address %s"
                   % (exp_pt[0], act_pt[0], exp_mac))

                self.assertAlmostEqual(
                   exp_pt[1], act_pt[1], 7,
                   "Expected radar point y-value (%.3f) differs from actual "
                   "radar point y-value (%.3f) for MAC address %s"
                   % (exp_pt[1], act_pt[1], exp_mac))

                self.assertAlmostEqual(exp_azi_vec[0], act_azi_vec[0],
                                       msg="Expected azimuth dx (%.3f) differs "
                                       "from actual azimuth dx (%.3f) for "
                                       "MAC address %s"
                                       % (exp_azi_vec[0],
                                          act_azi_vec[0],
                                          exp_mac),
                                       delta=2e-3)

                self.assertAlmostEqual(exp_azi_vec[1], act_azi_vec[1],
                                       msg="Expected azimuth dx (%.3f) differs "
                                       "from actual azimuth dx (%.3f) for "
                                       "MAC address %s"
                                       % (exp_azi_vec[1],
                                          act_azi_vec[1],
                                          exp_mac),
                                       delta=2e-3)