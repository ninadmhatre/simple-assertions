import unittest
import os

from simple_assertions import SimpleAssertions, PYASSERT_ERRORS_AS_WARNINGS


class SampleMsg:
    def __init__(self, msg_type, seq_num, data):
        self.msg_type = msg_type
        self.seq_num = seq_num
        self.data = data

    def __repr__(self):
        return "Msg(type={}, seq_num={}, data={})".format(
            self.msg_type, self.seq_num, self.data
        )


def assert_msg_type(assert_that, msg):
    assert_that(msg.msg_type, "msg_type").is_instance_of(str)
    assert_that(msg.msg_type, "msg_type").is_in(("fix4.1", "fix4.2"))


class CompositionBasedUse(unittest.TestCase):
    """
    all tests are same as `test_basic` with only difference of how `assert_that`
    is instantiated. Uses composition based approach.
    """

    def setUp(self) -> None:
        self.msg = SampleMsg("fix4.1", 10, "trade_msg")
        self.assert_that = SimpleAssertions().assert_that

    def assert_seq_num(self):
        self.assert_that(self.msg.seq_num, "seq_num").is_instance_of(
            int
        ).is_equal_to(10)

        # deliberately using bare assert, refer test_extend.py
        assert self.msg.seq_num >= 10, "Expected: <{}> to be >= 10".format(
            self.msg.seq_num
        )

    def test_happy_path(self):
        self.assert_that(self.msg.msg_type, "msg_type").is_equal_to("fix4.1")
        self.assert_that(self.msg.seq_num, "seq_num").is_equal_to(10)
        self.assert_that(self.msg.data, "data").is_populated()

        # chain
        self.assert_that(self.msg.data, "data").is_populated().is_not_equal_to(
            "any"
        )

    def test_basic_all_as_warn_using_arg(self):
        # all assertions will fail but still it will continue
        self.assert_that(
            self.msg.msg_type, "msg_type", as_warn=True
        ).is_equal_to("fix4")

        self.assert_that(
            self.msg.seq_num, "seq_num", as_warn=True
        ).is_equal_to(9)

        self.assert_that(
            self.msg.data, "data", as_warn=True
        ).is_not_populated()

    def test_basic_all_as_warn_env_var(self):
        os.environ[PYASSERT_ERRORS_AS_WARNINGS] = "true"

        self.assert_that(self.msg, "mst_type_check").is_not_instance_of(
            (SampleMsg, int)
        )
        self.assert_that(self.msg.msg_type, "msg_type").is_equal_to("fix4")
        self.assert_that(self.msg.seq_num, "seq_num").is_equal_to(9)
        self.assert_that(self.msg.data, "data").is_not_populated()

        del os.environ[PYASSERT_ERRORS_AS_WARNINGS]

    def test_base_selective_warn(self):
        self.assert_that(self.msg.msg_type, "msg_type").is_equal_to("fix4.1")
        self.assert_that(
            self.msg.seq_num, "seq_num", as_warn=True
        ).is_equal_to(5)
        self.assert_that(self.msg.data, "data").is_populated()

    def test_assert_in_multiple_places(self):
        assert_msg_type(self.assert_that, self.msg)
        self.assert_seq_num()
        self.assert_that(self.msg.data, "data").is_populated().is_equal_to(
            "trade_msg"
        )

    def test_raises_exceptions(self):
        with self.assertRaises(AssertionError):
            self.assert_that(self.msg.msg_type).is_equal_to("not_matching")

    def test_other_assertions(self):
        self.assert_that("1").is_numeric()
        self.assert_that(True, "there_will_be_cure_for_covid-19").is_true()
        self.assert_that(False, "is_world_a_happy_place").is_false()
        self.assert_that(1, "eq_or_in?").is_equal_or_in_seq(1)
        self.assert_that(1, "eq_or_in?").is_equal_or_in_seq([1, 2, 3])
        self.assert_that(1).is_not_instance_of(str)
        self.assert_that(1).is_not_in([2, 3, 4])

    def test_failed_assertions(self):
        with self.assertRaises(AssertionError):
            self.assert_that("a").is_numeric()

        with self.assertRaises(AssertionError):
            self.assert_that("1").is_in([1, 2])

        with self.assertRaises(AssertionError):
            self.assert_that(1).is_not_in([1, 2])
            
        with self.assertRaises(AssertionError):
            self.assert_that(1).is_equal_or_in_seq([3, 4])
            
        with self.assertRaises(AssertionError):
            self.assert_that(None).is_true()

        with self.assertRaises(AssertionError):
            self.assert_that(1).is_false()
            
        with self.assertRaises(AssertionError):
            self.assert_that(1).is_instance_of(str)

if __name__ == "__main__":
    unittest.main()
