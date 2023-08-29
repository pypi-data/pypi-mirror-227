"""Test functions in vec2_math module.

:author: Shay Hill
:created: 2023-08-19
"""
import math

from vec2_math import (
    move_toward,
    move_along,
    vrotate,
    get_signed_angle,
    qrotate,
    get_line_xsect,
    get_seg_xsect,
    _get_ray_xsect_times,  # type: ignore
    vmul,
    vdiv,
    get_norm,
    set_norm,
    _seg_to_ray,
    rotate_around,
    get_closest_point_on_line, get_closest_point_on_seg
)
import pytest


def _isclose_vec(
    vec_a: tuple[float, float],
    vec_b: tuple[float, float],
    rel_tol: float = 1e-09,
    abs_tol: float = 0.0,
):
    """Compare two vectors for equality.

    :param vec_a: first vector
    :param vec_b: second vector
    :param rel_tol: relative tolerance
    :param abs_tol: absolute tolerance
    :return: True if vectors are equal
    """
    if len(vec_a) != len(vec_b):
        return False
    return all(
        math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
        for a, b in zip(vec_a, vec_b)
    )


class TestGetSignedAngle:
    def test_quadrant_1(self):
        v1 = (1, 0)
        v2 = (0, 1)
        assert get_signed_angle(v1, v2) == math.pi / 2

    def test_quadrant_12(self):
        v1 = (1, 1)
        v2 = (-1, 1)
        assert get_signed_angle(v1, v2) == math.pi / 2

    def test_x_axis(self):
        v1 = (1, 0)
        v2 = (-1, 0)
        assert get_signed_angle(v1, v2) == math.pi

    def test_y_axis(self):
        v1 = (0, 1)
        v2 = (0, -1)
        assert get_signed_angle(v1, v2) == math.pi

    def test_equal(self):
        v1 = (0, 1)
        v2 = (0, 1)
        assert get_signed_angle(v1, v2) == 0

    def test_parallel(self):
        v1 = (0, 1)
        v2 = (0, 2)
        assert get_signed_angle(v1, v2) == 0

    def test_quadrant_4(self):
        v1 = (1, 0)
        v2 = (0, -1)
        assert get_signed_angle(v1, v2) == -math.pi / 2

    def test_one_zero_vector(self):
        v1 = (1, 0)
        v2 = (0, 0)
        assert get_signed_angle(v1, v2) == 0

    def test_two_zero_vectors(self):
        v1 = (0, 0)
        v2 = (0, 0)
        assert get_signed_angle(v1, v2) == 0


class TestGetNorm:
    def test_get_norm_q1(self):
        vec = (3, 4)
        expected_norm = 5
        assert math.isclose(get_norm(vec), expected_norm)

    def test_get_norm_zero(self):
        vec = (0, 0)
        expected_norm = 0
        assert math.isclose(get_norm(vec), expected_norm)

    def test_get_norm_q3(self):
        vec = (-2, -2)
        expected_norm = math.sqrt(8)
        assert math.isclose(get_norm(vec), expected_norm)

    def test_get_norm_q2(self):
        vec = (-3, 4)
        expected_norm = 5
        assert math.isclose(get_norm(vec), expected_norm)

    def test_get_norm_q4(self):
        vec = (3, -4)
        expected_norm = 5
        assert math.isclose(get_norm(vec), expected_norm)


class TestSetNorm:
    def test_set_norm_for_nonzero_input_vector(self):
        vec = (3, 4)
        norm = 5
        result = set_norm(vec, norm)
        assert result == (
            3,
            4,
        )  # Ensure the output vector is correctly normalized and scaled

    def test_set_norm_for_zero_input_vector_and_nonzero_norm(self):
        vec = (0, 0)
        norm = 5
        with pytest.raises(ValueError) as excinfo:
            set_norm(vec, norm)
        assert (
            str(excinfo.value)
            == "cannot scale a zero-length vector to a nonzero length"
        )

    def test_set_norm_for_zero_input_vector_and_zero_norm(self):
        vec = (0, 0)
        norm = 0
        result = set_norm(vec, norm)
        assert result == (
            0,
            0,
        )  # Ensure the output vector is (0, 0) for zero input and zero norm


class TestVmul:
    def test_vmul_with_positive_vectors(self):
        vec_a = (2, 3)
        vec_b = (4, 5)
        result = vmul(vec_a, vec_b)
        assert result == (8, 15)

    def test_vmul_with_negative_vectors(self):
        vec_a = (-2, -3)
        vec_b = (4, 5)
        result = vmul(vec_a, vec_b)
        assert result == (-8, -15)

    def test_vmul_with_zero_vector(self):
        vec_a = (0, 0)
        vec_b = (4, 5)
        result = vmul(vec_a, vec_b)
        assert result == (0, 0)


