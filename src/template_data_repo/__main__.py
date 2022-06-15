from data_common.management.cli import cli, set_doc_collection
from data_common.management.render_processing import DocumentCollection
from pathlib import Path

if Path("render.yaml").exists():
    doc_collection = DocumentCollection.from_yaml("render.yaml")
    set_doc_collection(doc_collection)

# in principle using the click syntax you could hook further commands on the 'cli' group here.


def main():
    cli()


if __name__ == "__main__":
    main()
