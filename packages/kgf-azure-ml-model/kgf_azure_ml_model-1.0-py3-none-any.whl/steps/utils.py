from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

class StepsUtils:

    def __init__(self) -> None:
        pass


    def get_workspace():
        
        # Define authentication details
        subscription_id = 'bcd7f22c-e997-42c9-9c6a-74ffa3781562'
        resource_group = 'kgf-mlw-rg'
        workspace_name = 'kgf-mlw'
        service_principal_id = '6f9fbc0f-c37c-4654-8a76-07989c5b7719'
        service_principal_password = 'U_58Q~Q~P_M6UmP0hgHylKCi.qJ6HTu83QgBXc9p'
        tenant_id = '592c8f86-65e2-4700-bf7a-c6907488aee7'


        # Authenticate using service principal
        ws = None
        try:
            ws = Workspace(subscription_id, resource_group, workspace_name,
                        auth=ServicePrincipalAuthentication(
                            tenant_id=tenant_id,
                            service_principal_id=service_principal_id,
                            service_principal_password=service_principal_password))
            print("Authenticated successfully!")
        except Exception as e:
            print("Authentication failed:", e)

        return ws