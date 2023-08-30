import pytest

from astropy.time import Time

from astropy.io import ascii
from ..tmoc import TimeMOC, times_to_microseconds, microseconds_to_times

import numpy as np


def test_time_to_microsec_1():
    """Test of the time conversion from `astropy.time` with format isot to microseconds."""
    t = Time("1999-01-01T00:00:00.123456789", format="isot", scale="tdb")
    us = times_to_microseconds(t)
    jd = microseconds_to_times(us)
    assert us == 211781908800123456
    assert jd.jd == t.jd


def test_time_to_microsec_2():
    """Test of the time conversion from `astropy.time` with format iso to microseconds."""
    t = Time([["1998-01-01", "1999-01-01"]], format="iso", scale="tdb")
    us1 = times_to_microseconds(t)
    us2 = np.asarray(t.jd * 86400000000, dtype=np.uint64)
    jd1 = microseconds_to_times(us1)
    jd2 = microseconds_to_times(us2)
    print(us1)
    print(us2)
    assert (us1 == us2).all()
    assert (jd1.jd == jd2.jd).all()


def test_complement():
    assert TimeMOC.new_empty(61).complement() == TimeMOC.from_depth61_ranges(
        61,
        np.array([[0, 2 * 2**61]], dtype=np.uint64),
    )
    assert TimeMOC.new_empty(61).complement().complement() == TimeMOC.new_empty(61)
    assert TimeMOC.from_depth61_ranges(
        61,
        np.array([[1, 2], [6, 8], [5, 6]], dtype=np.uint64),
    ).complement() == TimeMOC.from_depth61_ranges(
        61,
        np.array([[0, 1], [2, 5], [8, 2 * 2**61]], dtype=np.uint64),
    )


def test_to_depth61_ranges():
    assert (
        TimeMOC.from_depth61_ranges(
            61,
            np.array([[1, 2], [6, 8], [5, 6]], dtype=np.uint64),
        ).to_depth61_ranges
        == np.array([[1, 2], [5, 8]], dtype=np.uint64)
    ).all()


def test_empty_tmoc():
    times = Time([], format="jd", scale="tdb")
    tmoc = TimeMOC.from_times(times)
    assert tmoc.empty()
    assert tmoc.total_duration == 0

    with pytest.raises(ValueError, match="No min value in an empty MOC"):
        _ = tmoc.min_time  # follow ruff recommendation /ruff/issues/3831

    with pytest.raises(
        ValueError,
        match="No max value in an empty MOC",
    ):  # pytest styles : should add the match parameter
        _ = tmoc.max_time

    tmoc_ranges = TimeMOC.from_time_ranges(times, times)
    assert tmoc_ranges.empty()
    assert tmoc_ranges.total_duration == 0


def test_simple_tmoc():
    times = Time(
        [2 / TimeMOC.DAY_MICRO_SEC, 7 / TimeMOC.DAY_MICRO_SEC],
        format="jd",
        scale="tdb",
    )
    tmoc = TimeMOC.from_times(times, delta_t=TimeMOC.order_to_time_resolution(61))
    assert tmoc.total_duration.sec == 2 * 1e-6
    assert tmoc.max_order == 61

    # tmoc.write('tmoc.txt', format='json', overwrite=True)
    tmoc.save("tmoc.txt", format="json", overwrite=True)


def test_single_time_tmoc():
    times = Time(2 / TimeMOC.DAY_MICRO_SEC, format="jd", scale="tdb")
    tmoc = TimeMOC.from_times(times, delta_t=TimeMOC.order_to_time_resolution(61))
    assert tmoc.total_duration.sec == 1 * 1e-6
    assert tmoc.max_order == 61


