from upload2remarkable.uploader import Uploader

import click


@click.command()
@click.version_option(version="0.2.0")
@click.argument("source_file")
@click.argument("destination_folder")
def upload2remarkable(source_file, destination_folder):
    """
    Uploads a source_file to a reMarkable Cloud destination_folder.

    Relies on a ~/.rmapi configuration file.
    """

    click.echo("Uploading file {}".format(source_file))
    Uploader().upload_file_to_folder(source_file, destination_folder)
    click.echo("Uploaded file {} to {}".format(source_file, destination_folder))
