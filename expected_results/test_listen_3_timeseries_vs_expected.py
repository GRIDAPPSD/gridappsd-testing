import time
import logging
import random
import pytest

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_expected_vs_timeseries
import request_test_running
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."
# LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename=__name__+'.log', level=logging.INFO)

class SimpleListener(object):
    """ A simple class to listen for the test results
    """
    def __init__(self, gridappsd_obj, test_id):
        """ Create
        """
        self._gapps = gridappsd_obj
        self._test_id = test_id
        self._error_count = 0

    def on_message(self, headers, message):
        """ Handle incoming messages on the simulation_output_topic for the simulation_id
        Parameters
        ----------
        headers: dict
            A dictionary of headers that could be used to determine topic of origin and
            other attributes.
        message: object
            A data structure following the protocol defined in the message structure
            of ``GridAPPSD``.  Most message payloads will be serialized dictionaries, but that is
            not a requirement.
        """
        print(message)
        if 'status' in message and (message['status'] == 'finish' or message['status'] == 'start'):
            pass
        else:
            self._error_count+=1
        # json_message = json.loads(message)
        # "{\"status\":\"start\"}")
        if 'status' in message and message['status'] == 'finish':
            print("Exit")
            print("Error count " + str(self._error_count))
            print(self._error_count == 7)  # 5?

def test():
    username = "app_user"
    password = "1234App"
    gapps = GridAPPSD(username=username, password=password)
    gapps.connect()
    logging.info('Starting')
    sl = SimpleListener(gapps, 1)

    sim_id = request_test_running.start_test()
    time.sleep(65)
    print('sent run request ' + sim_id)

    # import json
    # with open('test_id_request_1.json') as f:
    #     sim_id = json.load(f)
    # sim_id = sim_id['sim_id1']
    # sim_id='2105518764'
    test_id2 = request_test_expected_vs_timeseries.start_test(simulationID=sim_id,
                                                              app_name='sample_app',
                                                              testOutput=False)

    response = gapps.subscribe(test_output_topic + str(test_id2), sl)
    print(response)
    print(type(test_id2))
    print('simid ' + str(sim_id))
    print('sent test request ' + str(test_id2))
    print(test_output_topic + str(test_id2))

    logging.info("Start waiting")
    finished = False
    while not finished:
        time.sleep(5)
        finished = True
    error_count = sl._error_count
    print(error_count)
    logging.info("Error count " + str(error_count))
    assert error_count == 11, f" For expected_vs_timeseries expecting 11 non matching results. Received {error_count}"

if __name__ == "__main__":
    test()

#  {'status': 'start'}
# {'object': '_0044ae64-1c72-4e81-b412-d7349ce267d3', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '374545.4981119089', 'actual': '54911.42414314939', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'angle', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '-5.066423674487563', 'actual': '21.91525592241816', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '2388.676720682955', 'actual': '23182.721945577698', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156016, 'indexTwo': 1248156016, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': '1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0.0', 'diffMrid': '07e75eb1-d72b-4e6b-8aae-fe7cef810001', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': '1.0', 'diffMrid': 'fca0f5c2-b4fa-49ec-8a73-278cc541af03', 'diffType': 'FORWARD', 'match': False}
# {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': '0.0', 'diffMrid': 'fca0f5c2-b4fa-49ec-8a73-278cc541af03', 'diffType': 'REVERSE', 'match': False}
# {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'status': 'finish'}
# Exit
# Error count 9

#
# {'status': 'start'}
# {'object': '_0044ae64-1c72-4e81-b412-d7349ce267d3', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '374545.4981119089', 'actual': '54911.42414314939', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'angle', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '-5.066423674487563', 'actual': '21.91525592241816', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '2388.676720682955', 'actual': '23182.721945577698', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156016, 'indexTwo': 1248156016, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': '1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156016, 'indexTwo': 1248156016, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': '1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4', 'diffType': 'REVERSE', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0.0', 'diffMrid': 'ddfc2e02-fea7-4d5f-a2a7-d855c750779b', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '1.0', 'diffMrid': 'ddfc2e02-fea7-4d5f-a2a7-d855c750779b', 'diffType': 'REVERSE', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': '1.0', 'diffMrid': 'f7167aa0-8e04-4a67-ac00-65ebc19d533b', 'diffType': 'FORWARD', 'match': False}
# {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': '0.0', 'diffMrid': 'f7167aa0-8e04-4a67-ac00-65ebc19d533b', 'diffType': 'REVERSE', 'match': False}
# {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
# {'status': 'finish'}
# Exit
# Error count 11