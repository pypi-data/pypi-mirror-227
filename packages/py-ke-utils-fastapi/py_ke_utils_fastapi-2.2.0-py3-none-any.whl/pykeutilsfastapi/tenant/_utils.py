import logging
from urllib.parse import urlparse


def tenant_extractor(origin: str, x_tenant_id: str, default_tenant: str = 'public'):
    """
    Function to extract tenant from Origin/Header or assign default
    :param origin:
    :param x_tenant_id:
    :param default_tenant:
    :return:
    """
    subdomain = default_tenant
    logging.info("Starting to check subdomain.")

    hostname = urlparse(origin).hostname if isinstance(origin, str) else None

    if hostname and len(hostname.split(".")) > 1:
        subdomain = hostname.split(".")[0]

    if x_tenant_id:
        subdomain = x_tenant_id
    logging.info(f"Subdomain set: {subdomain}")

    return subdomain
