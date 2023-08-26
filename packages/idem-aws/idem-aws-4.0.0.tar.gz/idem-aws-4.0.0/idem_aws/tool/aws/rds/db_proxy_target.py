"""Utility functions for Rds Db Proxy Targets."""
from typing import Any
from typing import Dict


async def convert_raw_resource_to_present_async(
    hub,
    ctx,
    idem_resource_name: str,
    resource_id: str,
    raw_resource: dict,
    db_proxy_name: str,
    target_group_name: str,
) -> Dict[str, Any]:
    r"""
    Convert raw resource of db_proxy_target type into present format.

    """

    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "db_proxy_name": db_proxy_name,
        "target_group_name": target_group_name,
    }

    resource_parameters = {
        "TargetArn": "target_arn",
        "Endpoint": "endpoint",
        "TrackedClusterId": "tracked_cluster_id",
        "RdsResourceId": "rds_resource_id",
        "Port": "port",
        "Type": "type",
        "Role": "role",
        "TargetHealth": "target_health",
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


def create_resource_id(hub, raw_resource, db_proxy_name, target_group_name):
    return (
        db_proxy_name
        + "/"
        + target_group_name
        + "/"
        + raw_resource.get("Type")
        + "/"
        + raw_resource.get("RdsResourceId")
    )
