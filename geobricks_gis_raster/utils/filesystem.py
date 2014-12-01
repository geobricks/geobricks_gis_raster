import os
import tempfile
import uuid
from geobricks_gis_raster.config.config import config

# temporary folder
try:
    folder_tmp_default = config["settings"]["folders"]["tmp"]
except Exception:
    folder_tmp_default = tempfile.gettempdir()


def create_tmp_filename(extension='', filename='',  subfolder='', add_uuid=True, folder_tmp=folder_tmp_default):
    """
    :param extension: i.e. "tif"
    :param subfolder: "modis_folder"
    :param filename: "modis"
    :param add_uuid: add or not a uuid to the file
    :param folder_tmp: if not specified it takes the default tmp folder of the os.
    :return: a path to a tmp file
    """

    """
    Create the path for a tmp file and filename

    @type path: string
    @param path: path from the tmp folder
    @type extension: extension
    @param extension: i.e. .geotiff
    """
    if extension != '' and "." not in extension: extension = "." + extension
    folder_path = os.path.join(folder_tmp, subfolder)
    if subfolder is not '':
        try:
            os.makedirs(folder_path)
        except Exception, e:
            # log.warn(e)
            pass
    file_path = os.path.join(folder_path, filename)
    if add_uuid:
        return (file_path + str(uuid.uuid4()) + extension).encode('utf-8')
    else:
        return (file_path + extension).encode('utf-8')


def get_raster_path_by_uid(uid):
    l = uid.split("|")
    return os.path.join(config["settings"]["folders"]["geoserver_datadir"], "data",  l[0], l[1], l[1] + ".geotiff");

