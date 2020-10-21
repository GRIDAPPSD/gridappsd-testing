import argparse
import json
import os
import time

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_timeseries_vs_timeseries
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."

class SimpleListener(object):
    """ A simple class to listen for the test results
    """
    global KEEP_LISTENING_FLAG

    def __init__(self, gridappsd_obj, test_id):
        """ Create
        """
        self._gapps = gridappsd_obj
        self._test_id = test_id

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

        # json_message = json.loads(message)
        # "{\"status\":\"start\"}")
        if 'status' in message and message['status'] == 'finish':
            print("Exit")
            os._exit(1)



def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-test_id", default=3258685887,
                        help="Simulation id to use for responses on the message bus.")
    opts = parser.parse_args()
    gapps = GridAPPSD(opts.test_id, address=utils.get_gridappsd_address(),
                      username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())
    sl = SimpleListener(gapps, opts.test_id)

    with open('test_id_request_1.json') as f:
        sim_id_dict = json.load(f)
    sim_id = sim_id_dict['sim_id1']
    with open('test_id_request_2.json') as f:
        sim_id_dict = json.load(f)
    sim_id2 = sim_id_dict['sim_id2']

    # sim_id = 1767860274
    # sim_id2 = 1564477893
    test_id2 = request_test_timeseries_vs_timeseries.start_test(sim_id, sim_id2)
    print('simid ' + str(sim_id))
    print('sent test request ' + test_id2)
    print(test_output_topic + str(test_id2))

    response = gapps.subscribe(test_output_topic+str(test_id2), sl)
    print(response)

    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    _main()

