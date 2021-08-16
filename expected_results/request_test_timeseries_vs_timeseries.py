import json
import argparse
import random
from gridappsd import GOSS

goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

def start_test(simulationID1, simulationID2, start_time=1248156000,duration=60):
    goss = GOSS()
    goss.connect()

    test_id = str(random.getrandbits(32))
    testCfgAll = {
               "appId": "sample_app",
                "testId": test_id,
                "testOutput": False,
                "start_time":start_time,
                "duration":duration
               }

    testCfgAll['compareWithSimId'] = simulationID1 # 847461010 # 660948920
    testCfgAll['compareWithSimIdTwo'] = simulationID2 # 912453649
    testCfgAll['testType'] = 'timeseries_vs_timeseries'
    request = json.dumps(testCfgAll)

    # status = goss.get_response(test_input+str(test_id), request, timeout=60)
    status = goss.send(test_input+str(test_id), request)
    print(status)
    print('sent test status')
    return test_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id1", type=int, help="simulation id 1", required=False)
    parser.add_argument("-j", "--id2", type=int, help="simulation id 2", required=False)
    args = parser.parse_args()

    start_test(simulationID1=args.id1, simulationID2=args.id2)

# If opposite
# {'status': 'start'}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156014, 'indexTwo': 1248156014, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0.0', 'diffMrid': '6cb31129-662d-4859-bd68-61d219730e2f', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '0.0', 'actual': '1.0', 'diffMrid': 'ef1db14e-2cb3-43f5-b3d1-e5354e52f8ea', 'diffType': 'FORWARD', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156029, 'indexTwo': 1248156029, 'simulationTimestamp': 0, 'expected': '1.0', 'actual': '0.0', 'diffMrid': 'ef1db14e-2cb3-43f5-b3d1-e5354e52f8ea', 'diffType': 'REVERSE', 'match': False}
# {'object': '_939CA567-AA3D-4972-AABC-1D0AAF4859FE', 'attribute': 'ShuntCompensator.sections', 'indexOne': 1248156044, 'indexTwo': 1248156044, 'simulationTimestamp': 0, 'expected': 'NA', 'actual': '0.0', 'diffMrid': 'd6a33bce-9a95-4d5f-83c5-29ec6d568886', 'diffType': 'FORWARD', 'match': False}
# {'status': 'finish'}
# Exit
# Error count 4