def test_single_range_time_tmoc():
    min_times = Time(2 / TimeMOC.DAY_MICRO_SEC, format="jd", scale="tdb")
    max_times = Time(3 / TimeMOC.DAY_MICRO_SEC, format="jd", scale="tdb")

    tmoc = TimeMOC.from_time_ranges(
        min_times,
        max_times,
        delta_t=TimeMOC.order_to_time_resolution(61),
    )
    assert tmoc.total_duration.sec == 1 * 1e-6
    assert tmoc.max_order == 61


def test_tmoc_from_time_ranges():
    """Test tmocs built from time ranges.

    Assert a correct tmoc loaded from a fits file is equal to the
    tmoc built from a CSV file containing a list of time intervals.
    """
    tmoc = TimeMOC.load("resources/TMOC/HST_SDSSg/TMoc.fits", "fits")

    # Load HST_SDSSg from a CSV file
    data = ascii.read("resources/TMOC/HST_SDSSg/uniq-times.csv", format="csv")
    tmoc2 = TimeMOC.from_time_ranges_approx(
        Time(data["t_min"], format="mjd", scale="tdb"),
        Time(data["t_max"], format="mjd", scale="tdb"),
        delta_t=TimeMOC.order_to_time_resolution(57),
    )

    assert tmoc.max_order == tmoc2.max_order
    assert tmoc.min_time == tmoc2.min_time
    assert tmoc.max_time == tmoc2.max_time
    assert tmoc == tmoc2

    with pytest.raises(ValueError):
        TimeMOC.from_time_ranges(
            Time([], format="jd", scale="tdb"),
            Time([3], format="jd", scale="tdb"),
        )


def test_tmoc_from_single_time_range():
    """Test tmoc build from a single time range.

    Assert a correct tmoc loaded from a fits file is equal to the
    tmoc built from a CSV file containing a list of time intervals.
    """
    tmoc = TimeMOC.from_time_ranges(
        Time(0, format="mjd", scale="tdb"),
        Time(3, format="mjd", scale="tdb"),
        delta_t=TimeMOC.order_to_time_resolution(61),
    )
    assert tmoc.total_duration.jd == 3


def test_add_neighbours():
    times = Time(
        [2 / TimeMOC.DAY_MICRO_SEC, 7 / TimeMOC.DAY_MICRO_SEC],
        format="jd",
        scale="tdb",
    )
    times_expected = Time(
        np.array([1, 2, 3, 6, 7, 8]) / TimeMOC.DAY_MICRO_SEC,
        format="jd",
        scale="tdb",
    )
    tmoc = TimeMOC.from_times(times, delta_t=TimeMOC.order_to_time_resolution(61))

    tmoc_expected = TimeMOC.from_times(
        times_expected,
        delta_t=TimeMOC.order_to_time_resolution(61),
    )
    tmoc.add_neighbours()

    assert tmoc == tmoc_expected


def test_remove_neighbours():
    times = Time(
        np.array([1, 2, 3, 6, 7, 8]) / TimeMOC.DAY_MICRO_SEC,
        format="jd",
        scale="tdb",
    )
    times_expected = Time(
        [2 / TimeMOC.DAY_MICRO_SEC, 7 / TimeMOC.DAY_MICRO_SEC],
        format="jd",
        scale="tdb",
    )

    tmoc = TimeMOC.from_times(times, delta_t=TimeMOC.order_to_time_resolution(61))
    tmoc_expected = TimeMOC.from_times(
        times_expected,
        delta_t=TimeMOC.order_to_time_resolution(61),
    )

    tmoc.remove_neighbours()

    assert tmoc == tmoc_expected


def test_add_remove_back_and_forth():
    times = Time(
        [2 / TimeMOC.DAY_MICRO_SEC, 7 / TimeMOC.DAY_MICRO_SEC],
        format="jd",
        scale="tdb",
    )

    tmoc = TimeMOC.from_times(times, delta_t=TimeMOC.order_to_time_resolution(61))
    tmoc_expected = TimeMOC.from_times(
        times,
        delta_t=TimeMOC.order_to_time_resolution(61),
    )

    print(tmoc.to_string())
    tmoc.add_neighbours().remove_neighbours()

    assert tmoc == tmoc_expected


