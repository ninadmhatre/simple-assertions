import os
import inspect


class WarnVals:
    """ Possible values when converting errors to warnings"""

    Min = OnlyLineNum = "1"
    Full = TraceBack = "2"


class ValToChk:
    def __init__(self, val, desc):
        self.val = val
        self.desc = desc


def show_line_no(msg, keywords=("check", "PYASSERT_ERRORS_AS_WARNINGS")):
    frame = inspect.currentframe()
    err_frame = None

    while frame:
        names = frame.f_code.co_names
        if all([k in names for k in keywords]):
            err_frame = frame
            break
        frame = frame.f_back

    return "[{}:{}]: {}".format(
        os.path.basename(err_frame.f_code.co_filename), err_frame.f_lineno, msg
    )


class ErrorFormatter:
    def add_desc(self, msg, desc):
        if desc and len(desc) > 0:
            msg = "[{}]: {}".format(desc, msg)
        return msg

    def compare(self, lhs: ValToChk, rhs, cmp_condition: str):
        err_msg = "Expected:[{}] {} [{}]".format(lhs.val, cmp_condition, rhs)
        return self.add_desc(err_msg, lhs.desc)

    def value(self, val_to_chk: ValToChk, cmp_condition: str):
        err_msg = "Expected:<{}> {}".format(val_to_chk.val, cmp_condition)
        return self.add_desc(err_msg, val_to_chk.desc)
