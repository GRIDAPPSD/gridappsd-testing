import argparse
import json
import os
import time
import logging

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_expected_vs_running
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."
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
            # assert self._error_count == 7, f" For expected_vs_running expecting 7 non matching results. Received {self._error_count}"

            # os._exit(1)


def test():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-test_id", default=3258685887,
    #                     help="Simulation id to use for responses on the message bus.")
    #
    # opts = parser.parse_args()
    sim_id, test_id = request_test_expected_vs_running.start_test(testOutput=False)
    time.sleep(2)
    print('sent test request ' + test_id)

    # gapps = GridAPPSD(opts.test_id, address=utils.get_gridappsd_address(),
    #                   username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())
    username = "app_user"
    password = "1234App"
    gapps = GridAPPSD(username=username, password=password)
    gapps.connect()
    assert gapps.connected
    sl = SimpleListener(gapps, 1)
    print(test_output_topic+str(test_id))
    response = gapps.subscribe(test_output_topic+str(test_id), sl)
    print(response)

    with open('test_id_request_1.json', 'w') as f:
        json.dump({'sim_id1': sim_id}, f)

    finished=False
    while not finished:
        time.sleep(85)
        finished = True
    error_count = sl._error_count
    print(error_count)
    logging.info("Error count " + str(error_count))
    assert error_count == 17, f" For expected_vs_running expecting 12 non matching results. Received {error_count}"

if __name__ == "__main__":
    test()

    # {'status': 'start'}
    # {'object': '_0044ae64-1c72-4e81-b412-d7349ce267d3', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '374545.4981119089', 'actual': '54911.42414314939', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'angle', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '-5.066423674487563', 'actual': '21.91525592241816', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '2388.676720682955', 'actual': '23182.721945577698', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': '0da4890f-1eb5-4ef2-81e7-97ac4b15d191', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_CABBC3A1-66F5-4B9C-ACB9-476E2389D119', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': '0da4890f-1eb5-4ef2-81e7-97ac4b15d191', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_D6C44FF1-BC60-49D3-9438-DFAD1AED0A28', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': '0da4890f-1eb5-4ef2-81e7-97ac4b15d191', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_3DE55D2D-34D3-487E-9D6E-3A4DB1E38E47', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': '0da4890f-1eb5-4ef2-81e7-97ac4b15d191', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156016, 'indexTwo': 1248156016, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': '1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': '1', 'diffMrid': '3cf5c2fd-9bd1-4636-80d0-00d6a16d2318', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': '0', 'diffMrid': '3cf5c2fd-9bd1-4636-80d0-00d6a16d2318', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'status': 'finish'}

    ## Added reverse
    # {'status': 'start'}
    # {'object': '_0044ae64-1c72-4e81-b412-d7349ce267d3', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '374545.4981119089', 'actual': '54911.42414314939', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'angle', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '-5.066423674487563', 'actual': '21.91525592241816', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_000b01a1-8238-4372-95c0-82aad26ea311', 'attribute': 'magnitude', 'indexOne': 1248156002, 'indexTwo': 1248156002, 'simulationTimestamp': 0, 'expected': '2388.676720682955', 'actual': '23182.721945577698', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_CABBC3A1-66F5-4B9C-ACB9-476E2389D119', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_D6C44FF1-BC60-49D3-9438-DFAD1AED0A28', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_3DE55D2D-34D3-487E-9D6E-3A4DB1E38E47', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '1', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_CABBC3A1-66F5-4B9C-ACB9-476E2389D119', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '1', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_D6C44FF1-BC60-49D3-9438-DFAD1AED0A28', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '1', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_3DE55D2D-34D3-487E-9D6E-3A4DB1E38E47', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '1', 'diffMrid': 'a20d42c1-022f-4338-b25c-67a415803c95', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156016, 'indexTwo': 1248156016, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': '1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156016, 'indexTwo': 1248156016, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': '1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': '1', 'diffMrid': '6842fe8e-555b-464f-a52a-4c03783ae46a', 'diffType': 'FORWARD', 'match': False}
    # {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': '0', 'diffMrid': '6842fe8e-555b-464f-a52a-4c03783ae46a', 'diffType': 'REVERSE', 'match': False}
    # {'object': '_only_in_expected_MRID_time_does_not_matches', 'attribute': 'value', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': 'NA', 'diffType': 'NA', 'match': False}
    # 17