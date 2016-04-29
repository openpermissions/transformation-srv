# Transformation Service Low Level Design
This service transforms asset data in json or comma separated value (csv)
format, to the rights expression language, Open Digital Rights Language (ODRL).

More information on ODRL can be found [here](https://www.w3.org/ns/odrl/2/)

The transformation is performed by the open source service
[Karma](#http://usc-isi-i2.github.io/karma/)

## Contents
+ [Transforming csv data](#transforming-csv-data)
+ [Transforming json data](#transforming-json-data)

## Transform csv data
![](./images/sequence-transform-data.png)

## Transforming json data
The transformation of json data follows the same pattern as csv data replacing
csv with json in the above diagram.