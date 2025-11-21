import hmac
import hashlib
from django.conf import settings


def verify_signature(payload: bytes, provided_signature: str) -> bool:
    if not provided_signature:
        return False
    secret = settings.SIGNING_SECRET.encode('utf-8')
    computed = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    # Also accept base64 if HOLO provides that format
    return provided_signature == computed


def is_ip_whitelisted(remote_addr: str) -> bool:
    allowed = settings.IP_WHITELIST
    return remote_addr in allowed