import hmac
import hashlib
from core.models import ModuleConfiguration
from django.apps import apps
from .apps import DEFAULT_CONFIG, MODULE_NAME

cfg = ModuleConfiguration.get_or_default(MODULE_NAME,DEFAULT_CONFIG)
SIGNING_SECRET = cfg["SIGNING_SECRET"]
IP_WHITELIST = cfg["IP_WHITELIST"]

def verify_signature(payload: bytes, provided_signature: str) -> bool:
    if not provided_signature:
        return False
    secret = SIGNING_SECRET.encode('utf-8')
    computed = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    # Also accept base64 if HOLO provides that format
    return provided_signature == computed


def is_ip_whitelisted(remote_addr: str) -> bool:
    allowed = IP_WHITELIST
    return remote_addr in allowed