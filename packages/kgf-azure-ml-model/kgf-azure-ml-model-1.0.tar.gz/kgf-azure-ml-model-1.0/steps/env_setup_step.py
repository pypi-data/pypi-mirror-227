import argparse
from azureml.core import Workspace, Experiment, Environment, Dataset
import os
from azureml.core.compute import AmlCompute
import sys
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from utils  import StepsUtils

# Add the path of the parent directory to the Python path
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)

from constants import ENVIRONMENT_NAME, COMPUTE_TARGET_NAME

def evaluate(ws, data_path):
    # Your evaluation logic here
    # Load trained model, evaluate on data, etc.
    # Define the compute target name
    compute_target_name = COMPUTE_TARGET_NAME
    try:
        # Retrieve the AmlCompute target
        compute_target = AmlCompute(workspace=ws, name=compute_target_name)
    except Exception:
        print(f"Compute target '{compute_target_name}' not found. Creating new compute target...")
        # Define configuration for new AmlCompute target
        provisioning_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2', min_nodes=0, max_nodes=1)
        # Create the compute target
        compute_target = AmlCompute.create(workspace=ws, name=compute_target_name, provisioning_configuration=provisioning_config)

        compute_target.wait_for_completion(show_output=True)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, help='Path to data')
    #parser.add_argument('--workspace', type=str, help='Workspace object')
    args = parser.parse_args()

    data_path = args.data_path
    ws = StepsUtils.get_workspace()
    print(f"Input workspace name: {ws.name}")
    evaluate(ws, data_path)
