from . import __version__ as app_version

app_name = "frappe_types"
app_title = "Frappe Types"
app_publisher = "Nikhil Kothari"
app_description = "Typescript type definition generator for Frappe DocTypes"
app_email = "nik.kothari22@live.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_types/css/frappe_types.css"
# app_include_js = "/assets/frappe_types/js/frappe_types.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_types/css/frappe_types.css"
# web_include_js = "/assets/frappe_types/js/frappe_types.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_types/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "frappe_types.utils.jinja_methods",
#	"filters": "frappe_types.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "frappe_types.frappe_types.type_generator.before_migrate"
after_install = "frappe_types.frappe_types.type_generator.after_migrate"

# Migration

before_migrate = "frappe_types.frappe_types.type_generator.before_migrate"
after_migrate = "frappe_types.frappe_types.type_generator.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "frappe_types.uninstall.before_uninstall"
# after_uninstall = "frappe_types.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_types.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events


doc_events = {
    "DocType": {
        "on_update": "frappe_types.frappe_types.type_generator.create_type_definition_file"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"frappe_types.tasks.all"
#	],
#	"daily": [
#		"frappe_types.tasks.daily"
#	],
#	"hourly": [
#		"frappe_types.tasks.hourly"
#	],
#	"weekly": [
#		"frappe_types.tasks.weekly"
#	],
#	"monthly": [
#		"frappe_types.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "frappe_types.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "frappe_types.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "frappe_types.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"frappe_types.auth.validate"
# ]
