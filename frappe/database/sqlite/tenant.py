"""Per-org (== per-tenant) database resolution for the SQLite / Hanzo Base driver.

One tenancy concept: the **org** (the IAM ``owner`` claim). There is no second
tenant abstraction — a Frappe "site" is just the app deployment, and the org is
the storage partition inside it.

Two deployment shapes, one code path:

* ``db_per_org`` **off** (default): native Frappe multi-site. One org == one site
  == one ``db/<db_name>.db`` file. The driver is untouched; isolation is by site.
* ``db_per_org`` **on**: a single deployment serves many orgs. The driver keys the
  database file by the org resolved from request context — ``db/org-<slug>.db`` —
  so provisioning an org is a one-file copy of the framework seed.

Security note (this is the whole reason this module exists as its own unit):
the org slug is the ONLY value standing between an attacker-controlled IAM claim
and a filesystem path. It is validated with a strict allowlist before it ever
touches ``Path``. Anything that is not ``^[a-z0-9][a-z0-9-]{0,62}$`` is refused —
no path traversal, no absolute paths, no NUL bytes, and (critically, because
macOS/APFS is case-insensitive by default) no uppercase, so ``Acme`` and ``acme``
can never fold onto the same file and cross-read each other's data. Validation
fails closed: an invalid org raises rather than silently falling back to another
org's database.
"""

import re

import frappe

# Strict allowlist. Lowercase-only guards against case-insensitive-FS collisions.
# Length capped at 63 (leading char + up to 62 more) — DNS-label sized, matches
# IAM org-slug conventions and keeps the filename bounded.
ORG_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")

# Prefix isolates per-org files from the base/framework site db (`<db_name>.db`),
# so an org can never be named to shadow the deployment's own database file.
ORG_DB_PREFIX = "org-"


class InvalidOrgError(frappe.ValidationError):
	"""Raised when an org identifier fails the strict slug allowlist."""


def validate_org_slug(org: str) -> str:
	"""Return ``org`` unchanged iff it is a safe slug, else raise ``InvalidOrgError``.

	No normalization is performed on purpose: silently lower-casing or stripping
	would let two distinct claims map to one database. The caller must present an
	already-canonical slug (IAM emits lowercase org slugs); anything else is a
	programming/authn error and is refused.
	"""
	if not isinstance(org, str) or not ORG_SLUG_RE.fullmatch(org):
		raise InvalidOrgError(f"Invalid org identifier for per-org database: {org!r}")
	return org


def resolve_org() -> str | None:
	"""Resolve the current tenant org from request context, or ``None``.

	Resolution order (first hit wins):

	1. ``frappe.local.org`` — set explicitly by the IAM/OAuth auth hook from the
	   validated ``owner`` claim (see ``frappe.integrations.hanzo_iam``).
	2. ``frappe.local.session.data.org`` — carried on the session so it survives
	   across a logged-in user's requests without re-parsing the token.

	Returns ``None`` when no org is in context (installers, migrations, background
	jobs, single-tenant deployments) so the caller falls back to the base site db.
	"""
	org = getattr(frappe.local, "org", None)
	if not org:
		session = getattr(frappe.local, "session", None)
		if session:
			data = getattr(session, "data", None) or {}
			org = data.get("org")
	if not org:
		return None
	return validate_org_slug(org)


def resolve_db_stem(default_db_name: str) -> str:
	"""Return the on-disk db filename stem (without ``.db``) for this request.

	Base site db unless ``db_per_org`` is enabled AND an org is in context, in
	which case the org-partitioned stem ``org-<slug>`` is returned.
	"""
	if not frappe.conf.get("db_per_org"):
		return default_db_name
	org = resolve_org()
	if not org:
		return default_db_name
	return f"{ORG_DB_PREFIX}{org}"
