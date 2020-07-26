# simple-assertions

Assertion library (skeleton) inspired from [assertpy](https://github.com/assertpy/assertpy) but without batteries! also allows to convert all the assertions to warnings, just like delayed asserts.

[![Build Status](https://travis-ci.org/ninadmhatre/simple-assertions.svg?branch=master)](https://travis-ci.org/ninadmhatre/simple-assertions)

## Installation

```
pip install simple-assertions
```

## Usage

Please check `tests/test_*.py` files for more usage here is only basic usage

### As Function
Just import the `check` function, and away you go...

```python
from simple_assertions import check

def test_something():
    check(4 + 10).is_equal_to(14)
    check(1).is_instance_of(int)
    check(3, "lucky_num", as_warn=True).is_equal_to(4)
```

### As instance

```python
from simple_assertions import SimpleAssertions

class YourTestClass:
    def __init__(self):
        self.check = SimpleAssertions().check

    def test_something(self):
        self.check(4 + 10).is_equal_to(14)
        self.check(1).is_instance_of(int)
        self.check(3, "lucky_num", as_warn=True).is_equal_to(4)      
```

### Add your own batteries
```python
from simple_assertions import SimpleAssertions
from typing import Union

class YourAssertions(SimpleAssertions):
    def __init__(self, as_warn=False, logger=None):
        super().__init__(as_warn, logger)

    def is_greater_than(self, other: Union[int, float]):
        if self.val_to_chk.val < other:
            self.raise_err(self.compare_err_msg(other, "to be greater than"))
        return self


class YourTestClass:
    def __init__(self):
        self.check = YourAssertions().check

    def test_something(self):
        self.check(4 + 10).is_greater_than(10).is_equal_to(14)
        self.check(1).is_instance_of(int)
        self.check(3, "lucky_num", as_warn=True).is_equal_to(4)      
```

Though only checked with `unittests` but it should work fine with [pytest](http://pytest.org/) or [Nose](http://nose.readthedocs.org/).

## Converting Errors to Warnings

Assume you have following test case, 

```python
class FuncBasedCases(unittest.TestCase):
    def test_failed_assertions(self):
        check("a").is_numeric()
        check("1").is_in([1, 2])
        check(1).is_not_in([1, 2])
        check(1).is_equal_or_in_seq([3, 4])
        check(None).is_true()
        check(1).is_false()
        check(1).is_instance_of(str)


if __name__ == "__main__":
    unittest.main()
```

### running as-is, error will stop execution

```bash
$ python -m unittest -v tests/test_sample.py

Traceback (most recent call last):
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 10, in test_failed_assertions
    check("a").is_numeric()
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 166, in is_numeric
    self.raise_err(self.value_err_msg("to be numeric"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 80, in raise_err
    raise AssertionError(msg)
AssertionError: Expected:<a> to be numeric

```

> Note: test will be reported as PASSED!
### running with show only errors but continue execution

```bash
$ set ASSERT_ERROR_AS_WARNING=1
$  python -m unittest -v tests/test_sample.py
C:\Users\ninad\PycharmProjects\simple-assertions>python -m unittest -v tests/test_sample.py
test_failed_assertions (tests.test_sample.FuncBasedCases) ... what is ASSERT_ERROR_AS_WARNING set to?: 1
2020-07-27 00:30:03,736 [WARNING] - [test_sample.py:16]: Expected:<a> to be numeric
2020-07-27 00:30:03,736 [WARNING] - [test_sample.py:17]: Expected:[1] to be in [[1, 2]]
2020-07-27 00:30:03,737 [WARNING] - [test_sample.py:18]: Expected:[1] to be not in [[1, 2]]
2020-07-27 00:30:03,737 [WARNING] - [test_sample.py:19]: Expected:[1] be in [[3, 4]]
2020-07-27 00:30:03,738 [WARNING] - [test_sample.py:20]: Expected:<None> to be true
2020-07-27 00:30:03,738 [WARNING] - [test_sample.py:21]: Expected:<1> to be false
2020-07-27 00:30:03,739 [WARNING] - [test_sample.py:22]: Expected: [int] to be of type [<class 'str'>]
ok

```

> Note: test will be reported as PASSED!
### running with traceback but continue execution

```bash
$ set ASSERT_ERROR_AS_WARNING=2
$  python -m unittest -v tests/test_sample.py

C:\Users\ninad\PycharmProjects\simple-assertions>python -m unittest -v tests/test_sample.py
test_failed_assertions (tests.test_sample.FuncBasedCases) ... what is ASSERT_ERROR_AS_WARNING set to?: 2
..
... stack trace ...
..
File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 16, in test_failed_assertions
    check("a").is_numeric()
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 166, in is_numeric
    self.raise_err(self.value_err_msg("to be numeric"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
2020-07-27 00:31:17,637 [WARNING] - Expected:<a> to be numeric
..
... stack trace ...
..
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 17, in test_failed_assertions
    check("1").is_in([1, 2])
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 115, in is_in
    self.raise_err(self.compare_err_msg(other, "to be in"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
2020-07-27 00:31:17,658 [WARNING] - Expected:[1] to be in [[1, 2]]
..
... stack trace ...
..
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 18, in test_failed_assertions
    check(1).is_not_in([1, 2])
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 120, in is_not_in
    self.raise_err(self.compare_err_msg(other, "to be not in"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
2020-07-27 00:31:17,679 [WARNING] - Expected:[1] to be not in [[1, 2]]
..
... stack trace ...
..
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 19, in test_failed_assertions
    check(1).is_equal_or_in_seq([3, 4])
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 128, in is_equal_or_in_seq
    self.raise_err(self.compare_err_msg(other, "be in"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
2020-07-27 00:31:17,695 [WARNING] - Expected:[1] be in [[3, 4]]
..
... stack trace ...
..
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 20, in test_failed_assertions
    check(None).is_true()
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 133, in is_true
    self.raise_err(self.value_err_msg("to be true"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
2020-07-27 00:31:17,718 [WARNING] - Expected:<None> to be true
..
... stack trace ...
..
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 21, in test_failed_assertions
    check(1).is_false()
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 138, in is_false
    self.raise_err(self.value_err_msg("to be false"))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
..
... stack trace ...
..
  File "C:\Users\ninad\PycharmProjects\simple-assertions\tests\test_sample.py", line 22, in test_failed_assertions
    check(1).is_instance_of(str)
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 146, in is_instance_of
    self.raise_err(
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 78, in raise_err
    self.logger.warning(log_as_warning(msg))
  File "C:\Users\ninad\PycharmProjects\simple-assertions\simple_assertions\__init__.py", line 33, in log_as_warning
    traceback.print_stack()
2020-07-27 00:31:17,754 [WARNING] - Expected: [int] to be of type [<class 'str'>]
ok

----------------------------------------------------------------------
Ran 1 test in 0.299s

OK


```

# Motivation 

`assertpy` is beautiful library but for my needs it's too much, i really loved the API of `assertpy` so i created new module because of following reasons


1. I wanted `assert_warn` to be dynamic, i.e. given certain condition all assertions are converted to
warning.
   - I added `ASSERT_ERROR_AS_WARNING` variable which can do that!
   - Modified `assert_that` API to make is call based with `assert_that(.., as_warn=True)`
2. Extending is possible but i wanted more intuitive logic
   - I exposed the `SimpleAssertions` class, and just inherit it to add new method
3. `assert_that` in `assertpy` creates new instance of class and loads all the extensions on every
call, and i wanted to avoid that!
   - By exposing the `SimpleAssertion` class, you can just make it part of your assertion class

> Note: earlier i used `assert_that` keyword from `assertpy` but i felt like it's copying from other library
>, so i changed `assert_that` to `check`, while reading this gives same reading experience but now saved 6 chars!

