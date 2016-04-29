FORMAT: 1A
HOST: https://tran-stage.copyrighthub.org

# Open Permissions Platform Transformation Service
The Transformation Service is a simple service used to transform rights data to a valid xml format.

## Standard error output
On endpoint failure there is a standard way to report errors.
The output should be of the form

| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| errors   | A list of errors          | array  |

### Error
| Property       | Description                                 | Type   | Mandatory |
| :-------       | :----------                                 | :---   | :-------  |
| source         | The name of the service producing the error | number | yes       |
| message        | A description of the error                  | string | yes       |
| line           | The line the error occurred                 | number | no        |

# Authorization

This API requires authentication. Where [TOKEN] is indicated in an endpoint header you should supply an OAuth 2.0 access token with the appropriate scope (read, write or delegate).

See [How to Auth](https://github.com/openpermissions/auth-srv/blob/master/documents/markdown/how-to-auth.md)
for details of how to authenticate Hub services.

# Group Service information
Information on the service

## Service information [/v1/transformation]

### Retrieve service information [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service information   | object |

##### Service information
| Property     | Description                                  | Type   |
| :-------     | :----------                                  | :---   |
| service_name | The name of the api service                  | string |
| version      | The version of the api service               | string |
| service_id   | The ID of the transformation service         | string |

+ Request
    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)
    + Body

            {
                "status": 200,
                "data": {
                    "service_name": "Open Permissions Platform Transformation Service",
                    "version": "0.1.0",
                    "service_id": "2c254cdce21411e581cfacbc32a8c615"
                }
            }

# Group Capabilities

## Service Capabilities [/v1/transformation/capabilities]
Returns the service capabilities.

### Retrieve Service Capabilities [GET]

| OAuth Token Scope |
| :----------       |
| read              |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service capabilities  | object |

##### Service capabilities
| Property           | Description                         | Type |
| :-------           | :----------                         | :--- |
| max_post_body_size | Maximum body size for post requests | int  |

+ Request
    + Headers

            Authorization: Bearer [TOKEN]
            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)
    + Body

            {
                "status": 200,
                "data": {
                    "max_post_body_size": 26214400
                }
            }


# Group Assets

## Assets [/v1/transformation/assets{?r2rml_url}]

+ Parameters
    + r2rml_url (optional, url, `https://example.com/r2rml_mappings_csv.ttl`)
        url for an r2rml mapping file. The mapping file should be an
RDF graph in Turtle syntax expressing the logic for transforming the
original CSV or JSON data into an RDF document using the Open
Permissions Ontology.

### Transform rights data for assets [POST]

| OAuth Token Scope |
| :----------       |
| write             |

#### Input

Multiple id types can be onboarded for a given asset.
The first id type and value will be used to form the hub key,
and the rest will be registered as aliases.

An optional parameter r2rml_url for a url to an r2rml mappings file can be supplied to apply customised transformation.

If the parameter is not supplied, the default mapping is used, which transforms data in the following csv or json format.

##### Assets data as a csv file

| Property         | Description                                           | Type   | Mandatory |
| :-------         | :----------                                           | :----  | :-------- |
| source_id_types  | Tilde separated list of source id types               | string | yes       |
| source_ids       | Tilde separated list of source ids                    | string | yes       |
| offer_ids        | Tilde separated list of offer ids available for asset | string | no        |
| set_ids          | Tilde separated list of set ids that asset belongs to | string | no        |
| description      | Description of asset                                  | string | no        |

##### Assets data as JSON

| Property         | Description                         | Type   | Mandatory |
| :-------         | :----------                         | :---   | :-------- |
| source_ids       | Array of source id objects          | array  | yes       |
| offer_ids        | Array of offer ids available to it  | array  | no        |
| set_ids          | Array of set ids that it belongs to | array  | no        |
| description      | Description of asset                | string | no        |

###### Source id object

| Property       | Description     | Type    |
| :-------       | :----------     | :------ |
| source_id_type | Source id type  | string  |
| source_id      | Source id value | string  |


#### Output

| Property | Description                                   | Type   |
| :------- | :----------                                   | :---   |
| status   | The status of the request                     | number |
| data     | Asset data transformed into different formats | object |


