import frappe
from pathlib import Path
from .utils import create_file
import subprocess


def create_type_definition_file(doc, method=None):

    # Check if type generation is paused
    common_site_config = frappe.get_conf()

    frappe_types_pause_generation = common_site_config.get(
        "frappe_types_pause_generation", 0)

    if frappe_types_pause_generation:
        print("Frappe Types is paused")
        return

    doctype = frappe.get_doc("DocType", doc.name)

    if is_developer_mode_enabled() and is_valid_doctype(doctype):
        print("Generating type definition file for " + doctype.name)
        module = frappe.get_doc('Module Def', doctype.module)

        if module.app_name == "frappe" or module.app_name == "erpnext":
            print("Ignoring core app DocTypes")
            return

        app_path: Path = Path("../apps") / module.app_name
        if not app_path.exists():
            print("App path does not exist - ignoring type generation")
            return

        # Fetch Type Generation Settings Document
        type_generation_settings = frappe.get_doc(
            'Type Generation Settings').as_dict().type_settings

        # Checking if app is existed in type generation settings
        for type_setting in type_generation_settings:
            if module.app_name == type_setting.app_name:
                # Types folder is created in the app
                type_path: Path = app_path / type_setting.app_path / "types"

                if not type_path.exists():
                    type_path.mkdir()

                module_path: Path = type_path / module.name.replace(" ", "")
                if not module_path.exists():
                    module_path.mkdir()

                generate_type_definition_file(doctype, module_path)
            else:
                return


def generate_type_definition_file(doctype, module_path):

    doctype_name = doctype.name.replace(" ", "")
    type_file_path = module_path / (doctype_name + ".ts")
    type_file_content = generate_type_definition_content(doctype)
    create_file(type_file_path, type_file_content)


def generate_type_definition_content(doctype):
    content = "export interface " + doctype.name.replace(" ", "") + "{\n"

    # Boilerplate types for all documents
    content += "\tcreation: string\n\tname: string\n\tmodified: string\n\towner: string\n\tmodified_by: string\n\tdocstatus: 0 | 1 | 2\n\tparent?: string\n\tparentfield?: string\n\tparenttype?: string\n\tidx?: number\n"

    for field in doctype.fields:
        if field.fieldtype in ["Section Break", "Column Break", "HTML", "Button", "Fold", "Heading", "Tab Break", "Break"]:
            continue
        content += get_field_comment(field)
        content += "\t" + get_field_type_definition(field) + "\n"

    content += "}"
    return content


def get_field_comment(field):
    desc = field.description
    print(field.options)
    if field.fieldtype in ["Link", "Table", "Table MultiSelect"]:
        desc = field.options + \
            (" - " + field.description if field.description else "")
    return "\t/**\t" + field.label + " : " + field.fieldtype + ((" - " + desc) if desc else "") + "\t*/\n"


def get_field_type_definition(field):
    return field.fieldname + get_required(field) + ": " + get_field_type(field)


def get_field_type(field):

    basic_fieldtypes = {
        "Data": "string",
        "Small Text": "string",
        "Text Editor": "string",
        "Text": "string",
        "Code": "string",
        "Link": "string",
        "Dynamic Link": "string",
        "Read Only": "string",
        "Password": "string",
        "Text Editor": "string",
        "Check": "0 | 1",
        "Int": "number",
        "Float": "number",
        "Currency": "number",
        "Percent": "number",
        "Attach Image": "string",
        "Attach": "string",
        "HTML Editor": "string",
        "Image": "string",
        "Duration": "string",
        "Small Text": "string",
        "Date": "string",
        "Datetime": "string",
        "Time": "string",
        "Phone": "string",
        "Color": "string",
        "Long Text": "string",
        "Markdown Editor": "string",
    }

    # TODO: Add support for Table and Table Multiselect - will need to add imports to file
    if field.fieldtype in ["Table", "Table MultiSelect"]:
        return "any[]"

    if field.fieldtype == "Select":
        options = field.options.split("\n")
        t = ""
        for option in options:
            t += "\"" + option + "\" | "
        if t.endswith(" | "):
            t = t[:-3]
        return t

    if field.fieldtype in basic_fieldtypes:
        return basic_fieldtypes[field.fieldtype]
    else:
        return "any"


def get_required(field):
    if field.reqd:
        return ""
    else:
        return "?"


def is_valid_doctype(doctype):
    if (doctype.custom):
        print("Custom DocType - ignoring type generation")
        return False

    if (doctype.is_virtual):
        print("Virtual DocType - ignoring type generation")
        return False

    return True


def is_developer_mode_enabled():
    if not frappe.conf.get("developer_mode"):
        print("Developer mode not enabled - ignoring type generation")
        return False
    return True


def before_migrate():
    # print("Before migrate")
    subprocess.run(
        ["bench", "config", "set-common-config", "-c", "frappe_types_pause_generation", "1"])


def after_migrate():
    # print("After migrate")
    subprocess.run(["bench", "config", "set-common-config",
                   "-c", "frappe_types_pause_generation", "0"])
