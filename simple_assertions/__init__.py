import logging
import os
from typing import Any, Union, Iterable, AnyStr
import traceback

from simple_assertions.helper import WarnVals, show_line_no, ErrorFormatter, ValToChk

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - %(message)s", level=logging.INFO
)
_logger = logging.getLogger(__name__)


PYASSERT_ERRORS_AS_WARNINGS = "ASSERT_ERROR_AS_WARNING"

__version__ = "0.3.1"


def _read_err_to_warn_envvar() -> str:
    return os.getenv(PYASSERT_ERRORS_AS_WARNINGS, "").lower()


def _is_warn_mode_set_using_envvar() -> bool:
    """
    check if warn mode is set using env variable
    :return: bool
    """
    return _read_err_to_warn_envvar() in WarnVals.__dict__.values()


def log_as_warning(msg):
    if _read_err_to_warn_envvar() == WarnVals.TraceBack:
        traceback.print_stack()
        return msg
    elif _read_err_to_warn_envvar() == WarnVals.OnlyLineNum:
        return show_line_no(msg)
    else:
        return show_line_no(msg, keywords=("check",))


class Base:
    def __init__(self, as_warn: bool, logger=None):
        self.logger = logger or _logger
        self._as_warn_flag = as_warn
        self.is_warn_mode = False
        self.val_to_chk = None
        self.format_err_msg = ErrorFormatter()
        self._is_running_in_warn_mode()

    def _is_running_in_warn_mode(self, override=False):
        """
        determine whether to run in fast fail (fail on first) or convert assertion
        errors to just warnings to continue with remaining program
        :param override: if set, set as warn mode
        :return: bool
        """
        self.is_warn_mode = (
            override or self._as_warn_flag or _is_warn_mode_set_using_envvar()
        )

    def set_fields(self, val, desc, as_warn=False):
        self.val_to_chk = ValToChk(val, desc)
        self._is_running_in_warn_mode(as_warn)

    def clear_fields(self):
        self.val_to_chk = None
        self.is_warn_mode = False

    def compare_err_msg(self, rhs, help_text):
        return self.format_err_msg.compare(self.val_to_chk, rhs, help_text)

    def value_err_msg(self, help_text):
        return self.format_err_msg.value(self.val_to_chk, help_text)

    def raise_err(self, msg):
        """Helper to raise an ``AssertionError`` with the given message."""
        if self.is_warn_mode:
            self.logger.warning(log_as_warning(msg))
        else:
            raise AssertionError(msg)


class SimpleAssertions(Base):
    def __init__(self, as_warn=False, logger=None):
        super().__init__(as_warn, logger)

    def check(self, val, desc=None, as_warn=False):
        self.clear_fields()
        self.set_fields(val, desc, as_warn)

        return self

    def is_equal_to(self, other: Union[AnyStr, int, float]):
        if self.val_to_chk.val != other:
            self.raise_err(self.compare_err_msg(other, "to be equal to"))
        return self

    def is_not_equal_to(self, other: Union[AnyStr, int, float]):
        if self.val_to_chk.val == other:
            self.raise_err(self.compare_err_msg(other, "to be not equal to"))
        return self

    def is_populated(self):
        if self.val_to_chk.val in (None, ""):
            self.raise_err(self.value_err_msg("to be populated"))
        return self

    def is_not_populated(self):
        if self.val_to_chk.val not in (None, ""):
            self.raise_err(self.value_err_msg("to not to be populated"))
        return self

    def is_in(self, other: Iterable):
        if self.val_to_chk.val not in other:
            self.raise_err(self.compare_err_msg(other, "to be in"))
        return self

    def is_not_in(self, other: Iterable):
        if self.val_to_chk.val in other:
            self.raise_err(self.compare_err_msg(other, "to be not in"))
        return self

    def is_equal_or_in_seq(self, other: Union[Any, Iterable]):
        if not isinstance(other, Iterable):
            other = (other,)

        if self.val_to_chk.val not in other:
            self.raise_err(self.compare_err_msg(other, "be in"))
        return self

    def is_true(self):
        if not self.val_to_chk.val:
            self.raise_err(self.value_err_msg("to be true"))
        return self

    def is_false(self):
        if self.val_to_chk.val:
            self.raise_err(self.value_err_msg("to be false"))
        return self

    def is_instance_of(self, other: Any):
        if not isinstance(self.val_to_chk.val, other):
            err = "Expected: [{}] to be of type [{}]".format(
                type(self.val_to_chk.val).__name__, other
            )
            self.raise_err(
                self.format_err_msg.add_desc(err, self.val_to_chk.desc)
            )
        return self

    def is_not_instance_of(self, other: Any):
        if isinstance(self.val_to_chk.val, other):
            err = "Expected: [{}] not to be of type [{}]".format(
                type(self.val_to_chk.val).__name__, other
            )
            self.raise_err(
                self.format_err_msg.add_desc(err, self.val_to_chk.desc)
            )
        return self

    def is_numeric(self):
        if not isinstance(self.val_to_chk.val, (float, int)):
            try:
                int(self.val_to_chk.val)
            except ValueError:
                self.raise_err(self.value_err_msg("to be numeric"))

        return self


def check(val, desc=None, as_warn=False) -> SimpleAssertions:
    """
    function based assertion call
    :param val: val to check
    :param desc: optional, description of val
    :param as_warn: if set, convert assertion error to warning message
    :return: assertionClass
    """

    return SimpleAssertions(as_warn=as_warn).check(val, desc)