class TestSegToRayException:
    def test_seg_to_ray_with_zero_length_segment(self):
        seg = [(2, 3), (2, 3)]
        with pytest.raises(ValueError) as excinfo:
            _seg_to_ray(seg)
        assert str(excinfo.value) == "points defining segment are coincident"


class TestVdiv:
    def test_vdiv_with_positive_vectors(self):
        vec_a = (10, 6)
        vec_b = (2, 3)
        result = vdiv(vec_a, vec_b)
        assert result == (5, 2)

    def test_vdiv_with_negative_vectors(self):
        vec_a = (-10, -6)
        vec_b = (2, 3)
        result = vdiv(vec_a, vec_b)
        assert result == (-5, -2)

    def test_vdiv_with_zero_vector(self):
        vec_a = (0, 0)
        vec_b = (2, 3)
        result = vdiv(vec_a, vec_b)
        assert result == (0, 0)


class TestGetRayXsectTimes:
    def test_a_at_negative_p25(self):
        ray_a = [(0, 0), (4, 0)]
        ray_b = [(-1, -1), (0, 2)]
        result = _get_ray_xsect_times(ray_a, ray_b)
        assert math.isclose(result[0], -0.25)

    def test_a_at_p25(self):
        ray_a = [(0, 0), (4, 0)]
        ray_b = [(1, -1), (0, 2)]
        result = _get_ray_xsect_times(ray_a, ray_b)
        assert math.isclose(result[0], 0.25)

    def test_a_at_1p25(self):
        ray_a = [(0, 0), (4, 0)]
        ray_b = [(5, -1), (0, 2)]
        result = _get_ray_xsect_times(ray_a, ray_b)
        assert math.isclose(result[0], 1.25)

    def test_b_at_negative_p25(self):
        ray_b = [(0, 0), (4, 0)]
        ray_a = [(-1, -1), (0, 2)]
        result = _get_ray_xsect_times(ray_a, ray_b)
        assert math.isclose(result[1], -0.25)

    def test_b_at_p25(self):
        ray_b = [(0, 0), (4, 0)]
        ray_a = [(1, -1), (0, 2)]
        result = _get_ray_xsect_times(ray_a, ray_b)
        assert math.isclose(result[1], 0.25)

    def test_b_at_1p25(self):
        ray_b = [(0, 0), (4, 0)]
        ray_a = [(5, -1), (0, 2)]
        result = _get_ray_xsect_times(ray_a, ray_b)
        assert math.isclose(result[1], 1.25)


class TestGetLineXsect:
    def test_normal_case(self):
        line_a = [(0, 0), (4, 4)]
        line_b = [(2, 0), (2, 4)]
        expected_result = (2, 2)
        result = get_line_xsect(line_a, line_b)
        assert math.isclose(result[0], expected_result[0])
        assert math.isclose(result[1], expected_result[1])

    def test_parallel_lines_raise_value_error(self):
        line_a = [(0, 0), (1, 1)]
        line_b = [(2, 2), (3, 3)]
        result = get_line_xsect(line_a, line_b)
        assert result is None

    def test_same_first_point(self):
        """Identify first point as intersection when a[0] == b[0]"""
        line_a = [(0, 0), (1, 1)]
        line_b = [(0, 0), (3, -3)]
        result = get_line_xsect(line_a, line_b)
        assert math.isclose(result[0], line_a[0][0])
        assert math.isclose(result[1], line_a[0][1])

    def test_same_last_point(self):
        """Identify first point as intersection when a[1] == b[1]"""
        line_a = [(1, 1), (0, 0)]
        line_b = [(3, -3), (0, 0)]
        result = get_line_xsect(line_a, line_b)

        assert math.isclose(result[0], line_a[1][0])
        assert math.isclose(result[1], line_a[1][1])

    def test_connected(self):
        """Identify shared point as intersection when a[1] == b[0]"""
        line_a = [(1, 1), (0, 0)]
        line_b = [(0, 0), (3, -3)]
        result = get_line_xsect(line_a, line_b)

        assert math.isclose(result[0], line_a[1][0])
        assert math.isclose(result[1], line_a[1][1])