def test_contains():
    tmoc = TimeMOC.from_time_ranges(
        Time(np.array([0]), format="mjd", scale="tdb"),
        Time(np.array([1]), format="mjd", scale="tdb"),
        delta_t=TimeMOC.order_to_time_resolution(61),
    )

    times_inside = Time(np.linspace(0, 1, num=100), format="mjd", scale="tdb")
    times_outside = Time(np.linspace(1.01, 2, num=100), format="mjd", scale="tdb")
    times_in_and_out = Time(np.linspace(0.9, 2, num=100), format="mjd", scale="tdb")

    assert tmoc.contains_with_timeresolution(times_inside).all()
    assert (~tmoc.contains_with_timeresolution(times_outside)).all()
    assert tmoc.contains_with_timeresolution(times_in_and_out).any()


@pytest.mark.parametrize(
    "a, b, expect",
    [
        (
            TimeMOC.from_times(Time(np.array([0, 2]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([0, 1, 2]), format="jd", scale="tdb")),
        ),
        (
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
        ),
        (
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
        ),
    ],
)
def test_union(a, b, expect):
    res = a.union(b)

    assert res == expect


@pytest.mark.parametrize(
    "a, b, expect",
    [
        (
            TimeMOC.from_times(Time(np.array([0, 2]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([0, 2]), format="jd", scale="tdb")),
        ),
        (
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
        ),
        (
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
        ),
    ],
)
def test_difference(a, b, expect):
    res = a.difference(b)

    assert res == expect


@pytest.mark.parametrize(
    "a, b, expect",
    [
        (
            TimeMOC.from_times(Time(np.array([0, 1, 2]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
        ),
        (
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([1]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
        ),
        (
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
            TimeMOC.from_times(Time(np.array([]), format="jd", scale="tdb")),
        ),
    ],
)
def test_intersection(a, b, expect):
    res = a.intersection(b)

    assert res == expect


# ------- TESTING IO features -------#
def test_tmoc_save_load_deser():
    """Test of IO features.

    1. Serializations
    2. Load
    3. Save
    """
    tmoc = TimeMOC.from_string("31/1 32/4 35/")

    # test to_string "json"
    tmoc_json = tmoc.to_string("json")
    tmoc_from_json = TimeMOC.from_string(tmoc_json, "json")
    assert tmoc == tmoc_from_json

    # test to_string "ascii"
    tmoc_ascii = tmoc.to_string("ascii")
    tmoc_from_ascii = TimeMOC.from_string(tmoc_ascii, "ascii")
    assert tmoc == tmoc_from_ascii

    # test load from an ascii file
    tmoc_load_ascii = TimeMOC.load("resources/MOC2.0/tmoc.ascii.txt", "ascii")
    assert tmoc == tmoc_load_ascii

    # test load from fits
    tmoc_load_fits = TimeMOC.load("resources/MOC2.0/TMOC.fits", "fits")
    assert tmoc == tmoc_load_fits

    # tests of save in the three formats
    tmoc.save("resources/MOC2.0/tmoc.py.test.fits", format="fits", overwrite=True)
    tmoc.save("resources/MOC2.0/tmoc.py.test.json", format="json", overwrite=True)
    tmoc.save("resources/MOC2.0/tmoc.py.test.ascii", format="ascii", overwrite=True)
    tmoc_saved_fits = TimeMOC.load("resources/MOC2.0/tmoc.py.test.fits", "fits")
    assert tmoc == tmoc_saved_fits
    tmoc_saved_json = TimeMOC.load("resources/MOC2.0/tmoc.py.test.json", "json")
    assert tmoc == tmoc_saved_json
    tmoc_saved_ascii = TimeMOC.load("resources/MOC2.0/tmoc.py.test.ascii", "ascii")
    assert tmoc == tmoc_saved_ascii
