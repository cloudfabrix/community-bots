import logging
from azure.identity import ClientSecretCredential
from azure.mgmt.consumption import ConsumptionManagementClient
import json

logger = logging.getLogger(__name__)


class AzureUsageBotPackage(object):

    def __init__(self, **kwargs):
        # kwargs will contain a reference to config object.
        # config object may also contain credentials provided by the user (if any)
        self.__config = kwargs.get("config")
        logger.info("Initializing my azure usage bot package")

    def shutdown(self):
        # Shutdown hook may be called before shutting down the bot code.
        # any cleanup can be performed.
        logger.info("Shutdown hook called")

    def bot_usage_details(self, **kwargs):
        azure_client_id = self.__config.get("azure_client_id")
        azure_tenant_id = self.__config.get("azure_tenant_id")
        azure_client_secret = self.__config.get("azure_client_secret")
        azure_credential = ClientSecretCredential(tenant_id=azure_tenant_id, client_id=azure_client_id,
                                                  client_secret=azure_client_secret)

        query_params = kwargs.get("query_params", {})
        billing_period_name = query_params.get("billing_period_name")

        azure_subscription_id = self.__config.get("azure_subscription_id")
        scope = "/subscriptions/" + azure_subscription_id + "/providers/Microsoft.Billing/billingPeriods/" + billing_period_name

        consumption_management_cli = ConsumptionManagementClient(azure_credential, azure_subscription_id)

        consumption_profile = consumption_management_cli.usage_details.list(scope=scope)
        usage_details = []
        for usage_detail in consumption_profile:
            row = {
                'billing_account_id': usage_detail.billing_account_id,
                'ID': usage_detail.id,
                'cost_in_usd': usage_detail.cost_in_usd,
                'service_family': usage_detail.service_family,
                'subscription_name':usage_detail.subscription_name,
                'pricing_model': usage_detail.pricing_model,
                'quantity': usage_detail.quantity,
                'billing_account_name': usage_detail.billing_account_name
            }
            usage_details.append(row)


        return usage_details