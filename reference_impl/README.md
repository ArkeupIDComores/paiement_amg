Reference Implementation – HOLO Payment Flow (Django)

Overview
- Minimal Django app showing HOLO payment initiation page and backend endpoints.
- Endpoints:
  - Web: `/payments/initier-paiement`, `/payment/holo/accept`, `/payment/holo/decline`, `/payment/holo/cancel`
  - API: `/api/payment/holo/initiate`, `/api/payment/holo/notify`
- Uses SQLite for demo and simple logging for double journalisation.

Security & Reliability
- HTTPS required in production; dev uses localhost for preview.
- IP whitelist for Notify (e.g., 3.6.76.175 – adjust to MSO list).
- Signature/HMAC verification if provided by HOLO.
- Idempotence by `purchaseref` + `ref_trans`.
- Timeout HOLO: 5 minutes; retry logic server-side for transient errors.
- Double validation: notification + optional verification (placeholder).

Demo Steps
1) User selects HOLO → openIMIS initiates payment.
2) Server obtains `sessionid` from HOLO and renders auto-submit form.
3) Page auto-posts to HOLO; user completes PIN + OTP.
4) HOLO redirects to Accept/Decline/Cancel page (informational).
5) HOLO sends Notify to backend → payment recorded → rights activated.

Run Locally
1) Install Python 3.10+.
2) `pip install -r reference_impl/services/requirements.txt`
3) `cd reference_impl/services`
4) `python manage.py migrate`
5) `python manage.py runserver` (uses `holo_site.settings` → dev by default)
6) Open `http://localhost:8000/payments/initier-paiement`.

Settings Organization
- `holo_site/settings/base.py`: common base settings
- `holo_site/settings/dev.py`: development overrides (DEBUG=True, permissive hosts)
- `holo_site/settings/prod.py`: production overrides (DEBUG=False, restricted hosts)
- Default import: `holo_site.settings` → loads dev via `holo_site/settings/__init__.py`.

Switch to production settings:
```
set DJANGO_SETTINGS_MODULE=holo_site.settings.prod
python manage.py runserver 0.0.0.0:8000
```

Configuration
- Set environment variables or edit `holo_site/settings/base.py`:
  - `HOLO_BASE_URL`: e.g. `https://<your-holo-host>`
  - `HOLO_ONLINE_ENDPOINT`: default `/online/online.php`
  - `HOLO_MERCHANT_ID`: e.g. `2449462108576891`
  - `CALLBACK_DOMAIN`: e.g. `https://dev.amg.km`
- If `HOLO_BASE_URL` is left as placeholder (`holourl`), the auto-submit page will warn and avoid auto-post.

Examples (PowerShell)
```
# Development (default)
setx HOLO_BASE_URL "https://26900.tagpay.fr"
setx HOLO_ONLINE_ENDPOINT "/online/online.php"
setx HOLO_MERCHANT_ID "2449462108576891"
setx CALLBACK_DOMAIN "https://dev.amg.km"

# Run dev
python manage.py runserver 0.0.0.0:8000

# Run prod
setx DJANGO_SETTINGS_MODULE "holo_site.settings.prod"
python manage.py runserver 0.0.0.0:8000
```

Examples
- Example HOLO session request (spec): `GET https://holoUrl/online/online.php?merchantid=2449462108576891` → returns a string; session id is `substr(response, 3)`.
- Example Notify payload:
  ```json
  {
    "ref_trans": "HTAG-2025-00004567",
    "purchaseref": "AMG-INV-2025-000123",
    "merchantid": "2449462108576891",
    "amount_paid": 5000,
    "currency": 174,
    "status": "success",
    "timestamp": "2025-11-20T14:05:12Z",
    "signature": "hmac-sha256-hex"
  }
  ```