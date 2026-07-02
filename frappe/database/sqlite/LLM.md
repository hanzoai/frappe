# Frappe → Hanzo Base/SQLite driver (per-org / per-tenant)

This is the hardened SQLite backend that lets **any** Frappe app (ERPNext,
Helpdesk, HR, CRM, …) persist to Hanzo **Base/SQLite**, one database file per
**org** (org == tenant == the IAM `owner`). A solid driver here means every
Frappe app becomes one-click deployable on the Hanzo platform.

## Files

| File | Role |
|------|------|
| `database.py` | `SQLiteDatabase` — connection, DDL/DML, transactions, sequence emulation, exception mapping. `get_db_path()` is org-aware. |
| `schema.py` | `SQLiteTable` — DocType → table schema-sync (create/alter/rename, index rebuild). |
| `setup_db.py` | new-site bootstrap; copies the `framework_sqlite.db` seed. |
| `tenant.py` | **per-org resolution + security allowlist** (this is the leverage). |
| `../../integrations/hanzo_iam.py` | hanzo.id OIDC SSO + org-context binding. |
| `test_tenant.py` | unit tests for the slug/stem/claim invariants. |

## One tenancy: org == tenant

There is exactly one tenant concept — the **org** (the IAM `owner` claim). A
Frappe "site" is just the app deployment, not a tenant. Two deployment shapes,
one code path:

* **Site-per-org** (`db_per_org` off, default): native Frappe multi-site. One org
  == one site == one `db/<db_name>.db`. Isolation is by site; the driver is
  untouched.
* **Shared-site, db-per-org** (`db_per_org: 1`): a single deployment serves many
  orgs. `get_db_path()` resolves the file from the org in request context:
  `sites/<site>/db/org-<slug>.db`. Provisioning an org = copying the framework
  seed to a new `org-<slug>.db`.

### Security (why `tenant.py` is its own unit)

The org slug is the only value between an IAM claim and a filesystem path. It is
allowlisted with `^[a-z0-9][a-z0-9-]{0,62}$` **before** touching `Path`:

* no traversal (`../`), no separators, no absolute paths, no NUL bytes;
* **lowercase-only** — macOS/APFS and NTFS are case-insensitive, so `Acme` and
  `acme` would otherwise fold onto one file and cross-read;
* fails **closed**: an invalid org raises `InvalidOrgError`, it never silently
  falls back to another org's database.

`get_connection(read_only)` builds `file:{path}?mode=ro`; because the org portion
is `[a-z0-9-]` only, no URI parameter injection is possible.

## IAM SSO (hanzo.id)

`frappe/integrations/hanzo_iam.py` binds the org from two authenticated seams,
both funnelled through `validate_org_slug`:

1. **Browser OIDC** — a Social Login Key (`get_social_login_key()`) points at
   hanzo.id; `stamp_org_on_login` pins the validated `owner` claim on the session.
2. **Gateway / M2M** — hanzoai/gateway authenticates and injects `X-IAM-Org-Id`;
   `set_org_from_request` validates it onto `frappe.local.org`.

Secrets (`iam_client_id`, `iam_client_secret`, JWKS) come from **KMS** into site
config — never hard-coded.

Wire into the deploy app's `hooks.py`:

```python
on_login = ["frappe.integrations.hanzo_iam.stamp_org_on_login"]
before_request = ["frappe.integrations.hanzo_iam.set_org_from_request"]
```

## Proven (real, no stubs)

A real Frappe site installed on this driver: **245 tables, 284 DocTypes** synced
through `SQLiteTable`. `frappe/database/sqlite/test_tenant.py` locks the
invariants. End-to-end recipe (reproducible):

```bash
# 1. venv + frappe (sqlite only; skip mysqlclient which is mariadb-only)
uv venv --python 3.14 .venv
uv pip install -p .venv/bin/python -r <(python -c "import tomllib;print(chr(10).join(x for x in tomllib.load(open('pyproject.toml','rb'))['project']['dependencies'] if not x.lower().startswith('mysqlclient')))")
uv pip install -p .venv/bin/python --no-deps -e .

# 2. real bench new-site on sqlite (installs all core DocTypes)
#    common_site_config.json: {"db_type":"sqlite"} ; site_config.json: {"db_type":"sqlite","db_name":"<org>"}
python -c 'import frappe; frappe.init("<org>", new_site=True); \
  from frappe.installer import _new_site; \
  _new_site(db_name="<org>", site="<org>", admin_password="…", db_type="sqlite", force=True)'

# 3. db_per_org site: provision org files by copying the installed seed, then
#    per request set frappe.local.org=<slug> and frappe.connect().
#    ToDo create/read/list in org A never appears in org B; verified at the raw
#    sqlite level (each org-<slug>.db holds only its own rows).
```

Verified: ORM CRUD (ToDo) on Base; `org 'acme' → org-acme.db`, `org 'globex' →
org-globex.db`; neither org reads the other's rows (ORM + raw file); slug
allowlist rejects traversal/absolute/uppercase/NUL/empty/dotfile/overlong.

Also fixed a real integration bug: `config.py` indexed `config["db_user"]`
(mariadb/postgres-only) which `KeyError`'d for any SQLite site whose config
omitted `db_name` → now `config.get("db_user")`.

## One-click deploy template (rides on `/v1/platform`)

Provisioning an org is a database-file copy + a config flag — the platform
control plane can do it with no schema migration:

1. **Image**: build ERPNext/Frappe on Base via arcd on-cluster
   (`ghcr.io/hanzoai/erp`), CGO not required (pure-Python + stdlib sqlite3).
2. **Deploy**: operator-native — a `services.hanzo.ai/erp` CR (never
   `kubectl set image`; that is reverted). Persist to `universe`.
3. **Storage**: `db_per_org: 1`; org dbs on the Base/SQLite persistence path
   (per-org SQLite, replicate → SeaweedFS per the operator persistence model).
4. **Onboarding an org** (`POST /v1/platform` once merged):
   `cp framework_seed.db sites/<site>/db/org-<slug>.db` → org is live. No global
   admin; IAM `owner` scopes every request via `X-IAM-Org-Id`.
5. **Auth**: hanzo.id OIDC (Social Login Key) + gateway identity header.

> Deploy is intentionally NOT executed here: it rides on `/v1/platform`, which
> is not yet merged, and the current cloud image carries unfixed `/v1/platform`
> crits. This branch lands the driver + SSO + tests + template only.
