#
# Copyright 2016 Crown Copyright
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from gafferpy import gaffer as g
from gafferpy import gaffer_connector


def run(host, verbose=False):
    return run_with_connector(create_connector(host, verbose))


def run_with_connector(gc):
    print()
    print('Running operations')
    print('--------------------------')
    print()

    get_schema(gc)
    get_filter_functions(gc)
    get_class_filter_functions(gc)
    get_element_generators(gc)
    get_object_generators(gc)
    get_operations(gc)
    get_serialised_fields(gc)
    get_store_traits(gc)

    is_operation_supported(gc)

    add_elements(gc)
    get_elements(gc)
    get_adj_seeds(gc)
    get_all_elements(gc)
    generate_elements(gc)
    generate_domain_objs(gc)
    generate_domain_objects_chain(gc)
    get_element_group_counts(gc)
    get_sub_graph(gc)
    export_to_gaffer_result_cache(gc)
    get_job_details(gc)
    get_all_job_details(gc)
    add_named_operation(gc)
    get_all_named_operations(gc)
    named_operation(gc)
    delete_named_operation(gc)

    sort_elements(gc)
    max_element(gc)
    min_element(gc)

    complex_op_chain(gc)

    op_chain_in_json(gc)


def create_connector(host, verbose=False):
    return gaffer_connector.GafferConnector(host, verbose)


def get_schema(gc):
    # Get Schema
    result = gc.execute_get(
        g.GetSchema()
    )

    print('Schema:')
    print(result)
    print()


def get_filter_functions(gc):
    # Get filter functions
    result = gc.execute_get(
        g.GetFilterFunctions()
    )

    print('Filter Functions:')
    print(result)
    print()


def get_class_filter_functions(gc):
    # Get class filter functions
    class_name = 'uk.gov.gchq.koryphe.impl.predicate.IsMoreThan'
    result = gc.execute_get(
        g.GetClassFilterFunctions(class_name=class_name)
    )

    print('Class Filter Functions (IsMoreThan):')
    print(result)
    print()


def get_element_generators(gc):
    # Get Element generators
    result = gc.execute_get(
        g.GetElementGenerators()
    )

    print('Element generators:')
    print(result)
    print()


def get_object_generators(gc):
    # Get Object generators
    result = gc.execute_get(
        g.GetObjectGenerators()
    )

    print('Object generators:')
    print(result)
    print()


def get_operations(gc):
    # Get operations
    result = gc.execute_get(
        g.GetOperations()
    )

    print('Operations:')
    print(result)
    print()


def get_serialised_fields(gc):
    # Get serialised fields
    class_name = 'uk.gov.gchq.koryphe.impl.predicate.IsMoreThan'
    result = gc.execute_get(
        g.GetSerialisedFields(class_name=class_name)
    )

    print('Serialised Fields (IsMoreThan):')
    print(result)
    print()


def get_store_traits(gc):
    # Get Store Traits
    result = gc.execute_get(
        g.GetStoreTraits()
    )

    print('Store Traits:')
    print(result)
    print()


def is_operation_supported(gc):
    # Is operation supported
    operation = 'uk.gov.gchq.gaffer.operation.impl.add.AddElements'
    result = gc.is_operation_supported(
        g.IsOperationSupported(operation=operation)
    )

    print(
        '\nOperation supported ("uk.gov.gchq.gaffer.operation.impl.add.AddElements"):')
    print(result)
    print()


def add_elements(gc):
    # Add Elements
    gc.execute_operation(
        g.AddElements(
            elements=[
                g.Entity(
                    group='JunctionUse',
                    vertex='M1:1',
                    properties={
                        'countByVehicleType': {
                            "uk.gov.gchq.gaffer.types.FreqMap": {
                                'BUS': 10,
                                'CAR': 50
                            }
                        },
                        'endDate': {
                            'java.util.Date': 1034319600000
                        },
                        'count': {
                            'java.lang.Long': 60
                        },
                        'startDate': {
                            'java.util.Date': 1034316000000
                        }
                    }
                ),
                g.Edge(
                    # TODO remove this deliberate typo
                    group='Unknown group!',
                    source='M1',
                    destination='M1:1',
                    directed=True,
                    property={}
                )
            ]
        )
    )
    print('Elements have been added')
    print()


