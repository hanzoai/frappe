-- Core Elements to install WNFramework
-- To be called from install.py

--
-- Table structure for table `tabDocField`
--

DROP TABLE IF EXISTS `tabDocField`;
CREATE TABLE `tabDocField` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `parent` TEXT DEFAULT NULL,
  `parentfield` TEXT DEFAULT NULL,
  `parenttype` TEXT DEFAULT NULL,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `fieldname` TEXT DEFAULT NULL,
  `label` TEXT DEFAULT NULL,
  `oldfieldname` TEXT DEFAULT NULL,
  `fieldtype` TEXT DEFAULT NULL,
  `oldfieldtype` TEXT DEFAULT NULL,
  `options` TEXT,
  `search_index` INTEGER NOT NULL DEFAULT 0,
  `show_dashboard` INTEGER NOT NULL DEFAULT 0,
  `hidden` INTEGER NOT NULL DEFAULT 0,
  `set_only_once` INTEGER NOT NULL DEFAULT 0,
  `allow_in_quick_entry` INTEGER NOT NULL DEFAULT 0,
  `print_hide` INTEGER NOT NULL DEFAULT 0,
  `report_hide` INTEGER NOT NULL DEFAULT 0,
  `reqd` INTEGER NOT NULL DEFAULT 0,
  `bold` INTEGER NOT NULL DEFAULT 0,
  `in_global_search` INTEGER NOT NULL DEFAULT 0,
  `collapsible` INTEGER NOT NULL DEFAULT 0,
  `unique` INTEGER NOT NULL DEFAULT 0,
  `no_copy` INTEGER NOT NULL DEFAULT 0,
  `allow_on_submit` INTEGER NOT NULL DEFAULT 0,
  `show_preview_popup` INTEGER NOT NULL DEFAULT 0,
  `trigger` TEXT DEFAULT NULL,
  `collapsible_depends_on` TEXT,
  `mandatory_depends_on` TEXT,
  `read_only_depends_on` TEXT,
  `depends_on` TEXT,
  `permlevel` INTEGER NOT NULL DEFAULT 0,
  `ignore_user_permissions` INTEGER NOT NULL DEFAULT 0,
  `width` TEXT DEFAULT NULL,
  `print_width` TEXT DEFAULT NULL,
  `columns` INTEGER NOT NULL DEFAULT 0,
  `default` TEXT,
  `description` TEXT,
  `in_list_view` INTEGER NOT NULL DEFAULT 0,
  `fetch_if_empty` INTEGER NOT NULL DEFAULT 0,
  `in_filter` INTEGER NOT NULL DEFAULT 0,
  `remember_last_selected_value` INTEGER NOT NULL DEFAULT 0,
  `ignore_xss_filter` INTEGER NOT NULL DEFAULT 0,
  `print_hide_if_no_value` INTEGER NOT NULL DEFAULT 0,
  `allow_bulk_edit` INTEGER NOT NULL DEFAULT 0,
  `in_standard_filter` INTEGER NOT NULL DEFAULT 0,
  `in_preview` INTEGER NOT NULL DEFAULT 0,
  `read_only` INTEGER NOT NULL DEFAULT 0,
  `precision` TEXT DEFAULT NULL,
  `max_height` TEXT DEFAULT NULL,
  `length` INTEGER NOT NULL DEFAULT 0,
  `translatable` INTEGER NOT NULL DEFAULT 0,
  `hide_border` INTEGER NOT NULL DEFAULT 0,
  `hide_days` INTEGER NOT NULL DEFAULT 0,
  `hide_seconds` INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (`name`)
);

--
-- Table structure for table `tabDocPerm`
--

