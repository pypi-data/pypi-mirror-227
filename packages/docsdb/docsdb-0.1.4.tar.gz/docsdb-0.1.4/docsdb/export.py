import os
import shutil
import click
from docsdb.mongodb import CURRENT_DIR, TARGET_DIR
from docsdb.include import DOCUMENTATION_INDEX_FILE_PATH


@click.command()
def export():
    """
    This helps export the static index.html required to run.
    Useful in cases when you want have the target/ folder generated with index.html
    So you can copy your artefacts {metadata.json, docs.json} manually
    """
    target_dir = os.path.join(CURRENT_DIR, TARGET_DIR)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    target_file_path = os.path.join(target_dir, "index.html")
    shutil.copyfile(DOCUMENTATION_INDEX_FILE_PATH, target_file_path)

    click.echo("target/ folder created with the index.html")
    click.echo(
        "copy your artefacts {metadata.json, docs_metadata.json} and run \"docsdb serve\" to view your documentation!"
    )