+ Request Asset of triples with valid csv data (text/csv; charset=utf-8)
    + Headers

            Authorization: Bearer [TOKEN]
            Accept: application/json

    + Body

            source_id_types,source_ids,offer_ids,set_ids,description
            examplecopictureid,100123,1~2~3~4,,Sunset over a Caribbean beach
            examplecopictureid~anotherpictureid,100456~999002,1~2~3~4,,Polar bear on an ice floe

+ Response 200 (application/json; charset=UTF-8)
    + Body

            {
                "status": 200,
                "data": {
                    "rdf_n3":
                        "<http://openpermissions.org/ns/id/2> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/20051> .
                        _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/anotherpictureid> .
                        _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        <http://openpermissions.org/ns/hub/anotherpictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType> .
                        _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 <http://openpermissions.org/ns/op/1.1/value> \"x100123\" .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Asset> .
                        <http://openpermissions.org/ns/id/1> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/10051> .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://purl.org/dc/terms/modified> \"2016-03-10T10:47:21.486000Z\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
                        <http://openpermissions.org/ns/id/2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://purl.org/dc/terms/description> \"Sunset over ? C?ribbe?n be?ch\" .
                        <http://openpermissions.org/ns/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        
                        <http://openpermissions.org/ns/id/3> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        <http://openpermissions.org/ns/id/2> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/20051> .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://openpermissions.org/ns/op/1.1/value> \"x100456\" .
                        <http://openpermissions.org/ns/id/4> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/40051> .
                        <http://openpermissions.org/ns/id/4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/examplecopictureid> .
                        <http://openpermissions.org/ns/hub/anotherpictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType> .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/anotherpictureid> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Asset> .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/examplecopictureid> .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/anotherpictureid> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://purl.org/dc/terms/description> \"Pol?r be?r on ?n ice floe\" .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://openpermissions.org/ns/op/1.1/value> \"x999002\" .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://purl.org/dc/terms/modified> \"2016-03-10T10:47:21.486999Z\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
                        <http://openpermissions.org/ns/id/1> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/10051> .
                        <http://openpermissions.org/ns/id/2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        <http://openpermissions.org/ns/id/3> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/30051> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        <http://openpermissions.org/ns/hub/examplecopictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 .
                        <http://openpermissions.org/ns/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        
                        _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 <http://openpermissions.org/ns/op/1.1/value> \"x999001\" .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://purl.org/dc/terms/description> \"Johnny Depp as Sweeney Todd\" .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://purl.org/dc/terms/modified> \"2016-03-10T10:47:21.486999Z\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Asset> .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 .
                        _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/examplecopictureid> .
                        <http://openpermissions.org/ns/hub/examplecopictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType>
                        "
                }
            }

+ Request Asset of triples with valid json data (application/json; charset=utf-8)
    + Headers

            Authorization: Bearer [TOKEN]
            Accept: application/json

    + Body

            [
                {
                    "source_ids": [
                      {
                         "source_id_type": "examplecopictureid",
                         "source_id": "100123"
                      }
                    ],
                    "offer_ids": [
                        "1",
                        "2",
                        "3",
                        "4"
                    ],
                    "set_ids": [],
                    "description": "Sunset over a Caribbean beach"
                },
                {
                    "source_ids": [
                      {
                        "source_id": "100456",
                        "source_id_type": "examplecopictureid"
                      },
                      {
                        "source_id_type": "anotherpictureid",
                        "source_id": "999002"
                      }
                    ],
                    "offer_ids": [
                        "1",
                        "2",
                        "3",
                        "4"
                    ],
                    "set_ids": [],
                    "description": "Polar bear on an ice floe"
                }
            ]