DROP TABLE IF EXISTS `tabDocPerm`;
CREATE TABLE `tabDocPerm` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `parent` TEXT DEFAULT NULL,
  `parentfield` TEXT DEFAULT NULL,
  `parenttype` TEXT DEFAULT NULL,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `permlevel` INTEGER DEFAULT 0,
  `role` TEXT DEFAULT NULL,
  `match` TEXT DEFAULT NULL,
  `read` INTEGER NOT NULL DEFAULT 1,
  `write` INTEGER NOT NULL DEFAULT 1,
  `create` INTEGER NOT NULL DEFAULT 1,
  `submit` INTEGER NOT NULL DEFAULT 0,
  `cancel` INTEGER NOT NULL DEFAULT 0,
  `delete` INTEGER NOT NULL DEFAULT 1,
  `amend` INTEGER NOT NULL DEFAULT 0,
  `report` INTEGER NOT NULL DEFAULT 1,
  `export` INTEGER NOT NULL DEFAULT 1,
  `import` INTEGER NOT NULL DEFAULT 0,
  `share` INTEGER NOT NULL DEFAULT 1,
  `print` INTEGER NOT NULL DEFAULT 1,
  `email` INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (`name`)
);

--
-- Table structure for table `tabDocType Action`
--

DROP TABLE IF EXISTS `tabDocType Action`;
CREATE TABLE `tabDocType Action` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `parent` TEXT DEFAULT NULL,
  `parentfield` TEXT DEFAULT NULL,
  `parenttype` TEXT DEFAULT NULL,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `label` TEXT DEFAULT NULL,
  `group` TEXT DEFAULT NULL,
  `action_type` TEXT DEFAULT NULL,
  `action` TEXT DEFAULT NULL,
  PRIMARY KEY (`name`)
);

--
-- Table structure for table `tabDocType Link`
--

DROP TABLE IF EXISTS `tabDocType Link`;
CREATE TABLE `tabDocType Link` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `parent` TEXT DEFAULT NULL,
  `parentfield` TEXT DEFAULT NULL,
  `parenttype` TEXT DEFAULT NULL,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `group` TEXT DEFAULT NULL,
  `link_doctype` TEXT DEFAULT NULL,
  `link_fieldname` TEXT DEFAULT NULL,
  PRIMARY KEY (`name`)
);

--
-- Table structure for table `tabDocType`
--

DROP TABLE IF EXISTS `tabDocType`;
CREATE TABLE `tabDocType` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `search_fields` TEXT DEFAULT NULL,
  `issingle` INTEGER NOT NULL DEFAULT 0,
  `is_virtual` INTEGER NOT NULL DEFAULT 0,
  `is_tree` INTEGER NOT NULL DEFAULT 0,
  `istable` INTEGER NOT NULL DEFAULT 0,
  `editable_grid` INTEGER NOT NULL DEFAULT 1,
  `track_changes` INTEGER NOT NULL DEFAULT 0,
  `module` TEXT DEFAULT NULL,
  `restrict_to_domain` TEXT DEFAULT NULL,
  `app` TEXT DEFAULT NULL,
  `autoname` TEXT DEFAULT NULL,
  `naming_rule` TEXT DEFAULT NULL,
  `title_field` TEXT DEFAULT NULL,
  `image_field` TEXT DEFAULT NULL,
  `timeline_field` TEXT DEFAULT NULL,
  `sort_field` TEXT DEFAULT NULL,
  `sort_order` TEXT DEFAULT NULL,
  `description` TEXT,
  `colour` TEXT DEFAULT NULL,
  `read_only` INTEGER NOT NULL DEFAULT 0,
  `in_create` INTEGER NOT NULL DEFAULT 0,
  `menu_index` INTEGER DEFAULT NULL,
  `parent_node` TEXT DEFAULT NULL,
  `smallicon` TEXT DEFAULT NULL,
  `allow_copy` INTEGER NOT NULL DEFAULT 0,
  `allow_rename` INTEGER NOT NULL DEFAULT 0,
  `allow_import` INTEGER NOT NULL DEFAULT 0,
  `hide_toolbar` INTEGER NOT NULL DEFAULT 0,
  `track_seen` INTEGER NOT NULL DEFAULT 0,
  `max_attachments` INTEGER NOT NULL DEFAULT 0,
  `print_outline` TEXT DEFAULT NULL,
  `document_type` TEXT DEFAULT NULL,
  `icon` TEXT DEFAULT NULL,
  `color` TEXT DEFAULT NULL,
  `tag_fields` TEXT DEFAULT NULL,
  `subject` TEXT DEFAULT NULL,
  `_last_update` TEXT DEFAULT NULL,
  `engine` TEXT DEFAULT 'InnoDB',
  `default_print_format` TEXT DEFAULT NULL,
  `is_submittable` INTEGER NOT NULL DEFAULT 0,
  `show_name_in_global_search` INTEGER NOT NULL DEFAULT 0,
  `_user_tags` TEXT DEFAULT NULL,
  `custom` INTEGER NOT NULL DEFAULT 0,
  `beta` INTEGER NOT NULL DEFAULT 0,
  `has_web_view` INTEGER NOT NULL DEFAULT 0,
  `allow_guest_to_view` INTEGER NOT NULL DEFAULT 0,
  `route` TEXT DEFAULT NULL,
  `is_published_field` TEXT DEFAULT NULL,
  `website_search_field` TEXT DEFAULT NULL,
  `email_append_to` INTEGER NOT NULL DEFAULT 0,
  `subject_field` TEXT DEFAULT NULL,
  `sender_field` TEXT DEFAULT NULL,
  `show_title_field_in_link` INTEGER NOT NULL DEFAULT 0,
  `migration_hash` TEXT DEFAULT NULL,
  `translated_doctype` INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (`name`)
);

