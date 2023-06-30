import click
from frappe_types.frappe_types.type_generator import generate_types_for_doctype, generate_types_for_module
from frappe.commands import pass_context
import frappe


@click.command("generate-types-for-doctype")
@click.option("--app", prompt="App Name")
@click.option("--doctype", prompt="Doctype Name")
@click.option(
    "--generate_child_tables",
    default=False,
    is_flag=True,
    prompt="Do you want to generate types for child tables too?",
    help="It will generate Types for child tables includes in the doctype",
)
@click.option(
    "--custom_fields",
    default=False,
    is_flag=True,
    prompt="Do you want to generate types for custom fields too if exists?",
    help="It will generate Types for custom fields includes in the doctype",
)
@pass_context
def generate_types_file_from_doctype(context, app, doctype, generate_child_tables, custom_fields):
    """Generate types file from doctype"""
    if not app:
        click.echo("Please provide an app with --app")
        return
    print(f"Generating types file for {doctype} in {app}")

    for site in context.sites:
        frappe.connect(site=site)
        try:
            generate_types_for_doctype(
                doctype, app, generate_child_tables, custom_fields)
        finally:
            frappe.destroy()
    if not context.sites:
        raise SiteNotSpecifiedError


@click.command("generate-types-for-module")
@click.option("--app", prompt="App Name")
@click.option("--module", prompt="Module Name")
@click.option('--generate_child_tables', default=False, is_flag=True, prompt='Do you want to generate types for child tables too?', help='It will generate Types for child tables includes in the doctype')
@pass_context
def generate_types_file_from_module(context, app, module, generate_child_tables):
    """Generate types file from module"""
    if not app:
        click.echo("Please provide an app with --app")
        return
    print(f"Generating types file for {module} in {app}")

    for site in context.sites:
        frappe.connect(site=site)
        try:
            generate_types_for_module(module, app, generate_child_tables)
        finally:
            frappe.destroy()
    if not context.sites:
        raise SiteNotSpecifiedError


commands = [generate_types_file_from_doctype, generate_types_file_from_module]