+ Response 200 (application/json; charset=UTF-8)
    + Body

            {
                "status": 200,
                "data": {
                    "rdf_n3":
                        "<http://openpermissions.org/ns/id/2> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/20051> .
                        _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/anotherpictureid> .
                        _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        <http://openpermissions.org/ns/hub/anotherpictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType> .
                        _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 <http://openpermissions.org/ns/op/1.1/value> \"x100123\" .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_e4f0b34cd51831d93d57d0412f6931ae4746c51f_N77 .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Asset> .
                        <http://openpermissions.org/ns/id/1> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/10051> .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://purl.org/dc/terms/modified> \"2016-03-10T10:47:21.486000Z\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
                        <http://openpermissions.org/ns/id/2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        <http://openpermissions.org/ns/id/a409940c7986429185a6f456587c9a26> <http://purl.org/dc/terms/description> \"Sunset over ? C?ribbe?n be?ch\" .
                        <http://openpermissions.org/ns/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        
                        <http://openpermissions.org/ns/id/3> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        <http://openpermissions.org/ns/id/2> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/20051> .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://openpermissions.org/ns/op/1.1/value> \"x100456\" .
                        <http://openpermissions.org/ns/id/4> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/40051> .
                        <http://openpermissions.org/ns/id/4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/examplecopictureid> .
                        <http://openpermissions.org/ns/hub/anotherpictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType> .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/anotherpictureid> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Asset> .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/examplecopictureid> .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/anotherpictureid> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://purl.org/dc/terms/description> \"Pol?r be?r on ?n ice floe\" .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://openpermissions.org/ns/op/1.1/value> \"x999002\" .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://purl.org/dc/terms/modified> \"2016-03-10T10:47:21.486999Z\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
                        <http://openpermissions.org/ns/id/1> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/10051> .
                        <http://openpermissions.org/ns/id/2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        <http://openpermissions.org/ns/id/3> <http://openpermissions.org/ns/op/1.1/defaultTarget> <http://openpermissions.org/ns/id/30051> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 .
                        _:ol_Id1_608942548ab3f90be2ca70233917201fec6ee0d9_N78 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        <http://openpermissions.org/ns/hub/examplecopictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType> .
                        <http://openpermissions.org/ns/id/cde49df0bb8547af99870c12dcd29fe6> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_0ecc21203bfb8a78050f71c0d5a5bcf771720314_N79 .
                        <http://openpermissions.org/ns/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Policy> .
                        
                        _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Id> .
                        _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 <http://openpermissions.org/ns/op/1.1/value> \"x999001\" .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://purl.org/dc/terms/description> \"Johnny Depp as Sweeney Todd\" .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://purl.org/dc/terms/modified> \"2016-03-10T10:47:21.486999Z\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/Asset> .
                        <http://openpermissions.org/ns/id/6142b3a2e2f441baa309f4e0a175f989> <http://openpermissions.org/ns/op/1.1/alsoIdentifiedBy> _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 .
                        _:ol_Id1_1e2430ee1eb2d3fd23133a253a5e9c0ac597264c_N80 <http://openpermissions.org/ns/op/1.1/id_type> <http://openpermissions.org/ns/hub/examplecopictureid> .
                        <http://openpermissions.org/ns/hub/examplecopictureid> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://openpermissions.org/ns/op/1.1/IdType>
                        "
                }
            }

+ Request Attempt to create triples with invalid csv data (text/csv; charset=utf-8)
    + Headers

            Authorization: Bearer [TOKEN]
            Accept: text/xml, application/json

    + Body

            source_id_types,source_ids,offer_ids,set_ids,description
            ,1~2~3~4,,Sunset over a Caribbean beach
            examplecopictureid~anotherpictureid,100456~999002,1~2~3~4,,Polar bear on an ice floe
            anotherpictureid,,1~3,,Johnny Depp as Sweeney Todd
            anotherpictureid,999002,1~3,,Evening street view Paris 1910

+ Response 400 (application/json; charset=UTF-8)
    + Body

            {
                "errors" : [
                    {
                        "source": "transformation",
                        "line": 2,
                        "message": "Missing value for SourceIdType"
                    },
                    {
                        "source": "transformation",
                        "line": 4,
                        "message": "Missing value for SourceId"
                    }
                ]
            }

+ Request Attempt to create triples with invalid source id type (text/csv; charset=utf-8)
    + Headers

            Authorization: Bearer [TOKEN]
            Accept: text/xml, application/json

    + Body

            source_id_types,source_ids,description,offer_ids
            IllegalPictureIDType,100123,Sunset over á Cáribbeán beách,01~02

+ Response 400 (application/json; charset=UTF-8)
    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "transformation",
                        "message": "unknown source id type IllegalPictureIDType"
                    }
                ]
            }
