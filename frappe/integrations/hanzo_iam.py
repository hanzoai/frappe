"""Hanzo IAM (hanzo.id / Casdoor) single-sign-on + org-context binding for Frappe.

Two seams, one tenant identity (the IAM ``owner`` == the org == the tenant):

1. **Browser OIDC login** via a Social Login Key pointed at hanzo.id. After the
   OAuth callback, ``stamp_org_on_login`` reads the validated ``owner`` claim from
   the userinfo and pins it on the session, so subsequent requests route to the
   org's database.

2. **Gateway / M2M requests** where hanzoai/gateway has already authenticated the
   caller and injected the trusted identity header ``X-IAM-Org-Id`` (the same
   header the rest of the platform uses). ``set_org_from_request`` reads it and
   pins ``frappe.local.org``.

Both paths funnel the org through ``tenant.validate_org_slug`` before it can reach
the database driver, so a forged or malformed org can never select another
tenant's file. Secrets (client id/secret, JWKS) live in KMS and are surfaced to
the site as config — never hard-coded here.
"""

import frappe
from frappe.database.sqlite.tenant import InvalidOrgError, validate_org_slug

# Trusted, gateway-injected identity header. It is only honoured when the request
# arrives through the authenticated gateway; a direct client cannot set it because
# the gateway strips inbound copies (defense in depth lives at the ingress).
ORG_HEADER = "X-IAM-Org-Id"

# Claims that may carry the org/tenant, in priority order. `owner` is Casdoor's
# organization claim; `org`/`organization` are OIDC-standard fallbacks.
ORG_CLAIMS = ("owner", "org", "organization")


def get_social_login_key() -> dict:
	"""Return the Social Login Key definition for hanzo.id (OIDC).

	Endpoints derive from ``iam_base_url`` in site config (default hanzo.id).
	client_id / client_secret are pulled from site config, which is populated from
	KMS at deploy time — this function never embeds a secret.
	"""
	base = (frappe.conf.get("iam_base_url") or "https://hanzo.id").rstrip("/")
	return {
		"doctype": "Social Login Key",
		"enable_social_login": 1,
		"social_login_provider": "Custom",
		"provider_name": "Hanzo IAM",
		"client_id": frappe.conf.get("iam_client_id"),
		"client_secret": frappe.conf.get("iam_client_secret"),
		"base_url": base,
		"custom_base_url": 1,
		"authorize_url": "/login/oauth/authorize",
		"access_token_url": "/api/login/oauth/access_token",
		"api_endpoint": "/api/userinfo",
		"redirect_url": "/api/method/frappe.integrations.oauth2_logins.custom/hanzo_iam",
		"auth_url_data": '{"scope": "openid profile email"}',
	}


def extract_org_from_claims(claims: dict) -> str | None:
	"""Return the validated org slug from an IAM userinfo/token claim set, or None.

	Raises ``InvalidOrgError`` if a claim is present but not a safe slug — we fail
	closed rather than fall through to an unscoped database.
	"""
	if not isinstance(claims, dict):
		return None
	for key in ORG_CLAIMS:
		value = claims.get(key)
		if value:
			return validate_org_slug(value)
	return None


def stamp_org_on_login(login_manager=None) -> None:
	"""``on_login`` hook: persist the org from the IAM userinfo onto the session.

	The OAuth layer stashes the raw userinfo on ``frappe.flags.hanzo_iam_userinfo``;
	we extract + validate the org and store it on the session so ``tenant.resolve_org``
	picks it up for every later request in the session.
	"""
	claims = frappe.flags.get("hanzo_iam_userinfo")
	org = extract_org_from_claims(claims) if claims else None
	if org and getattr(frappe.local, "session", None):
		frappe.local.session.data["org"] = org
		frappe.local.org = org


def set_org_from_request() -> None:
	"""Request hook: bind ``frappe.local.org`` from the gateway identity header.

	Runs before any database access. If the header is absent the org stays unset
	and the driver uses the base site db (single-tenant / system contexts). A
	malformed header raises and the request is refused — it never silently
	targets the wrong tenant.
	"""
	value = frappe.get_request_header(ORG_HEADER)
	if not value:
		return
	try:
		frappe.local.org = validate_org_slug(value)
	except InvalidOrgError:
		frappe.throw(f"Invalid {ORG_HEADER}", exc=frappe.PermissionError)