def get_elements(gc):
    # Get Elements
    elements = gc.execute_operation(
        g.GetElements(
            seeds=[
                g.EntitySeed('M5:10'),

                # Edge seeds can be provided as follows
                g.EdgeSeed('M5:10', 'M5:11', g.DirectedType.EITHER),
                g.EdgeSeed('M5:10', 'M5:11', g.DirectedType.DIRECTED),
                # Or you can use True or False for the direction
                g.EdgeSeed('M5:10', 'M5:11', True)
            ],
            view=g.View(
                edges=[
                    g.ElementDefinition(
                        # TODO remove this deliberate typo
                        group='Unknown group!',
                        transient_properties=[
                            g.Property('description', 'java.lang.String')
                        ],
                        pre_aggregation_filter_functions=[
                            g.FilterFunction(
                                class_name='uk.gov.gchq.koryphe.impl.predicate.IsMoreThan',
                                selection=['count'],
                                function_fields={'value': {'java.lang.Long': 1}}
                            )
                        ],
                        transform_functions=[
                            g.TransformFunction(
                                class_name='uk.gov.gchq.gaffer.traffic.transform.DescriptionTransform',
                                selection=['SOURCE', 'DESTINATION', 'count'],
                                projection=['description']
                            )
                        ]
                    )
                ]
            ),
            directed_type=g.DirectedType.EITHER
        )
    )
    print('Related elements')
    print(elements)
    print()


def get_adj_seeds(gc):
    # Adjacent Elements - chain 2 adjacent entities together
    adj_seeds = gc.execute_operations(
        [
            g.GetAdjacentIds(
                seeds=[
                    g.EntitySeed(
                        vertex='M5'
                    )
                ],
                view=g.View(
                    edges=[
                        g.ElementDefinition('RoadHasJunction')
                    ]
                ),
                in_out_type=g.InOutType.OUT
            ),
            g.GetAdjacentIds(
                view=g.View(
                    edges=[
                        g.ElementDefinition('RoadUse')
                    ]
                ),
                in_out_type=g.InOutType.OUT
            )
        ]
    )
    print('Adjacent entities - 2 hop')
    print(adj_seeds)
    print()


def get_all_elements(gc):
    # Get all elements, but limit the total results to 3, deduplication true
    all_elements = gc.execute_operations(
        operations=[
            g.GetAllElements(),
            g.Limit(result_limit=3)
        ]
    )
    print('All elements (Limited to first 3)')
    print(all_elements)
    print()


def generate_elements(gc):
    # Generate Elements
    elements = gc.execute_operation(
        g.GenerateElements(
            'uk.gov.gchq.gaffer.traffic.generator.RoadTrafficElementGenerator',
            objects=[
                '"South West","E06000054","Wiltshire","6016","389200","179080","M4","LA Boundary","381800","180030","17","391646","179560","TM","E","2000","2000-05-03 00:00:00","7","0","9","2243","15","426","127","21","20","37","106","56","367","3060"'
            ]
        )
    )
    print('Generated elements from provided domain objects')
    print(elements)
    print()


def generate_domain_objs(gc):
    # Generate Domain Objects - single provided element
    objects = gc.execute_operation(
        g.GenerateObjects(
            'uk.gov.gchq.gaffer.rest.example.ExampleDomainObjectGenerator',
            elements=[
                g.Entity('entity', '1'),
                g.Edge('edge', '1', '2', True)
            ]
        )
    )
    print('Generated objects from provided elements')
    print(objects)
    print()


def generate_domain_objects_chain(gc):
    # Generate Domain Objects - chain of get elements then generate objects
    objects = gc.execute_operations(
        [
            g.GetElements(
                seeds=[g.EntitySeed(vertex='M5')],
                seed_matching_type=g.SeedMatchingType.RELATED,
                view=g.View(
                    edges=[
                        g.ElementDefinition(group='RoadHasJunction',
                                            group_by=[])
                    ]
                )
            ),
            g.GenerateObjects(
                'uk.gov.gchq.gaffer.rest.example.ExampleDomainObjectGenerator')
        ]
    )
    print('Generated objects from get elements by seed')
    print(objects)
    print()


