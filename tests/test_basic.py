import unittest
from contextlib import redirect_stderr
from io import StringIO

from simple_assertions import check, PYASSERT_ERRORS_AS_WARNINGS, WarnVals
from tests.helper import SetEnvVarContext


class SampleMsg:
    def __init__(self, msg_type, seq_num, data):
        self.msg_type = msg_type
        self.seq_num = seq_num
        self.data = data

    def __repr__(self):
        return "Msg(type={}, seq_num={}, data={})".format(
            self.msg_type, self.seq_num, self.data
        )


def assert_msg_type(msg):
    check(msg.msg_type, "msg_type").is_instance_of(str)
    check(msg.msg_type, "msg_type").is_in(("fix4.1", "fix4.2"))


def assert_seq_num(msg):
    check(msg.seq_num, "seq_num").is_instance_of(int).is_equal_to(10)

    # deliberately using bare assert
    assert msg.seq_num >= 10, "Expected: <{}> to be >= 10".format(msg.seq_num)


class FuncBasedCases(unittest.TestCase):
    def setUp(self) -> None:
        self.msg = SampleMsg("fix4.1", 10, "trade_msg")

    def test_happy_path(self):
        check(self.msg.msg_type, "msg_type").is_equal_to("fix4.1")
        check(self.msg.seq_num, "seq_num").is_equal_to(10)
        check(self.msg.data, "data").is_populated()

        # chain
        check(self.msg.data, "data").is_populated().is_not_equal_to("any")

    def test_basic_all_as_warn_using_arg(self):
        # all assertions will fail but still it will continue
        check(self.msg.msg_type, "msg_type", as_warn=True).is_equal_to("fix4")
        check(self.msg.seq_num, "seq_num", as_warn=True).is_equal_to(9)
        check(self.msg.data, "data", as_warn=True).is_not_populated()

    def test_basic_all_as_warn_env_var_show_lineno(self):
        with SetEnvVarContext(
            PYASSERT_ERRORS_AS_WARNINGS, WarnVals.OnlyLineNum
        ):
            check(self.msg, "msg_type_check").is_not_instance_of(
                (SampleMsg, int)
            )
            check(self.msg.msg_type, "msg_type").is_equal_to("fix4")
            check(self.msg.seq_num, "seq_num").is_equal_to(9)
            check(self.msg.data, "data").is_not_populated()

    def test_basic_all_as_warn_env_var_traceback(self):
        with SetEnvVarContext(PYASSERT_ERRORS_AS_WARNINGS, WarnVals.TraceBack):
            output = StringIO()
            with redirect_stderr(output):
                check(self.msg, "msg_type_check").is_not_instance_of(
                    (SampleMsg, int)
                )

            self.assertIn(
                "traceback.print_stack()",
                output.getvalue(),
                "failed to find err text stderr! Captured:\n {}".format(output.getvalue()),
            )

    def test_base_selective_warn(self):
        check(self.msg.msg_type, "msg_type").is_equal_to("fix4.1")
        check(self.msg.seq_num, "seq_num", as_warn=True).is_equal_to(5)
        check(self.msg.data, "data").is_populated()

    def test_assert_in_multiple_places(self):
        assert_msg_type(self.msg)
        assert_seq_num(self.msg)
        check(self.msg.data, "data").is_populated().is_equal_to("trade_msg")

    def test_raises_exceptions(self):
        with self.assertRaises(AssertionError):
            check(self.msg.msg_type).is_equal_to("not_matching")

    def test_other_assertions(self):
        check("1").is_numeric()
        check(True, "there_will_be_cure_for_covid-19").is_true()
        check(False, "is_world_a_happy_place").is_false()
        check(1, "eq_or_in?").is_equal_or_in_seq(1)
        check(1, "eq_or_in?").is_equal_or_in_seq([1, 2, 3])
        check(1).is_not_instance_of(str)
        check(1).is_not_in([2, 3, 4])

    def test_failed_assertions(self):
        with self.assertRaises(AssertionError):
            check("a").is_numeric()

        with self.assertRaises(AssertionError):
            check("1").is_in([1, 2])

        with self.assertRaises(AssertionError):
            check(1).is_not_in([1, 2])

        with self.assertRaises(AssertionError):
            check(1).is_equal_or_in_seq([3, 4])

        with self.assertRaises(AssertionError):
            check(None).is_true()

        with self.assertRaises(AssertionError):
            check(1).is_false()

        with self.assertRaises(AssertionError):
            check(1).is_instance_of(str)


if __name__ == "__main__":
    unittest.main()
