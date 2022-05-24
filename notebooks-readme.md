# mySociety standard data repository

This is a pattern for running mySociety Jupyter notebooks. See `notebooks\example.ipynb` for an example of use.

# Structure of this repo

- `.devcontainer` - The setup instructions for vscode and codespaces to work with the relevant dockerfile. Includes expected exemptions.
- `.vscode` - Default code processing settings for vscode.
- `data` - data storage. Has some subfolders to help with common sorting. Files put in `data\private` will not be committed.
- `docs` - jekyll directory that maps to the github pages site for this repo.
- `notebooks` - store any jupyter notebooks here. 
- `script` - script-to`rule`them`all directory.
- `src/data_common` - submodule for the `data_common` repo that contains common tools and helper libraries. This also contains the
- `src/[repo_name]` - where you should put specific python scripts for this repository. 
- `tests` - directory for pytest tests. 
- `Dockerfile.dev` - The dockerfile for this repo. Is locked to the `data_common` image at the latest commit when the repo was upgraded. This can be updated if you make changes that require a new docker setup. 

# Code standards

This repo uses:

- black formatting for python
- pyright's 'basic' type checking for python

`script/test`, as well as running all pytests, enforces black formatting over the repository and pyright's 'basic' checking for python typing. 



## Dataset management

This repo template is meant to help manage and publish datasets in a light-weight way. 

The `dataset` helper tool uses the [frictionless standard](https://specs.frictionlessdata.io/data-package/) to describe datasets. 

A csv table + accompanying resource and schema is a frictionless 'resource'.  Multiple 'resources' are a frictionless data package.

A datapackage joins all resources together in a single Excel file.

### Managing a new dataset

- Run `dataset create` - this will walk you through a series of questions and create a config file in `data\data_packages\[dataset_name]`.
- Now, either manually or using scripts in `src\[repo]` create csv files in this repo. 
- Then run 'dataset refresh' (either *in* the dataset folder, or using the ``--slug [dataset_name]' or `--all` arguments. This will create a yml file for each csv with the schema of the csv file.
- Your task is then, through all yml files in the directory, to go through and fill in the `description` field (and title where missing). 
- `dataset detail` will tell you which fields remain to be filled in. When you think you've got them all, `dataset validate` will tell you if you've created a valid data package that passes tests.
- Then `dataset build` will take these files, compile composite `datapackage.json`, excel and sqlite files, and move them to the Jekyll site in the `docs` directory. This will also create Jekyll markdown files for the pages.
- To run a preview server, use `script\server`.

### Extra notes

- If you want resources to be in a specific order on the website or the Excel sheet, you can use the `sheet_order` property in the resource YAML. This expects a number and the default is 999. Otherwise, files are ordered alphabetically. 
- If you add/remove columns from a table or change the value types, the validation will start to fail. `dataset refresh` will update with new column information, but preserve previous descriptions added (but no other manual changes). 


## How to use notebooks

In a new notebook, add the boilerplate:

```
from data_common.notebook import *
```

This will load common libaries like Pandas, Altair, and numpy, as well as the mySociety customisation of these.

# Binder

[Binder](https://mybinder.org/) is a tool for demoing and using jupyter notebooks online. Binder links are automatically generated for the repo using the cookiecutter template. This will only work with repos that do not require secrets (these can not safely be loaded into binder).

# Rendering

Render setings are defined in a top-level `render.yaml`. This indicates how notebooks should be grouped into a single `document`. Parameters, the title and the slug (used to define folder structure) can use jinja templating to define their values dynamically. 

The order this works is:

1. Variables are loaded from the context modules. 
2. These variables are used to populate the parameters. Parameters are populated in order, so once the first is defined, it can be used in future parameters.
3. The title and slug can simiilarly use the defined parameters. 

Multiple documents can be defined in the render.yaml. Each document can be specified with the key when using the management commands. e.g. 

`python manage.py render second-example-doc`

Will render the doc with the key of `second-example-doc`. When there is only one document, the key does not need to be specified. 

# Uploading

The only build-in uploading steps are to google drive. This needs some additional settings added to the `.env` (see the passwords page on the wiki). Once present, the upload can be run once, and it will trigger the auth workflow to give you the final client key to add to the `.env`.

Once this is done, the render path is defined in the `render.yaml`, where you need to specify both the drive_id and the folder_id (look at the URL of the folder in question). The document will be named with the title defined in `render.yaml`. Caution: google drive allows multiple files of the same name in the same folder, so use the jinja templating to make sure the name changes if the process will be rerun. 

The resulting file can be uploaded with `python manage.py upload`. 

# Parameterised notebooks

If option: rerun is set to true in the `render.yaml`, [papermill](https://github.com/nteract/papermill) is used to add parameters dynamically to notebooks before rendering. 

The way this works is in each notebook, after a code cell that contains `#default-params`, a new cell will be injected containing new parameters. These parameters will be the ones defined in `render.yaml` but can also be overridden in the CLI. For instanceL

`
python manage.py render -p parameter_name parameter_value
`

Will recreate in the injected cell:
`
parameter_name="parameter_value"
`

# Settings and secrets

Once `from data_common import *` is run, a `settings` dict is avaliable. 

This contains variables defined in a top-level `settings.yaml`. [out of date]

Secrets are given a valuein the file as `$$ENV$$` to indicate an enviromental variable of the same name should be used as the source. 

This will also try and extract directly from a top-level `.env` file so the container doesn't have to be reloaded locally to add a new secret.