def get_element_group_counts(gc):
    # Get Elements
    group_counts = gc.execute_operations([
        g.GetElements(
            seeds=[g.EntitySeed('M5')]
        ),
        g.CountGroups(limit=1000)
    ])
    print('Groups counts (limited to 1000 elements)')
    print(group_counts)
    print()


def get_sub_graph(gc):
    # Export and Get to/from an in memory set
    entity_seeds = gc.execute_operations(
        [
            g.GetAdjacentIds(
                seeds=[g.EntitySeed('South West')],
                in_out_type=g.InOutType.OUT
            ),
            g.ExportToSet(),
            g.GetAdjacentIds(in_out_type=g.InOutType.OUT),
            g.ExportToSet(),
            g.DiscardOutput(),
            g.GetSetExport()
        ]
    )
    print('Export and Get to/from an in memory set')
    print(entity_seeds)
    print()


def export_to_gaffer_result_cache(gc):
    # Export to Gaffer Result Cache and Get from Gaffer Result Cache
    job_details = gc.execute_operations(
        [
            g.GetAdjacentIds(
                seeds=[g.EntitySeed('South West')],
                in_out_type=g.InOutType.OUT
            ),
            g.ExportToGafferResultCache(),
            g.DiscardOutput(),
            g.GetJobDetails()
        ]
    )
    print('Export to Gaffer Result Cache. Job Details:')
    print(job_details)
    print()

    job_id = job_details['jobId']
    entity_seeds = gc.execute_operation(
        g.GetGafferResultCacheExport(job_id=job_id),
    )
    print('Get Gaffer Result Cache Export.')
    print(entity_seeds)
    print()


def get_job_details(gc):
    # Get all job details
    job_details_initial = gc.execute_operations(
        [
            g.GetAdjacentIds(
                seeds=[g.EntitySeed('1')],
            ),
            g.ExportToGafferResultCache(),
            g.DiscardOutput(),
            g.GetJobDetails()
        ]
    )

    job_id = job_details_initial['jobId']

    job_details = gc.execute_operation(
        g.GetJobDetails(job_id=job_id),
    )
    print('Get job details')
    print(job_details)
    print()


def get_all_job_details(gc):
    # Get all job details
    all_job_details = gc.execute_operation(
        g.GetAllJobDetails(),
    )
    print('Get all job details (just prints the first 3 results)')
    print(all_job_details[:3])
    print()


def delete_named_operation(gc):
    gc.execute_operation(
        g.DeleteNamedOperation('CountAllElementGroups')
    )
    print('Deleted named operation: CountAllElementGroups')
    print()


def add_named_operation(gc):
    gc.execute_operation(
        g.AddNamedOperation(
            operation_chain={
                'operations': [{
                    'class': 'uk.gov.gchq.gaffer.operation.impl.get.GetAllElements',
                }, {
                    'class': 'uk.gov.gchq.gaffer.operation.impl.CountGroups'
                }]
            },
            name='CountAllElementGroups',
            description='Counts all element groups',
            overwrite=True
        )
    )
    print('Added named operation: CountAllElementGroups')
    print()


def get_all_named_operations(gc):
    namedOperations = gc.execute_operation(
        g.GetAllNamedOperations()
    )
    print('Named operations')
    print(namedOperations)
    print()


def named_operation(gc):
    result = gc.execute_operation(
        g.NamedOperation('CountAllElementGroups')
    )
    print('Execute named operation')
    print(result)
    print()


def sort_elements(gc):
    # Get sorted Elements
    elements = gc.execute_operations([
        g.GetAllElements(
            view=g.View(
                edges=[
                    g.ElementDefinition(
                        group='RoadUse'
                    )
                ]
            )
        ),
        g.Sort(
            comparators=[
                g.ElementPropertyComparator(
                    groups=['RoadUse'],
                    property='count'
                )
            ],
            result_limit=5
        )
    ])
    print('Sorted elements')
    print(elements)
    print()


def max_element(gc):
    # Get sorted Elements
    elements = gc.execute_operations([
        g.GetAllElements(
            view=g.View(
                edges=[
                    g.ElementDefinition(
                        group='RoadUse'
                    )
                ]
            )
        ),
        g.Max(
            comparators=[
                g.ElementPropertyComparator(
                    groups=['RoadUse'],
                    property='count'
                )
            ]
        )
    ])
    print('Max element')
    print(elements)
    print()