class TestGetSegXsect:
    def test_normal_case(self):
        line_a = [(0, 0), (4, 4)]
        line_b = [(2, 0), (2, 4)]
        expected_result = (2, 2)
        result = get_seg_xsect(line_a, line_b)
        assert math.isclose(result[0], expected_result[0])
        assert math.isclose(result[1], expected_result[1])

    def test_t(self):
        """Identify an intersection at a t-junction"""
        seg_a = [(0, 0), (2, 0)]
        seg_b = [(1, 0), (1, 2)]
        result = get_seg_xsect(seg_a, seg_b)
        assert math.isclose(result[0], 1)
        assert math.isclose(result[1], 0)

    def test_behind_a(self):
        """Do not identify an intersection when seg_a would cross seg_b at t < 0."""
        seg_a = [(0, 0), (2, 0)]
        seg_b = [(-1, -1), (-1, 2)]
        result = get_seg_xsect(seg_a, seg_b)
        assert result is None

    def test_beyond_a(self):
        """Do not identify an intersection when seg_a would cross seg_b at t > 1."""
        seg_a = [(0, 0), (2, 0)]
        seg_b = [(3, -1), (3, 1)]
        result = get_seg_xsect(seg_a, seg_b)
        assert result is None

    def test_before_b(self):
        """Do not identify an intersection when seg_b would cross seg_a at t < 0."""
        seg_a = [(0, 0), (2, 0)]
        seg_b = [(3, -1), (3, 2)]
        result = get_seg_xsect(seg_b, seg_a)
        assert result is None

    def test_beyond_b(self):
        """Do not identify an intersection when seg_a would cross seg_b at t > 1."""
        seg_a = [(0, 0), (2, 0)]
        seg_b = [(3, -1), (3, 1)]
        result = get_seg_xsect(seg_b, seg_a)
        assert result is None

    def test_parallel_lines_raise_value_error(self):
        line_a = [(0, 0), (1, 1)]
        line_b = [(2, 2), (3, 3)]
        result = get_seg_xsect(line_a, line_b)
        assert result is None

    def test_same_first_point(self):
        """Identify first point as intersection when a[0] == b[0]"""
        line_a = [(0, 0), (1, 1)]
        line_b = [(0, 0), (3, -3)]
        result = get_seg_xsect(line_a, line_b)
        assert math.isclose(result[0], line_a[0][0])
        assert math.isclose(result[1], line_a[0][1])

    def test_same_last_point(self):
        """Identify first point as intersection when a[1] == b[1]"""
        line_a = [(1, 1), (0, 0)]
        line_b = [(3, -3), (0, 0)]
        result = get_seg_xsect(line_a, line_b)

        assert math.isclose(result[0], line_a[1][0])
        assert math.isclose(result[1], line_a[1][1])

    def test_connected(self):
        """Identify shared point as intersection when a[1] == b[0]"""
        line_a = [(1, 1), (0, 0)]
        line_b = [(0, 0), (3, -3)]
        result = get_seg_xsect(line_a, line_b)

        assert math.isclose(result[0], line_a[1][0])
        assert math.isclose(result[1], line_a[1][1])


class TestMoveAlong:
    def test_move_along_with_positive_distance(self):
        pnt = (2, 3)
        vec = (4, 4)
        distance = 4 * pow(2, 1 / 2)
        result = move_along(pnt, vec, distance)
        assert math.isclose(result[0], 6)
        assert math.isclose(result[1], 7)

    def test_move_along_with_zero_distance(self):
        pnt = (2, 3)
        vec = (4, 4)
        distance = 0
        result = move_along(pnt, vec, distance)
        assert math.isclose(result[0], 2)
        assert math.isclose(result[1], 3)

    def test_move_along_with_negative_distance(self):
        pnt = (2, 3)
        vec = (4, 4)
        distance = -4 * pow(2, 1 / 2)
        result = move_along(pnt, vec, distance)
        assert math.isclose(result[0], -2)
        assert math.isclose(result[1], -1)


class TestMoveToward:
    def test_move_toward_with_different_points(self):
        pnt = (2, 3)
        target = (5, 6)
        distance = 3 * pow(2, 1 / 2)
        result = move_toward(pnt, target, distance)
        assert math.isclose(result[0], 5)
        assert math.isclose(result[1], 6)

    def test_move_toward_with_zero_distance(self):
        pnt = (2, 3)
        target = (5, 7)
        distance = 0
        result = move_toward(pnt, target, distance)
        assert result == (2, 3)  # Ensure the point stays the same for zero distance


class TestVrotate:
    def test_vrotate_with_positive_angle(self):
        vec = (2, 3)
        angle = math.pi / 2
        result = vrotate(vec, angle)
        assert math.isclose(result[0], -3)
        assert math.isclose(result[1], 2)

    def test_vrotate_with_negative_angle(self):
        vec = (2, 3)
        angle = -math.pi / 2
        result = vrotate(vec, angle)
        assert math.isclose(result[0], 3)
        assert math.isclose(result[1], -2)

    def test_vrotate_with_zero_angle(self):
        vec = (2, 3)
        angle = 0
        result = vrotate(vec, angle)
        assert math.isclose(result[0], 2)
        assert math.isclose(result[1], 3)


