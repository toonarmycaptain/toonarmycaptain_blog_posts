---
title: "Dropping local test runtime and scope with pytest"
description: "Using pytest's -k option to run only the tests for the code I'm working on."
date: 2021-02-25
slug: dropping-local-test-runtime-and-scope-with-pytest
categories: [Python, Testing]
tags: [python, pytest, productivity, testing]
---

I love pytest.

I have a [project](https://github.com/toonarmycaptain/dionysus) that I use as something of a learning platform (and that I don't want to break because it's at least occasionally used in production by my wife..). Most recently I've used it to learn how to abstract a database layer, implement a SQLite database, and now I'm similarly implementing [SQLAlchemy](https://www.sqlalchemy.org/).

<!-- more -->

Database tests can take a...while to run.
The cross product of a test suite and a variety of database backends via `pytest.mark.parametrize` takes...longer.

The other day I [googled "pytest only run specific parameters"](https://www.google.com/search?q=pytest+only+run+specific+parameters) and happened across the `python -m pytest -k some_string` invocation.

Now, I see that the [documentation](https://docs.pytest.org/en/stable/usage.html#Run) refers to strings in quotation marks,[<sup>1</sup>](#footnote-1) but I missed that, and my incovation `python -m pytest -k sqlalchemy` works just fine cut my test runtime down to 1/6th the full suite, running only tests specific to my `SQLiteSQLAlchemyDatabase` object in `sqlite_sqlalchemy.py`, and my common tests that run against every database backend, but only the parameters using my `empty_sqlite_sqlalchemy_database` fixture.[<sup>2</sup>](#footnote-2)

So while I'm working on this backend, and assuming I'm not changing the database interface, I can run the full suite of tests, but only on the part of the code I'm working on. This way, I can ensure that the implementation works (or is getting closer to working), and that it's not breaking any thing that relies on it (because my common interface tests are running, and that one test for another component I would have forgotten that uses this code) as I go, without waiting for the entirety of the project's tests to run!

This is not only saving me time waiting, but means I'm not just running the tests more often, but receiving the feedback  much closer to the writing of the code. You know, I'm actually checking the results of the tests *before* writing much/any subsequent code, that generally relies on the former actually working.

- <a id="footnote-1"><sup>1</sup></a> Later I wondered how run my `SQLiteDatabase` tests without also catching my `SQLiteSQLAlchemyDatabase` tests (which is what would happen by using `sqlite`). The answer was to use a string with logic: `python -m pytest -k "sqlite and not sqlalchemy"`. More options and ideas: [SO: parametrize and running a single test in pytest](https://stackoverflow.com/questions/44943470/parametrize-and-running-a-single-test-in-pytest),
[SO: Pytest select tests based on mark.parameterize value?](https://stackoverflow.com/questions/52785961/pytest-select-tests-based-on-mark-parameterize-value), [Working with custom markers](https://docs.pytest.org/en/latest/example/markers.html).
- <a id="footnote-2"><sup>2</sup></a> I should write a post about how I use fixtures as parameters in `pytest.mark.parametrize`.
