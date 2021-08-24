from contextlib import contextmanager
from deepdiff import DeepDiff
import json
import logging
import os
from time import sleep
import pytest

from gridappsd import GridAPPSD
from gridappsd import GridAPPSD,topics as t
from gridappsd.simulation import Simulation
from gridappsd_docker import docker_up, docker_down

LOGGER = logging.getLogger(__name__)

POWERGRID_MODEL = 'powergridmodel'
database_type = POWERGRID_MODEL
request_topic = '.'.join((t.REQUEST_DATA, database_type))
slept = 0

def sleep_once():
    """Sleep one time to allow blazegraph to become available"""
    global slept
    if slept == 0:
        sleep(30)
        slept = 1

def test_power_model_names(gridappsd_client_module):
    """Verify all models are present"""
    gapps = gridappsd_client_module
    sleep_once()
    LOGGER.info('Performing model name query')
    response = gapps.query_model_names(model_id=None)
    LOGGER.debug(f'Response: {response}')
    #os.makedirs("/tmp/output", exist_ok=True)
    #with open("/tmp/output/power.json", 'w') as f:
        #f.write(json.dumps(response, indent=4, sort_keys=True))
    with open('./simulation_baseline_files/power_api_models.json', 'r') as f:
        baseline = json.load(f)
    LOGGER.debug(f'Baseline: {baseline}')
    result = DeepDiff(baseline, response, ignore_order=True, exclude_paths="root['id']")
    assert (result == {}), f'Powergrid API model name differs {result}'

def test_power_object(gridappsd_client_module):
    """Verify object exists in model"""
    gapps = gridappsd_client_module
    sleep_once()
    LOGGER.info('Performing object query')
    obj = '_46EA069B-F08C-4945-9C08-8F7CABECCF5C'
    response = gapps.query_object(obj, model_id=None)
    LOGGER.debug(f'Response: {response}')
    #os.makedirs("/tmp/output", exist_ok=True)
    #with open("/tmp/output/power2.json", 'w') as f:
    #    f.write(json.dumps(response, indent=4, sort_keys=True))
    with open('./simulation_baseline_files/power_api_object.json', 'r') as f:
        baseline = json.load(f)
    LOGGER.debug(f'Baseline: {baseline}')
    result = DeepDiff(baseline, response, ignore_order=True, exclude_paths="root['id']")
    assert (result == {}), f'Powergrid API object {obj} differs {result}'

def test_power_object_type(gridappsd_client_module):
    """Verify object types in model"""
    gapps = gridappsd_client_module
    sleep_once()
    LOGGER.info('Performing object type query')
    response = gapps.query_object_types(model_id=None)
    #os.makedirs("/tmp/output", exist_ok=True)
    #with open("/tmp/output/power3.json", 'w') as f:
    #    f.write(json.dumps(response, indent=4, sort_keys=True))
    with open('./simulation_baseline_files/power_api_object_types.json', 'r') as f:
        baseline = json.load(f)
    LOGGER.debug(f'Baseline: {baseline}')
    result = DeepDiff(baseline, response, ignore_order=True, exclude_paths="root['id']")
    assert (result == {}), f'Powergrid API object types differs {result}'

def test_power_query_model_info(gridappsd_client_module):
    """Verify model information is correct"""
    gapps = gridappsd_client_module
    sleep_once()
    LOGGER.info('Performing model info query')
    response = gapps.query_model_info()
    #os.makedirs("/tmp/output", exist_ok=True)
    #with open("/tmp/output/power4.json", 'w') as f:
    #    f.write(json.dumps(response, indent=4, sort_keys=True))
    with open('./simulation_baseline_files/power_api_model_info.json', 'r') as f:
        baseline = json.load(f)
    LOGGER.debug(f'Baseline: {baseline}')
    result = DeepDiff(baseline, response, ignore_order=True, exclude_paths="root['id']")
    assert (result == {}), f'Powergrid API query model differs {result}'

def test_power_query_data_new(gridappsd_client_module):
    """Verify model data info query is correct"""
    gapps = gridappsd_client_module
    sleep_once()
    LOGGER.info('Performing model data query')
    query = "select ?feeder_name ?subregion_name ?region_name WHERE {?line r:type c:Feeder.?line c:IdentifiedObject.name  ?feeder_name.?line c:Feeder.NormalEnergizingSubstation ?substation.?substation r:type c:Substation.?substation c:Substation.Region ?subregion.?subregion  c:IdentifiedObject.name  ?subregion_name .?subregion c:SubGeographicalRegion.Region  ?region . ?region   c:IdentifiedObject.name  ?region_name}"
    response = gapps.query_data(query, database_type=POWERGRID_MODEL, timeout=30)
    #os.makedirs("/tmp/output", exist_ok=True)
    #with open("/tmp/output/power5.json", 'w') as f:
    #    f.write(json.dumps(response, indent=4, sort_keys=True))
    with open('./simulation_baseline_files/power_api_model_data.json', 'r') as f:
        baseline = json.load(f)
    LOGGER.debug(f'Baseline: {baseline}')
    result = DeepDiff(baseline, response, ignore_order=True, exclude_paths="root['id']")
    print(result)
    assert (result == {}), f'Powergrid API query data differs for quer {query} {result}'