--
-- Table structure for table `tabSeries`
--

DROP TABLE IF EXISTS `tabSeries`;
CREATE TABLE `tabSeries` (
  `name` TEXT NOT NULL,
  `current` INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(`name`)
);

--
-- Table structure for table `tabSessions`
--

DROP TABLE IF EXISTS `tabSessions`;
CREATE TABLE `tabSessions` (
  `user` TEXT DEFAULT NULL,
  `sid` TEXT DEFAULT NULL,
  `sessiondata` TEXT,
  `ipaddress` TEXT DEFAULT NULL,
  `lastupdate` TEXT DEFAULT NULL,
  `status` TEXT DEFAULT NULL,
  PRIMARY KEY (`sid`)
);

--
-- Table structure for table `tabSingles`
--

DROP TABLE IF EXISTS `tabSingles`;
CREATE TABLE `tabSingles` (
  `doctype` TEXT DEFAULT NULL,
  `field` TEXT DEFAULT NULL,
  `value` TEXT,
  PRIMARY KEY (`doctype`, `field`)
);

--
-- Table structure for table `__Auth`
--

DROP TABLE IF EXISTS `__Auth`;
CREATE TABLE `__Auth` (
  `doctype` TEXT NOT NULL,
  `name` TEXT NOT NULL,
  `fieldname` TEXT NOT NULL,
  `password` TEXT NOT NULL,
  `encrypted` INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (`doctype`, `name`, `fieldname`)
);

--
-- Table structure for table `tabFile`
--

DROP TABLE IF EXISTS `tabFile`;
CREATE TABLE `tabFile` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `parent` TEXT DEFAULT NULL,
  `parentfield` TEXT DEFAULT NULL,
  `parenttype` TEXT DEFAULT NULL,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `file_name` TEXT DEFAULT NULL,
  `file_url` TEXT DEFAULT NULL,
  `module` TEXT DEFAULT NULL,
  `attached_to_name` TEXT DEFAULT NULL,
  `file_size` INTEGER NOT NULL DEFAULT 0,
  `attached_to_doctype` TEXT DEFAULT NULL,
  PRIMARY KEY (`name`)
);

--
-- Table structure for table `tabDefaultValue`
--

DROP TABLE IF EXISTS `tabDefaultValue`;
CREATE TABLE `tabDefaultValue` (
  `name` TEXT NOT NULL,
  `creation` TEXT DEFAULT NULL,
  `modified` TEXT DEFAULT NULL,
  `modified_by` TEXT DEFAULT NULL,
  `owner` TEXT DEFAULT NULL,
  `docstatus` INTEGER NOT NULL DEFAULT 0,
  `parent` TEXT DEFAULT NULL,
  `parentfield` TEXT DEFAULT NULL,
  `parenttype` TEXT DEFAULT NULL,
  `idx` INTEGER NOT NULL DEFAULT 0,
  `defvalue` TEXT,
  `defkey` TEXT DEFAULT NULL,
  PRIMARY KEY (`name`)
);
