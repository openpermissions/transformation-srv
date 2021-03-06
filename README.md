The Open Permissions Platform Transformation Service
====================================================

Useful Links
============
* [Open Permissions Platform](http://openpermissions.org)
* [Low level Design](https://github.com/openpermissions/transformation-srv/blob/master/documents/markdown/low-level-design.md)
* [API Documentation](https://github.com/openpermissions/transformation-srv/blob/master/documents/apiary/api.md)

Service Overview
================
The Transformation Service is a simple service used to transform rights data to a valid xml format.

Running locally
---------------
To run the service locally:

```
pip install -r requirements/dev.txt
python setup.py develop
python transformation/
```

To show a list of available CLI parameters:

```
python transformation/ -h [--help]
```

To start the service using test.service.conf:

```
python transformation/ -t [--test]
```

Running tests and generating code coverage
------------------------------------------
To have a "clean" target from build artifacts:

```
make clean
```

To install requirements. By default, prod requirement is used:

```
make requirements [REQUIREMENT=dev|prod]
```

To run all unit tests and generate an HTML code coverage report along with a
JUnit XML report in tests/unit/reports:

```
make test
```

To run pyLint and generate a HTML report in tests/unit/reports:

```
make pylint
```

To run create the documentation for the service in _build:

```
make docs
```
