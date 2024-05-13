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
    
    if frappe.flags.in_patch or frappe.flags.in_migrate or frappe.flags.in_install or frappe.flags.in_setup_wizard:
        print("Skipping type generation in patch, migrate, install or setup wizard")
        return

    doctype = doc

    if is_developer_mode_enabled() and is_valid_doctype(doctype):
        print("Generating type definition file for " + doctype.name)
        module_name = doctype.module
        app_name = frappe.db.get_value('Module Def', module_name, 'app_name')

        if app_name == "frappe" or app_name == "erpnext":
            print("Ignoring core app DocTypes")
            return

        app_path: Path = Path("../apps") / app_name
        if not app_path.exists():
            print("App path does not exist - ignoring type generation")
            return

        # Fetch Type Generation Settings Document
        type_generation_settings = frappe.get_doc(
            'Type Generation Settings'
        ).as_dict().type_settings

        # Checking if app is existed in type generation settings
        for type_setting in type_generation_settings:
            if app_name == type_setting.app_name:
                # Types folder is created in the app
                type_path: Path = app_path / type_setting.app_path / "types"

                if not type_path.exists():
                    type_path.mkdir()

                module_path: Path = type_path / module_name.replace(" ", "")
                if not module_path.exists():
                    module_path.mkdir()

                generate_type_definition_file(
                    doctype, module_path, generate_child_tables=False)

def generate_type_definition_file(doctype, module_path, generate_child_tables=False):

    doctype_name = doctype.name.replace(" ", "")
    type_file_path = module_path / (doctype_name + ".ts")
    type_file_content = generate_type_definition_content(
        doctype, module_path, generate_child_tables)

    create_file(type_file_path, type_file_content)


def generate_type_definition_content(doctype, module_path, generate_child_tables):
    import_statement = ""

    content = "export interface " + doctype.name.replace(" ", "") + "{\n"

    # Boilerplate types for all documents
    name_field_type = "string"
    if doctype.naming_rule == "Autoincrement":
        name_field_type = "number"
    content += f"\tname: {name_field_type}\n\tcreation: string\n\tmodified: string\n\towner: string\n\tmodified_by: string\n\tdocstatus: 0 | 1 | 2\n\tparent?: string\n\tparentfield?: string\n\tparenttype?: string\n\tidx?: number\n"

    for field in doctype.fields:
        if field.fieldtype in ["Section Break", "Column Break", "HTML", "Button", "Fold", "Heading", "Tab Break", "Break"]:
            continue
        content += get_field_comment(field)

        file_defination, statement = get_field_type_definition(
            field, doctype, module_path, generate_child_tables)

        if statement and import_statement.find(statement) == -1:
            import_statement += statement
        
        content += "\t" + file_defination + "\n"

    content += "}"

    return import_statement + "\n" + content

def get_field_comment(field):
    desc = field.description
    if field.fieldtype in ["Link", "Table", "Table MultiSelect"]:
        desc = field.options + \
            (" - " + field.description if field.description else "")
    return "\t/**\t" + (field.label if field.label else '') + " : " + field.fieldtype + ((" - " + desc) if desc else "") + "\t*/\n"


def get_field_type_definition(field, doctype, module_path, generate_child_tables):
    field_type,import_statement =  get_field_type(field, doctype, module_path, generate_child_tables)
    return field.fieldname + get_required(field) + ": " + field_type , import_statement


def get_field_type(field, doctype, module_path, generate_child_tables):

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

    if field.fieldtype in ["Table", "Table MultiSelect"]:

        return get_imports_for_table_fields(field, doctype, module_path, generate_child_tables)

    if field.fieldtype == "Select":
        if (field.options):
            options = field.options.split("\n")
            t = ""
            for option in options:
                t += "\"" + option + "\" | "
            if t.endswith(" | "):
                t = t[:-3]
            return t, None
        else:
            return 'string',None

    if field.fieldtype in basic_fieldtypes:
        return basic_fieldtypes[field.fieldtype], None
    else:
        return "any", None


