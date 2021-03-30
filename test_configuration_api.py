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
    ("ieee123", "_C1C3E687-6FFD-C753-582B-632A27E28507"),
    ("ieee123pv", "_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D"),
    ("ieee123transactive", "_503D6E20-F499-4CC7-8051-971E23D0BF79"),
    ("ieee13nodeckt", "_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"),
    ("ieee13nodecktassets", "_5B816B93-7A5F-B64C-8460-47C17D6E4B0F"),
    ("test9500new", "_AAE94E4A-2465-6F5E-37B1-3E72183A4E44"),
])
def test_symbols_file_output(gridappsd_client, model_name, model_id):

	result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files/configuration_api/Gridlabd_symbol_files/{model_name}.json")

	gapps = gridappsd_client
    
	query = {
            "configurationType": "GridLAB-D Symbols",
            "parameters": {
    			"model_id": model_id
  						  }
			}

	response = gapps.get_response(t.CONFIG ,query, timeout=300)
	
	with open(result_file, 'r') as fl:
		result = json.load(fl)
	

	difference = diff(response["data"], result)

	print(list(difference))

	assert len(list(difference))==0

@pytest.mark.parametrize("model_name, model_id", [
    ("ieee123", "_C1C3E687-6FFD-C753-582B-632A27E28507"),
    ("ieee123pv", "_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D"),
    ("ieee123transactive", "_503D6E20-F499-4CC7-8051-971E23D0BF79"),
    ("ieee13nodeckt", "_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"),
    ("ieee13nodecktassets", "_5B816B93-7A5F-B64C-8460-47C17D6E4B0F"),
    ("test9500new", "_AAE94E4A-2465-6F5E-37B1-3E72183A4E44"),
])
def test_CIM_dictionary_file_output(gridappsd_client, model_name, model_id):

    result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files/configuration_api/CIM_dictionary_file/{model_name}.json")

    gapps = gridappsd_client
    
    query = {
            "configurationType": "CIM Dictionary",
            "parameters": {
                "model_id": model_id
                          }
            }

    response = gapps.get_response(t.CONFIG ,query, timeout=300)
    
    with open(result_file, 'r') as fl:
        result = json.load(fl)
    

    difference = diff(response["data"], result)

    #print(list(difference))

    assert len(list(difference))==0


# @pytest.mark.parametrize("model_name, model_id", [
#     ("ieee123", "_C1C3E687-6FFD-C753-582B-632A27E28507"),
#     # ("ieee123pv", "_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D"),
#     # ("ieee123transactive", "_503D6E20-F499-4CC7-8051-971E23D0BF79"),
#     # ("ieee13nodeckt", "_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"),
#     # ("ieee13nodecktassets", "_5B816B93-7A5F-B64C-8460-47C17D6E4B0F"),
#     # ("test9500new", "_AAE94E4A-2465-6F5E-37B1-3E72183A4E44"),
# ])
# def test_base_file_output(gridappsd_client, model_name, model_id):

# 	result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files/configuration_api/Gridlabd_base_files/{model_name}.json")

# 	gapps = gridappsd_client
    
# 	query = {
#             "configurationType": "GridLAB-D Base GLM",
#             "parameters": {
#                 "i_fraction": "1.0",
#                 "z_fraction": "0.0",
#                 "model_id": model_id,
#                 "load_scaling_factor": "1.0",
#                 "schedule_name": "ieeezipload",
#                 "p_fraction": "0.0"
#                           }
#             }

# 	# response = gapps.get_response(t.CONFIG ,query, timeout=300)

# 	# print(response)
	
# 	with open(result_file, 'r') as fl:
# 	   result = json.load(fl)
#         result = json.loads(result)
# 	print(result, type(result))

	# difference = diff(response["data"], result)

	# print(list(difference))

	# assert len(list(difference))==0
	