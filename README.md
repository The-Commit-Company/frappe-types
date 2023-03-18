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
```
After installing the app, search for "Type Generation Settings" in Desk using the Awesomebar. You need to add the app name and path where you want to save your Typescript type definition files. frappe-types will only run on those app whose app name and path are added in these settings.

<img width="1372" alt="Screenshot 2023-01-12 at 2 30 31 PM" src="https://user-images.githubusercontent.com/59503001/212024507-3197ecfb-e243-4695-a96c-b86d0c1113b4.png">

That's it. 

Now whenever you create or update any DocType on your local machine, the app will generate `.ts` files under at the following path: `app/types/<module_def>/<doctype_name>.ts`.

<br/>

## Features

1. Supports most Frappe field types
2. Runs automatically whenever you save/update a DocType
3. Adds JSDoc comments for every field in the interface

<br/>

## Example

Let's say you create a DocType in a module called "Project Management" called "Project" with the following fields:
<br/>

<img width="1058" alt="image" src="https://user-images.githubusercontent.com/19825455/189567982-87e3b28f-3627-4a96-87cc-eddee164f4c2.png">

<br/>

The app will automatically create a file called `Project.ts` at the path `<your_app_folder>/types/ProjectManagement/Project` like this:

(Notice that spaces in the Module and DocType names will be removed)

<br/>

<img width="1337" alt="image" src="https://user-images.githubusercontent.com/19825455/189568132-ecc79a9e-832a-4558-8102-2a9d919e5fed.png">


<br/>

## Where can you use this?

If you are developing custom Frappe apps with a Frappe backend and a frontend single-page app using React/Vue/other frameworks, you can use this app to generate TypeScript definitions to be used in your frontend app. 


<br/>

## What features will we add next?

1. Looking at how to improve speed so that DocType saving does not take a lot of time.
2. Adding a CLI option to run type generation on existing DocTypes without having to update them.
   
<br/>


## Maintainers

| Maintainer     | GitHub                                          | Social                                                          |
| -------------- | ----------------------------------------------- | ---------------------------------------------------             |
| Nikhil Kothari | [nikkothari22](https://github.com/nikkothari22) | [@nik_kothari22](https://twitter.com/nik_kothari22)             |
| Sumit Jain     | [sumitjain236](https://github.com/sumitjain236) | [@sumit_jain](https://www.linkedin.com/in/sumit-jain-66bb5719a/)|

<br/>

#### License

MIT
