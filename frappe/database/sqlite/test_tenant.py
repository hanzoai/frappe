"""Tests for the per-org (per-tenant) SQLite/Base driver resolution and the
Hanzo IAM org-claim binding. These are dependency-light (no live site needed for
the slug/stem/claim logic) so they run anywhere in CI.

The full end-to-end proof (real Frappe site, ToDo ORM CRUD across two org
databases, file-level isolation) lives in the driver's LLM.md as a runnable
recipe; this module locks in the security-critical invariants as unit tests.
"""

import unittest
from unittest.mock import patch

import frappe
from frappe.database.sqlite.tenant import (
	InvalidOrgError,
	resolve_db_stem,
	resolve_org,
	validate_org_slug,
)


class TestOrgSlugValidation(unittest.TestCase):
	def test_accepts_canonical_slugs(self):
		for good in ("acme", "a", "acme-corp", "org1", "a" * 63):
			self.assertEqual(validate_org_slug(good), good)

	def test_rejects_unsafe_slugs(self):
		bad = [
			"../../etc/passwd",  # traversal
			"/etc/passwd",  # absolute
			"a/b",  # separator
			"Acme",  # uppercase -> case-fold collision on APFS/NTFS
			"acme\x00",  # NUL
			"",  # empty
			".",  # dotfile
			"-acme",  # leading hyphen
			"a" * 64,  # too long
			"acme.db",  # dot
			"org space",  # whitespace
			123,  # not a string
			None,
		]
		for value in bad:
			with self.assertRaises(InvalidOrgError):
				validate_org_slug(value)


class TestResolveDbStem(unittest.TestCase):
	def setUp(self):
		self._org = getattr(frappe.local, "org", None)

	def tearDown(self):
		frappe.local.org = self._org

	def test_db_per_org_off_returns_base(self):
		frappe.local.org = "acme"
		with patch.dict(frappe.conf, {"db_per_org": 0}):
			self.assertEqual(resolve_db_stem("platform"), "platform")

	def test_db_per_org_on_no_org_returns_base(self):
		frappe.local.org = None
		with patch.dict(frappe.conf, {"db_per_org": 1}):
			self.assertEqual(resolve_db_stem("platform"), "platform")

	def test_db_per_org_on_with_org_partitions(self):
		frappe.local.org = "acme"
		with patch.dict(frappe.conf, {"db_per_org": 1}):
			self.assertEqual(resolve_db_stem("platform"), "org-acme")

	def test_db_per_org_on_with_bad_org_raises(self):
		frappe.local.org = "../evil"
		with patch.dict(frappe.conf, {"db_per_org": 1}):
			with self.assertRaises(InvalidOrgError):
				resolve_db_stem("platform")

	def test_resolve_org_reads_session_data(self):
		frappe.local.org = None
		with patch.object(frappe.local, "session", frappe._dict(data={"org": "globex"}), create=True):
			self.assertEqual(resolve_org(), "globex")


class TestHanzoIamClaims(unittest.TestCase):
	def test_owner_claim_wins(self):
		from frappe.integrations.hanzo_iam import extract_org_from_claims

		self.assertEqual(extract_org_from_claims({"owner": "acme", "org": "other"}), "acme")

	def test_org_fallback(self):
		from frappe.integrations.hanzo_iam import extract_org_from_claims

		self.assertEqual(extract_org_from_claims({"org": "globex"}), "globex")

	def test_no_claim_returns_none(self):
		from frappe.integrations.hanzo_iam import extract_org_from_claims

		self.assertIsNone(extract_org_from_claims({"email": "z@acme"}))

	def test_malformed_claim_fails_closed(self):
		from frappe.integrations.hanzo_iam import extract_org_from_claims

		with self.assertRaises(InvalidOrgError):
			extract_org_from_claims({"owner": "../../etc"})


if __name__ == "__main__":
	unittest.main()
