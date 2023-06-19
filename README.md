## Frappe Typescript Type Generator

Typescript type definition generator for Frappe DocTypes.

<br />
<p align="center">
  <a href="https://github.com/nikkothari22/frappe-types"><img src="https://img.shields.io/maintenance/yes/2023?style=flat-square" /></a>
  <a href="https://github.com/nikkothari22/frappe-types"><img src="https://img.shields.io/github/license/nikkothari22/frappe-types?style=flat-square" /></a>
</p>

<br/>

## Usage

To use the app, install it on your local development bench:

```bash
$ bench get-app https://github.com/nikkothari22/frappe-types
$ bench --site mysite.test install-app frappe_types
```

After installing the app, search for "Type Generation Settings" in Desk using the Awesomebar. You need to add the app name and path where you want to save your Typescript type definition files. frappe-types will only run on those app whose app name and path are added in these settings.

<img width="1372" alt="Screenshot 2023-01-12 at 2 30 31 PM" src="https://user-images.githubusercontent.com/59503001/212024507-3197ecfb-e243-4695-a96c-b86d0c1113b4.png">

That's it.

Now whenever you create or update any DocType on your local machine, the app will generate `.ts` files under at the following path: `app/src/types/<module_def>/<doctype_name>.ts`.

<br/>

## Features

1. Supports most Frappe field types
2. Runs automatically whenever you save/update a DocType
3. Adds JSDoc comments for every field in the interface
4. Support CLI command to run type generation on existing DocTypes without having to update them.

<br/>

## CLI Command

You can also run the type generation command from the bench CLI. This will generate types for all DocTypes in the system.
This CLI Command works for all frappe-bench apps, and can generate types of any DocType .

1.  Generate types for DocType.

```bash
 $ bench generate-types-for-doctype --app <app_name> --doctype <doctype_name> [--generate_child_tables] [--custom_fields]

#  or just Answer the prompts
 $ bench generate-types-for-doctype
```

2.  Generate types for Module.

```bash
 $ bench generate-types-for-module --app <app_name> --module <module_name> [--generate_child_tables]

#  or just Answer the prompts
  $ bench generate-types-for-module
```

Note:

1. `--app` - the app name included in `Type Generation Settings` doctype and where you want to save type files.
2. `--doctype` - the doctype name for which you want to generate types.
3. `--module` - the module name for which you want to generate types.
4. `--generate_child_tables` - if you want to generate types for child tables of the doctype (default=False).
5. `--custom_fields` - if you want to generate types for custom fields of the doctype (Default=False).

<br>

## Example

Let's say you create a DocType in a module called "Project Management" called "Projects" and Child Table called "Project User Table" with the following fields:
<br/>

<img width="1047" alt="image" src="https://github.com/The-Commit-Company/frappe-types/assets/59503001/60718378-c1e7-4b65-86eb-5e320ab3a5ca">

<br/>

The app will automatically create a file called `Projects.ts` and `ProjectUserTable.ts` at the path `<your_app_folder>/types/ProjectManagement` like this:

(Notice that spaces in the Module and DocType names will be removed)

<br/>

<img width="1239" alt="image" src="https://github.com/The-Commit-Company/frappe-types/assets/59503001/c67b6f11-66b3-4c72-8217-bb1afab95c02">

<br/>
<img width="1242" alt="image" src="https://github.com/The-Commit-Company/frappe-types/assets/59503001/1c40ccd4-66a1-4b12-be5d-1f8c3798b60e">

<br/>

## Where can you use this?

If you are developing custom Frappe apps with a Frappe backend and a frontend single-page app using React/Vue/other frameworks, you can use this app to generate TypeScript definitions to be used in your frontend app.

<br/>

## What features will we add next?

1. Looking at how to improve speed so that DocType saving does not take a lot of time.

<br/>

## Maintainers

| Maintainer     | GitHub                                          | Social                                                           |
| -------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Nikhil Kothari | [nikkothari22](https://github.com/nikkothari22) | [@nik_kothari22](https://twitter.com/nik_kothari22)              |
| Sumit Jain     | [sumitjain236](https://github.com/sumitjain236) | [@sumit_jain](https://www.linkedin.com/in/sumit-jain-66bb5719a/) |

<br/>

#### License

MIT