class TestQrotate:
    def test_zero_quadrants(self):
        v = (2, 3)
        quadrants = 0
        assert qrotate(v, quadrants) == v

    def test_one_quadrant(self):
        v = (2, 3)
        quadrants = 1
        expected_result = (-3, 2)
        assert qrotate(v, quadrants) == expected_result

    def test_two_quadrants(self):
        v = (2, 3)
        quadrants = 2
        expected_result = (-2, -3)
        assert qrotate(v, quadrants) == expected_result

    def test_three_quadrants(self):
        v = (2, 3)
        quadrants = 3
        expected_result = (3, -2)
        assert qrotate(v, quadrants) == expected_result

    def test_negative_quadrants(self):
        vec = (1, 2)
        result = qrotate(vec, -1)
        assert result == (2, -1)

    def test_multiple_quadrants(self):
        vec = (1, 2)
        result = qrotate(vec, 3)
        assert result == (2, -1)


class TestRotateAround:
    def test_rotate_around_origin(self):
        # Arrange
        pnt = (2, 3)
        center = (0, 0)
        angle = math.pi / 2
        result = rotate_around(pnt, center, angle)
        assert math.isclose(result[0], -3)
        assert math.isclose(result[1], 2)

    def test_rotate_around_center(self):
        # Arrange
        pnt = (5, 5)
        center = (2, 2)
        angle = math.pi / 4
        result = rotate_around(pnt, center, angle)
        assert math.isclose(result[0], 2)
        assert math.isclose(result[1], 2 + 3 * math.sqrt(2))

    def test_rotate_around_self(self):
        # Arrange
        pnt = (-4, 1)
        center = (-4, 1)
        angle = math.pi / 6
        result = rotate_around(pnt, center, angle)
        assert math.isclose(result[0], -4)
        assert math.isclose(result[1], 1)


class TestClosesetPointOnLine:
    def test_get_closest_point_on_line(self):
        line = [(0, 0), (1, 1)]
        point = (2, 2)
        expected_result = (2, 2)
        result = get_closest_point_on_line(line, point)
        assert _isclose_vec(result, expected_result)

    def test_get_closest_point_on_line_same_point(self):
        line = [(0, 0), (1, 1)]
        point = (0, 0)
        expected_result = (0, 0)
        result = get_closest_point_on_line(line, point)
        assert _isclose_vec(result, expected_result)


    def test_get_closest_point_on_line_horizontal_line(self):
        line = [(0, 1), (0, -1)]
        point = (2, 0)
        expected_result = (0, 0)
        result = get_closest_point_on_line(line, point)
        assert _isclose_vec(result, expected_result)

    def test_get_closest_point_on_line_vertical_line(self):
        line = [(1, 0), (-1, 0)]
        point = (0, 2)
        expected_result = (0, 0)
        result = get_closest_point_on_line(line, point)
        assert _isclose_vec(result, expected_result)

    def test_above(self):
        line = [(0, 0), (1, 1)]
        point = (2, 3)
        expected_result = (2.5, 2.5)
        result = get_closest_point_on_line(line, point)
        assert _isclose_vec(result, expected_result)

    def test_below(self):
        line = [(0, 0), (1, 1)]
        point = (2, -3)
        expected_result = (-0.5, -0.5)
        result = get_closest_point_on_line(line, point)
        assert _isclose_vec(result, expected_result)

class TestClosesetPointOnSeg:
    def test_get_closest_point_on_seg(self):
        seg = [(0, 0), (1, 1)]
        point = (2, 2)
        expected_result = (1, 1)
        result = get_closest_point_on_seg(seg, point)
        assert _isclose_vec(result, expected_result)

    def test_get_closest_point_on_seg_same_point(self):
        seg = [(0, 0), (1, 1)]
        point = (0, 0)
        expected_result = (0, 0)
        result = get_closest_point_on_seg(seg, point)
        assert _isclose_vec(result, expected_result)


    def test_get_closest_point_on_seg_horizontal_seg(self):
        seg = [(0, 1), (0, -1)]
        point = (2, 0)
        expected_result = (0, 0)
        result = get_closest_point_on_seg(seg, point)
        assert _isclose_vec(result, expected_result)

    def test_get_closest_point_on_seg_vertical_seg(self):
        seg = [(1, 0), (-1, 0)]
        point = (0, 2)
        expected_result = (0, 0)
        result = get_closest_point_on_seg(seg, point)
        assert _isclose_vec(result, expected_result)

    def test_above(self):
        seg = [(0, 0), (1, 1)]
        point = (2, 3)
        expected_result = (1, 1)
        result = get_closest_point_on_seg(seg, point)
        assert _isclose_vec(result, expected_result)

    def test_below(self):
        seg = [(0, 0), (1, 1)]
        point = (2, -3)
        expected_result = (0, 0)
        result = get_closest_point_on_seg(seg, point)
        assert _isclose_vec(result, expected_result)
