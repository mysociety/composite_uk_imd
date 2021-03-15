
import json
import os
from datetime import datetime
from pathlib import Path

import nbformat
import pandas as pd
from IPython.core.display import display as jupyter_display
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import (ClearMetadataPreprocessor,
                                     ClearOutputPreprocessor,
                                     ExecutePreprocessor)
from traitlets.config import Config
from ipython_genutils.text import indent as normal_indent


def indent(instr, nspaces=4, ntabs=0, flatten=False):
    if instr.strip() and instr.strip()[0] == "|":
        return instr
    return normal_indent(instr, nspaces, ntabs, flatten)


def display(obj, *args, format=None, **kwargs):
    """
    changes default to markdown display for tables
    """
    if isinstance(obj, pd.DataFrame):
        # usually percentage
        if format:
            for c in obj.columns[1:]:
                obj[c] = obj[c].map(lambda n: format.format(n))
        print(obj.to_markdown(index=False, tablefmt="github"))
    else:
        jupyter_display(obj,  *args, **kwargs)


def compile_notebook(input_file="readme.ipynb", output_file=None):
    # render clear markdown version of chart
    # equiv of `jupyter nbconvert --ClearMetadataPreprocessor.enabled=True --ClearOutput.enabled=True --no-input --execute readme.ipynb --to markdown`

    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".md"

    with open(input_file) as f:
        nb = json.load(f)

    def check_for_self_reference(x):
        # scope out the cell that called this function
        # prevent circular call
        for x in x["source"]:
            if "compile_notebook(" in x:
                return True
        return False

    nb["cells"] = [x for x in nb["cells"]
                   if check_for_self_reference(x) is False]
    str_notebook = json.dumps(nb)
    nb = nbformat.reads(str_notebook, as_version=4)

    c = Config()
    c.MarkdownExporter.preprocessors = [
        ClearMetadataPreprocessor,
        ClearOutputPreprocessor,
        ExecutePreprocessor]
    c.MarkdownExporter.filters = {"indent": indent}
    c.MarkdownExporter.exclude_input = True

    markdown = MarkdownExporter(config=c)

    body, resources = markdown.from_notebook_node(nb)

    with open(output_file, "w") as f:
        f.write(body)

    print("Written to {0} at {1}".format(output_file, datetime.now(tz=None)))
