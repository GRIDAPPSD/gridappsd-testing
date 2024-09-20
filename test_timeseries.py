import ast
from contextlib import contextmanager
import json
import logging
import os
from time import sleep, time
import sys
import pytest

from gridappsd import GridAPPSD
from gridappsd.simulation import Simulation
from gridappsd_docker import docker_up, docker_down
from gridappsd import GridAPPSD, topics as t

LOGGER = logging.getLogger(__name__)

result_weather_data = []
result_timeseries_query = []
result_sensor_query = []

@pytest.mark.parametrize("sim_config_file, sim_result_file", [
    ("9500-timeseries-config.json", "9500-simulation.json")
    # ("123-config.json", "123-simulation.json"),
    # ("13-node-config.json", "13-node-sim.json"),
    # , ("t3-p1-config.json", "t3-p1.json"),
])
def test_timeseries_output(gridappsd_client, sim_config_file, sim_result_file):
    global result_weather_data
    global result_timeseries_query
    global result_sensor_query
    simulation_id = None
    sim_config_file = os.path.join(os.path.dirname(__file__), f"simulation_config_files/{sim_config_file}")
    sim_result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files/{sim_result_file}")

    assert os.path.exists(sim_config_file), f"File {sim_config_file} must exist to run simulation test"

    gapps = gridappsd_client
    sim_complete = False
    rcvd_measurement = False

    def onmeasurement(sim, timestep, measurements):
        LOGGER.info('Measurement received at %s', timestep)

    def onfinishsimulation(sim):
        nonlocal sim_complete
        sim_complete = True
        LOGGER.info('Simulation Complete')


    simulation_start = int(time())
    with open(sim_config_file) as fp:
        LOGGER.info('Loading config')
        run_config = json.load(fp)
        simulation_start = run_config["simulation_config"]["start_time"]
        simulation_start_str = str(simulation_start) 
        LOGGER.info(f'Simulation start time {simulation_start_str}')


    sim = Simulation(gapps, run_config)
    LOGGER.info(f'Simulation id {sim.simulation_id}')

    LOGGER.info('sim.add_oncomplete_callback')
    sim.add_oncomplete_callback(onfinishsimulation)

    LOGGER.info('sim.add_onmeasurement_callback')
    sim.add_onmeasurement_callback(onmeasurement)


    print('About to query weather')
    with open("./simulation_config_files/weather_data.json", 'r') as g:
        LOGGER.info('Querying weather data from timeseries')
        print('Querying weather data from timeseries')
        query1 = json.load(g)
        result_weather_data = gapps.get_response(t.TIMESERIES, query1, timeout=60)
        LOGGER.info('Weather data received ')
        print('Weather data received ')
        LOGGER.info(result_weather_data)
        print(result_weather_data)
        LOGGER.info(type(result_weather_data))
        print(type(result_weather_data))
        
    LOGGER.info('Starting the simulation')
    sim.start_simulation()
    sim.run_loop()

    with open("./simulation_config_files/timeseries_query.json", 'r') as f:
        query2 = json.load(f)
        #simulation_end = int(time())
        simulation_end = int(simulation_start)+25

        query2["queryFilter"]["simulation_id"] = sim.simulation_id
        query2["queryFilter"]["starttime"] = simulation_start
        query2["queryFilter"]["endtime"] = simulation_end       
        LOGGER.info('Querying simulation data from timeseries')
        LOGGER.info(query2)
        try:
            result_timeseries_query = gapps.get_response(t.TIMESERIES, query2, timeout=600)
            print('Time series query complete')
            LOGGER.info('Simulation data received for Timeseries API')
            LOGGER.info(result_timeseries_query)
        except Exception as err:
            LOGGER.info('Error in time series query')
            LOGGER.info(err)


    with open("./simulation_config_files/sensor_query.json", 'r') as file:
        simulation_end = int(simulation_start)+100000000
        sensor_query = json.load(file)
        sensor_query["queryFilter"]["starttime"] = simulation_start
        sensor_query["queryFilter"]["endtime"] = simulation_end       
        sensor_query["queryFilter"]["simulation_id"] = sim.simulation_id
        LOGGER.info('Querying GridAPPS-D sensor simulator data from timeseries')
        LOGGER.info(sensor_query)
        result_sensor_query = gapps.get_response(t.TIMESERIES, sensor_query, timeout=600)
        LOGGER.info('Simulation data received for sensor simulator')
        LOGGER.info(result_sensor_query)

def test_weather_api():
    global result_weather_data

    LOGGER.info('Weather data received in test ')
    LOGGER.info(result_weather_data)
    LOGGER.info(type(result_weather_data))

    if type(result_weather_data) == str:
        LOGGER.info('Weather data is a string, parsing')
        result_weather_data = json.loads(result_weather_data)
    result_weather_data_obj = {}    
    if "data" in result_weather_data:
        result_weather_data_obj = result_weather_data["data"]
        if type(result_weather_data_obj) == str:
            result_weather_data_obj = json.loads(result_weather_data_obj)
    try:
         assert "Diffuse" in result_weather_data_obj[0], \
            f'Weather data query does not have expected output {result_weather_data_obj[0]}'
    except KeyError:
        assert (result_weather_data_obj != {}), \
            f'Weather data query does not have expected output {result_weather_data}'
    LOGGER.info('Weather data query has expected output')


def test_timeseries_simulation_api():
    global result_timeseries_query
    LOGGER.info('Timeseries data received in test ')
    LOGGER.info(result_timeseries_query)
    LOGGER.info(type(result_timeseries_query))
    if type(result_timeseries_query) == str:
        result_timeseries_query = json.loads(result_timeseries_query)

    result_timeseries_query_obj = {}    
    if "data" in result_timeseries_query:
        result_timeseries_query_obj = result_timeseries_query["data"]
        if type(result_timeseries_query_obj) == str:
            result_timeseries_query_obj = json.loads(result_timeseries_query_obj)

    try:
        assert "hasSimulationMessageType" in result_timeseries_query_obj[0], \
            f'Simulation data query does not have expected output {result_timeseries_query_obj[0]}'
    except KeyError:
        assert (result_timeseries_query_obj != {}), \
            f'Simulation data query does not have expected output {result_timeseries_query}'
    LOGGER.info('Simulation data query has expected output')


@pytest.mark.xfail(strict=True, reason="sensor simulator requires updates for gridappsd-python")
def test_sensor_simulator_api():
    global result_sensor_query
    if type(result_sensor_query) == str:
        result_sensor_query = json.loads(result_sensor_query)
    result_timeseries_query_obj = {}    
    if "data" in result_timeseries_query:
        result_timeseries_query_obj = result_timeseries_query["data"]
        if type(result_timeseries_query_obj) == str:
            result_timeseries_query_obj = json.loads(result_timeseries_query_obj)
    try:
        assert "hasSimulationMessageType" in result_sensor_query["data"][0], \
            f'Sensor simulator data does not have expected output {result_timeseries_query_obj[0]}'
    except KeyError:
        assert (result_timeseries_query_obj != {}), \
            f'Sensor simulator data does not have expected output {result_sensor_query}'
    LOGGER.info('Query response received for  GridAPPS-D sensor simulator data from timeseries')