def get_imports_for_table_fields(field, doctype, module_path, generate_child_tables):
    if field.fieldtype == "Table" or field.fieldtype == "Table MultiSelect":
        doctype_module_name = doctype.module
        table_doc = frappe.get_doc('DocType', field.options)
        table_module_name = table_doc.module
        should_import = False
        import_statement = ""

        # check if table doctype type file is already generated and exists

        if doctype_module_name == table_module_name:

            table_file_path: Path = module_path / \
                (table_doc.name.replace(" ", "") + ".ts")
            if not table_file_path.exists():
                if generate_child_tables:
                    generate_type_definition_file(table_doc, module_path)

                    should_import = True

            else:
                should_import = True
            
            import_statement = ("import { " + field.options.replace(" ", "") + " } from './" +
                                    field.options.replace(" ", "") + "'") + "\n" if should_import else ''

        else:

            table_module_path: Path = module_path.parent / \
                table_module_name.replace(" ", "")
            if not table_module_path.exists():
                table_module_path.mkdir()

            table_file_path: Path = table_module_path / \
                (table_doc.name.replace(" ", "") + ".ts")

            if not table_file_path.exists():
                if generate_child_tables:
                    generate_type_definition_file(table_doc, table_module_path)

                    should_import = True

            else:
                should_import = True

            import_statement = ("import { " + field.options.replace(" ", "") + " } from '../" +
                                    table_module_name.replace(" ", "") + "/" + field.options.replace(" ", "") + "'") + "\n" if should_import else ''

        return field.options.replace(" ", "") + "[]" if should_import else 'any', import_statement
    return "",None


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


@frappe.whitelist()
def generate_types_for_doctype(doctype, app_name, generate_child_tables=False, custom_fields=False):

    try:
        # custom_fields True means that the generate .ts file for custom fields with original fields
        doc = frappe.get_meta(doctype) if custom_fields else frappe.get_doc(
            'DocType', doctype)

        # Check if type generation is paused
        common_site_config = frappe.get_conf()

        frappe_types_pause_generation = common_site_config.get(
            "frappe_types_pause_generation", 0)

        if frappe_types_pause_generation:
            print("Frappe Types is paused")
            return

        if is_developer_mode_enabled() and is_valid_doctype(doc):
            print("Generating type definition file for " + doc.name)
            module_name = doc.module

            app_path: Path = Path("../apps") / app_name
            if not app_path.exists():
                print("App path does not exist - ignoring type generation")
                return

            # Fetch Type Generation Settings Document
            type_generation_settings = frappe.get_doc(
                'Type Generation Settings'
            ).as_dict().type_settings

            # Checking if app is existed in type generation settings
            for type_setting in type_generation_settings:
                if app_name == type_setting.app_name:
                    # Types folder is created in the app
                    # path: Path = type_setting.app_path / "types"
                    type_path: Path = app_path / type_setting.app_path / "types"
                    if not type_path.exists():
                        type_path.mkdir()

                    module_path: Path = type_path / \
                        module_name.replace(" ", "")
                    if not module_path.exists():
                        module_path.mkdir()

                    generate_type_definition_file(
                        doc, module_path, generate_child_tables)
               
    except Exception as e:
        err_msg = f": {str(e)}\n{frappe.get_traceback()}"
        print(
            f"An error occurred while generating type for {doctype} {err_msg}")


@frappe.whitelist()
def generate_types_for_module(module, app_name, generate_child_tables=False):
    try:
        child_tables = [doctype['name'] for doctype in frappe.get_list(
            'DocType', filters={'module': module, 'istable': 1})]
        if len(child_tables) > 0:
            for child_table in child_tables:
                generate_types_for_doctype(
                    child_table, app_name, generate_child_tables)

        doctypes = [doctype['name'] for doctype in frappe.get_list(
            'DocType', filters={'module': module, 'istable': 0})]

        if len(doctypes) > 0:
            for doctype in doctypes:
                generate_types_for_doctype(
                    doctype, app_name, generate_child_tables)
    except Exception as e:
        err_msg = f": {str(e)}\n{frappe.get_traceback()}"
        print(
            f"An error occurred while generating type for {module} {err_msg}")
