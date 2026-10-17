---
title: "Unit testing with assertive mocks vs not testing implementation: Why not both?"
description: "Parametrizing a test to run with and without assertions in its mocks, to get the benefits of both."
date: 2021-03-30
slug: assertive-mocks
categories: [Python, Testing]
tags: [unittest, python, pytest, mock]
---

Often I will have a function that contains another function call, and want to write a unit test for it.

```python
"""my_module"""

def function_under_test(arg):
    # do stuff
    var = called_function(arg2)
    # do stuff
    return something
```

<!-- more -->

The typical [pytest](https://docs.pytest.org) way of testing `function_under_test` as a unit (rather than `function_under_test` and `called_function`) would be to mock out/monkeypatch `called_function`:

```python
def test_function_under_test():

    def mock_called_function(*args):
        # I usually assign expected_args/return value 
        # based on test inputs/parametrize
        assert args = expected_args
        return appropriate_test_value

    monkeypatch.setattr(module_containing_called_function, "called_function", mock_called_function)
    
    assert function_under_test(arg) == expected_result
```

Now often I want to mock out the function call, as it might be writing to file, making network calls etc.
*But* this means if I change how I'm calling `called_function`, or the internals of `called_function`, the test breaks, even if the arguments to `function_under_test` and it's return value are exactly the same. So in a sense, it's not a pure unit test unless you get rid of the `assert` in the mock, it's still halfway to an integration test, provided your mock is accurate, because it cares what it was called by (although it can be simpler in terms of defining mocks to put a small amount of logic there, rather than specifying for each test case).

I have found (and it might just be me), that even when I run integration tests and pure(r) unit tests, I diagnose errors more easily when I have the assertions in my mocked function calls, because then it's easy to nail down the source of the error.
Yes, it can be a *lot more work*, because you might have to make changes to tests when you change the implementation (although you might have to anyway if the mocked function's return value would be different...).

But what if you simply did both?

```python
@pytest.mark.parametrize[<sup>1</sup>](#footnote-1)('mock_assertions', [True, False])
def test_function_under_test(mock_assertions):

    def mock_called_function(*args):
        if mock_assertions:
            assert args = expected_args
        return appropriate_test_value

    monkeypatch.setattr(module_containing_called_function, "called_function", mock_called_function)
    
    assert function_under_test(arg) == expected_result
```

This way, you get instant feedback if you changed the behaviour of `function_under_test`, but you also get feedback if you changed the calls you might make to `called_function` in ways you did not expect. Sure you can make mistakes in your `mock_called_function` args and return values...but at least you need to think about them, particularly if the calls/needed return values change.

Integration tests are still necessary, because whatever you *say* `called_function` returns in your mocks, that might not be what it *actually* returns.
Yet I wonder if, despite some extra work to maintain, testing this way gets the best of a couple of worlds, helping us better pin down that our functions do what we expect, without flawed tests that pass because we returned what we'd want, rather than what we'd get, and helping us pinpoint *why* our integration tests failed (*if* we have them, and *if* they have the same exploration of edge cases as our unit tests).

Or is it better to have the integration tests and pure(r) unit tests, even if the integration tests force you to mock expensive/disk/network calls anyway?

What do you think?
&nbsp;
&nbsp;
&nbsp;
&nbsp;
<a id="footnote-1"><sup>1</sup></a> Do you use [`@pytest.mark.parametrize`](https://docs.pytest.org/en/stable/parametrize.html)? It lets you specify a bunch of different inputs to your tests, and pass/fail the test run on each input. It is excellent.
