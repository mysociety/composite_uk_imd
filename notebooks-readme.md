# mySociety Jupyter notebook system

This is a pattern for running mySociety Jupyter notebooks. See `notebooks\example.ipynb` for an example of use.

## How to use

In a new notebook, add the boilerplate:

```
from notebook_helper import *

notebook_setup()
```

This will load common libaries like Pandas, Altair, and numpy, as well as the mySociety customisation of these.

The try/except pattern is because the notebooks will be run by users in the `notebooks` folder, and so need the setup script to add the level above to path, but the papermill process will run from the top-level.

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