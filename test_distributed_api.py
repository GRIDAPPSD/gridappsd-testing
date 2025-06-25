import ast
from contextlib import contextmanager
import json
import logging
import os
from time import sleep, time
import sys
import pytest
from dictdiffer import diff 

from gridappsd import GridAPPSD
from gridappsd.simulation import Simulation
from gridappsd_docker import docker_up, docker_down
from gridappsd import GridAPPSD, topics as t



LOGGER = logging.getLogger(__name__)

@pytest.mark.parametrize("model_name, model_id", [
    ("ieee123", "C1C3E687-6FFD-C753-582B-632A27E28507"),
    ("ieee13nodeckt", "49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"),
    ("final9500node", "EE71F6C9-56F0-4167-A14E-7F4C71F10EAA"),
])
def test_symbols_file_output(gridappsd_client, model_name, model_id):

	result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files{os.path.sep}distributed_api{os.path.sep}{model_name}.json")

	gapps = gridappsd_client
    
	query = {
				"requestType":"GET_DISTRIBUTED_AREAS", 
				"mRID": model_id
			}

	response = gapps.get_response(t.REQUEST_DATA+'.cimtopology' ,query, timeout=300)
	
	with open(result_file, 'r') as fl:		
		result = json.load(fl)
		

	difference = diff(response["data"], result)
	print(f'DIFFERENCES for :{model_name}')
	print(list(difference))

	assert len(list(difference))==0
	