def min_element(gc):
    # Get sorted Elements
    elements = gc.execute_operations([
        g.GetAllElements(
            view=g.View(
                edges=[
                    g.ElementDefinition(
                        group='RoadUse'
                    )
                ]
            )
        ),
        g.Min(
            comparators=[
                g.ElementPropertyComparator(
                    groups=['RoadUse'],
                    property='count'
                )
            ]
        )
    ])
    print('Min element')
    print(elements)
    print()


def complex_op_chain(gc):
    # All road junctions in the South West that were heavily used by buses in year 2000.
    junctions = gc.execute_operations(
        operations=[
            g.GetAdjacentIds(
                seeds=[g.EntitySeed(vertex='South West')],
                view=g.View(
                    edges=[
                        g.ElementDefinition(group='RegionContainsLocation')
                    ]
                )
            ),
            g.GetAdjacentIds(
                view=g.View(
                    edges=[
                        g.ElementDefinition(group='LocationContainsRoad')
                    ]
                )
            ),
            g.ToSet(),
            g.GetAdjacentIds(
                view=g.View(
                    edges=[
                        g.ElementDefinition(group='RoadHasJunction')
                    ]
                )
            ),
            g.GetElements(
                view=g.View(
                    entities=[
                        g.ElementDefinition(
                            group='JunctionUse',
                            group_by=[],
                            transient_properties=[
                                g.Property('busCount', 'java.lang.Long')
                            ],
                            pre_aggregation_filter_functions=[
                                g.FilterFunction(
                                    class_name='uk.gov.gchq.koryphe.impl.predicate.IsMoreThan',
                                    selection=['startDate'],
                                    function_fields={'value': {
                                        'java.util.Date': 946684800000},
                                        'orEqualTo': True}
                                ),
                                g.FilterFunction(
                                    class_name='uk.gov.gchq.koryphe.impl.predicate.IsLessThan',
                                    selection=['endDate'],
                                    function_fields={'value': {
                                        'java.util.Date': 978307200000},
                                        'orEqualTo': False}
                                )
                            ],
                            post_aggregation_filter_functions=[
                                g.FilterFunction(
                                    class_name='uk.gov.gchq.koryphe.impl.predicate.IsMoreThan',
                                    selection=['startDate'],
                                    function_fields={'value': {
                                        'java.util.Date': 946684800000},
                                        'orEqualTo': True}
                                ),
                                g.FilterFunction(
                                    class_name='uk.gov.gchq.koryphe.predicate.PredicateMap',
                                    selection=['countByVehicleType'],
                                    function_fields={
                                        'predicate': {
                                            'class': 'uk.gov.gchq.koryphe.impl.predicate.IsMoreThan',
                                            'orEqualTo': False,
                                            'value': {
                                                'java.lang.Long': 1000
                                            }
                                        },
                                        'key': 'BUS'
                                    }
                                )
                            ],
                            transform_functions=[
                                g.TransformFunction(
                                    selection=['countByVehicleType'],
                                    class_name='uk.gov.gchq.gaffer.function.FreqMapExtractor',
                                    function_fields={'key': 'BUS'},
                                    projection=['busCount']
                                )
                            ]
                        )
                    ]
                ),
                in_out_type=g.InOutType.OUT
            ),
            g.ToCsv(
                element_generator={
                    'class': 'uk.gov.gchq.gaffer.data.generator.CsvGenerator',
                    'fields': {
                        'VERTEX': 'Junction',
                        'busCount': 'Bus Count'
                    },
                    'quoted': False,
                    'header': 'Junction,Bus Count'
                }
            )
        ]
    )
    print(
        'All road junctions in the South West that were heavily used by buses in year 2000.')
    print(junctions)
    print()


def op_chain_in_json(gc):
    # Operation chain defined in json
    result = gc.execute_operation_chain(
        {
            "operations": [{
                "class": "uk.gov.gchq.gaffer.operation.impl.get.GetAllElements",
            }, {
                "class": "uk.gov.gchq.gaffer.operation.impl.CountGroups"
            }]
        }
    )
    print('Operation chain defined in json')
    print(result)
    print()


if __name__ == "__main__":
    run('http://localhost:8080/rest/v1', False)
