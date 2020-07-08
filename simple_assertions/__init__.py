import inspect
import logging
import os
from typing import Any, Union, Iterable, AnyStr

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - %(message)s", level=logging.INFO
)
_logger = logging.getLogger(__name__)


PYASSERT_ERRORS_AS_WARNINGS = "ASSERT_ERROR_AS_WARNING"

__version__ = "0.2.0"


class ValToChk:
    def __init__(self, val, desc):
        self.val = val
        self.desc = desc


def _show_line_no(msg):
    def _unwind(_frame, fn="assert_that"):
        if _frame and fn in _frame.f_code.co_names:
            return _frame
        return _unwind(_frame.f_back, fn)

    frame = _unwind(inspect.currentframe())
    line_no = frame.f_lineno
    filename = os.path.basename(frame.f_code.co_filename)

    return "[{}:{}]: {}".format(filename, line_no, msg)


def _is_warn_mode_set_using_envvar() -> bool:
    """
    check if warn mode is set using env variable
    :return: bool
    """
    return os.getenv(PYASSERT_ERRORS_AS_WARNINGS, "").lower() in ("1", "true")


class AssertionsBase:
    def __init__(self, as_warn: bool, logger=None):
        self.logger = logger or _logger
        self._as_warn_flag = as_warn
        self.is_warn_mode = False
        self.val_to_chk = None

        self._is_running_in_warn_mode()

    def _is_running_in_warn_mode(self, override=False):
        """
        determine whether to run in fast fail (fail on first) or convert assertion
        errors to just warnings to continue with remaining program
        :param override: if set, set as warn mode
        :return: bool
        """
        self.is_warn_mode = (
            override
            or self._as_warn_flag
            or _is_warn_mode_set_using_envvar()
        )

    def set_fields(self, val, desc, as_warn=False):
        self.val_to_chk = ValToChk(val, desc)
        self._is_running_in_warn_mode(as_warn)

    def clear_fields(self):
        self.val_to_chk = None
        self.is_warn_mode = False

    def _add_desc(self, msg):
        if self.val_to_chk.desc and len(self.val_to_chk.desc) > 0:
            msg = "[{}]: {}".format(self.val_to_chk.desc, msg)
        return msg

    def generate_err_msg(self, other, cmp_condition: str):
        err_msg = "Expected:<{}> {} <{}>".format(
            self.val_to_chk.val, cmp_condition, other
        )
        return self._add_desc(err_msg)

    def generate_err_msg_for_val_check(self, cmp_condition: str):
        err_msg = "Expected:<{}> {}".format(self.val_to_chk.val, cmp_condition)
        return self._add_desc(err_msg)

    def error(self, msg):
        """Helper to raise an ``AssertionError`` with the given message."""
        if self.is_warn_mode:
            self.logger.warning(_show_line_no(msg))
        else:
            raise AssertionError(msg)


class SimpleAssertions(AssertionsBase):
    def __init__(self, as_warn=False, logger=None):
        super().__init__(as_warn, logger)

    def assert_that(self, val, desc=None, as_warn=False):
        self.clear_fields()
        self.set_fields(val, desc, as_warn)

        return self

    def is_equal_to(self, other: Union[AnyStr, int, float]):
        if self.val_to_chk.val != other:
            self.error(self.generate_err_msg(other, "to be equal to"))
        return self

    def is_not_equal_to(self, other: Union[AnyStr, int, float]):
        if self.val_to_chk.val == other:
            self.error(self.generate_err_msg(other, "to be not equal to"))
        return self

    def is_populated(self):
        if self.val_to_chk.val in (None, ""):
            self.error(self.generate_err_msg_for_val_check("to be populated"))
        return self

    def is_not_populated(self):
        if self.val_to_chk.val not in (None, ""):
            self.error(
                self.generate_err_msg_for_val_check("to not to be populated")
            )
        return self

    def is_in(self, other: Iterable):
        if self.val_to_chk.val not in other:
            self.error(self.generate_err_msg(other, "to be in"))
        return self

    def is_not_in(self, other: Iterable):
        if self.val_to_chk.val in other:
            self.error(self.generate_err_msg(other, "to be not in"))
        return self

    def is_equal_or_in_seq(self, other: Union[Any, Iterable]):
        if not isinstance(other, Iterable):
            other = (other,)

        if self.val_to_chk.val not in other:
            self.error(self.generate_err_msg(other, "be in"))
        return self

    def is_true(self):
        if not self.val_to_chk.val:
            self.error(self.generate_err_msg_for_val_check("to be true"))
        return self

    def is_false(self):
        if self.val_to_chk.val:
            self.error(self.generate_err_msg_for_val_check("to be false"))
        return self

    def is_instance_of(self, other: Any):
        if not isinstance(self.val_to_chk.val, other):
            err = "Expected: [{}] to be of type [{}]".format(
                type(self.val_to_chk.val).__name__, other
            )
            self.error(self._add_desc(err))
        return self

    def is_not_instance_of(self, other: Any):
        if isinstance(self.val_to_chk.val, other):
            err = "Expected: [{}] not to be of type [{}]".format(
                type(self.val_to_chk.val).__name__, other
            )
            self.error(self._add_desc(err))
        return self

    def is_numeric(self):
        if not isinstance(self.val_to_chk.val, (float, int)):
            try:
                int(self.val_to_chk.val)
            except ValueError:
                self.error(
                    self.generate_err_msg_for_val_check("to be numeric")
                )

        return self


def assert_that(val, desc=None, as_warn=False) -> SimpleAssertions:
    """
    function based assertion call
    :param val: val to check
    :param desc: optional, description of val
    :param as_warn: if set, convert assertion error to warning message
    :return: assertionClass
    """

    return SimpleAssertions(as_warn=as_warn).assert_that(val, desc)
