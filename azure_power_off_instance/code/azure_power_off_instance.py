import logging
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient

logger = logging.getLogger(__name__)


class AzurePowerOffInstanceBotPackage(object):

    def __init__(self, **kwargs):
        # kwargs will contain a reference to config object.
        # config object may also contain credentials provided by the user (if any)
        self.__config = kwargs.get("config")
        logger.info("Initializing my azure power off instance bot package")

    def shutdown(self):
        # Shutdown hook may be called before shutting down the bot code.
        # any cleanup can be performed.
        logger.info("Shutdown hook called")

    def bot_power_off_instance(self, **kwargs):
        # Subcription ID, Client ID, Tenant ID, and Client Secret should all later be passed through config
        azure_client_id = self.__config.get("azure_client_id")
        azure_tenant_id = self.__config.get("azure_tenant_id")
        azure_client_secret = self.__config.get("azure_client_secret")
        azure_credential = ClientSecretCredential(tenant_id=azure_tenant_id, client_id=azure_client_id,
                                                  client_secret=azure_client_secret)

        query_params = kwargs.get("query_params", {})
        resource_group_name = query_params.get("resource_group_name")
        vm_name = query_params.get("vm_name")

        azure_subscription_id = self.__config.get("azure_subscription_id")

        compute_management_cli = ComputeManagementClient(azure_credential, azure_subscription_id)

        # Stop vm
        compute_management_cli.virtual_machines.begin_power_off(resource_group_name=resource_group_name,
                                                                vm_name=vm_name)
        return None
