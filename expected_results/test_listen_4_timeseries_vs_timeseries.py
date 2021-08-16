import time
import logging
import json

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_timeseries_vs_timeseries
import request_test_running
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."

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
            print(self._error_count == 0)


def test():
    gapps = GridAPPSD()
    gapps.connect()
    logging.info('Starting')
    sl = SimpleListener(gapps, 1)
    sim_id = request_test_running.start_test('sample_app')
    time.sleep(90)
    print('sent run request ' + sim_id)

    sim_id2 = request_test_running.start_test('sample_app')
    # sim_id2 = request_test_running.start_test('sample_app_opp')
    time.sleep(90)
    print('sent run request ' + sim_id)
    # sim_id='1290306857'
    # sim_id2='156135802'
    with open('test_id_request_4.json', 'w') as f:
        json.dump({'sim_id1': sim_id, 'sim_id2':sim_id2}, f)

    test_id2 = request_test_timeseries_vs_timeseries.start_test(sim_id, sim_id2)
    print('simid ' + str(sim_id))
    print('sent test request ' + test_id2)
    print(test_output_topic + str(test_id2))

    response = gapps.subscribe(test_output_topic+str(test_id2), sl)
    print(response)
    time.sleep(2)

    finished = False
    while not finished:
        time.sleep(120)
        finished = True

    gapps.disconnect()

    error_count = sl._error_count
    print(error_count)
    assert error_count == 0, f" For timeseries_vs_timeseries expecting 0 non matching results. Received {error_count}"

if __name__ == "__main__":
    test()

# {'status': 'start'}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': '87ac3700-0e81-4f35-8062-6a9aa4f762bc', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': '87ac3700-0e81-4f35-8062-6a9aa4f762bc', 'diffType': 'REVERSE', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': '0.0', 'diffMrid': '5c7bbd6e-790d-4abe-9804-dd59840a1ce3', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': '1.0', 'diffMrid': '5c7bbd6e-790d-4abe-9804-dd59840a1ce3', 'diffType': 'REVERSE', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156044, 'indexTwo': 1248156044, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': 'NA', 'diffMrid': '2bf77715-7c0f-48cb-8982-b848f057ac15', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156044, 'indexTwo': 1248156044, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': 'NA', 'diffMrid': '2bf77715-7c0f-48cb-8982-b848f057ac15', 'diffType': 'REVERSE', 'match': False}
# {'status': 'finish'}
# Exit
# Error count 6
