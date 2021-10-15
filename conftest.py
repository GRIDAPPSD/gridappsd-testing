from copy import deepcopy
from pathlib import Path
from py.xml import html

import logging
import os
import sys

import pytest

from gridappsd import GridAPPSD, GOSS
from gridappsd.docker_handler import run_dependency_containers, run_gridappsd_container, Containers

levels = dict(
    CRITICAL=50,
    FATAL=50,
    ERROR=40,
    WARNING=30,
    WARN=30,
    INFO=20,
    DEBUG=10,
    NOTSET=0
)

# Get string representation of the log level passed
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Make sure the level passed is one of the valid levels.
if LOG_LEVEL not in levels.keys():
    raise AttributeError("Invalid LOG_LEVEL environmental variable set.")

# Set the numeric version of log level to pass to the basicConfig function
LOG_LEVEL = levels[LOG_LEVEL]

logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL,
                    format="%(asctime)s|%(levelname)s|%(name)s|%(message)s")
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
logging.getLogger("docker.utils.config").setLevel(logging.INFO)
logging.getLogger("docker.auth").setLevel(logging.INFO)


STOP_CONTAINER_AFTER_TEST = os.environ.get('GRIDAPPSD_STOP_CONTAINERS_AFTER_TESTS', True)


@pytest.fixture(scope="module")
def docker_dependencies():
    print("Docker dependencies")
    # Containers.reset_all_containers()

    with run_dependency_containers(stop_after=STOP_CONTAINER_AFTER_TEST) as dep:
        yield dep
    print("Cleanup docker dependencies")

@pytest.fixture
def gridappsd_client(request, docker_dependencies):
    with run_gridappsd_container(stop_after=STOP_CONTAINER_AFTER_TEST):
        gappsd = GridAPPSD()
        gappsd.connect()
        assert gappsd.connected
        models = gappsd.query_model_names()
        assert models is not None
        if request.cls is not None:
            request.cls.gridappsd_client = gappsd
        yield gappsd

        gappsd.disconnect()

@pytest.fixture
def goss_client(docker_dependencies):
    with run_gridappsd_container(stop_after=STOP_CONTAINER_AFTER_TEST):
        goss = GOSS()
        goss.connect()
        assert goss.connected

        yield goss

@pytest.fixture(scope="module")
def gridappsd_client_module(docker_dependencies):
    with run_gridappsd_container(True):
        gappsd = GridAPPSD()
        gappsd.connect()
        assert gappsd.connected

        yield gappsd

        gappsd.disconnect()


# USED AS EXAMPLES COPIED FROM gridappsd-sensor-simulator
#
# @pytest.fixture(scope="module")
# def gridappsd_client_include_as_service_no_cleanup(docker_dependencies):
#
#     config = deepcopy(DEFAULT_GRIDAPPSD_DOCKER_CONFIG)
#
#     config['gridappsd']['volumes'][str(LOCAL_MOUNT_POINT_FOR_SERVICE)] = dict(
#         bind=str(SERVICE_MOUNT_POINT),
#         mode="rw")
#
#     # from pprint import pprint
#     # pprint(config['gridappsd'])
#     with run_containers(config, stop_after=False) as containers:
#         containers.wait_for_log_pattern("gridappsd", "MYSQL")
#
#         gappsd = GridAPPSD()
#         gappsd.connect()
#         assert gappsd.connected
#
#         yield gappsd
#
#         gappsd.disconnect()
#
#
# @pytest.fixture
# def gridappsd_client_include_as_service(docker_dependencies):
#
#     config = deepcopy(DEFAULT_GRIDAPPSD_DOCKER_CONFIG)
#
#     config['gridappsd']['volumes'][str(LOCAL_MOUNT_POINT_FOR_SERVICE)] = dict(
#         bind=str(SERVICE_MOUNT_POINT),
#         mode="rw")
#
#     local_config = LOCAL_MOUNT_POINT_FOR_SERVICE.joinpath("sensor_simulator.config")
#     config['gridappsd']['volumes'][str(local_config)] = dict(
#         bind=str(CONFIG_MOUNT_POINT),
#         mode="rw")
#
#     # from pprint import pprint
#     # pprint(config['gridappsd'])
#     with run_containers(config, stop_after=STOP_AFTER_FIXTURE) as containers:
#         containers.wait_for_log_pattern("gridappsd", "MYSQL")
#
#         gappsd = GridAPPSD()
#         gappsd.connect()
#         assert gappsd.connected
#
#         yield gappsd
#
#         gappsd.disconnect()


# Add description column to the html report and fill with the __doc__ text

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Description"))


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
