from osgeo import gdal
import os
import subprocess
import copy
import math
import json
import rasterio
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename

log = logger(__file__)

# example of statistics
stats_config = {
    "descriptive_stats": {
        "force": True
    },
    "histogram": {
        "buckets": 256,
        "include_out_of_range": 0,
        "force": True
    }
}


def crop_raster_on_vector_bbox_and_postgis_db(input_file, db_connection_string, query, minlon, minlat, maxlon, maxlat, srcnodata=None, dstnodata=None):
    if srcnodata == None:
        srcnodata = get_nodata_value(input_file)
    if dstnodata == None:
        dstnodata = srcnodata

    output_bbox = crop_raster_with_bounding_box(input_file, minlon, minlat, maxlon, maxlat, srcnodata)
    output_path = crop_by_vector_from_db(output_bbox, db_connection_string, query, srcnodata, dstnodata)
    os.remove(output_bbox)
    return output_path


def crop_raster_with_bounding_box(input_file, minlon, minlat, maxlon, maxlat, srcnodata=None):
    if srcnodata == None:
        srcnodata = get_nodata_value(input_file)

    log.info("crop_raster_with_bounding_box")
    output_file = create_tmp_filename('.tif', 'gdal_translate_by_bbox')
    args = [
        "gdal_translate",
        "-a_nodata", str(srcnodata),
        "-projwin",
        str(minlat),
        str(minlon),
        str(maxlat),
        str(maxlon),
        input_file,
        output_file
    ]
    try:
        log.info(args)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
        # proc = subprocess.check_output(args)
        # print proc
    except Exception, e:
        raise Exception(e)
    return output_file


def crop_by_vector_from_db(input_file, db_connection_string, query, srcnodata='nodata', dstnodata='nodata'):
    log.info(query)
    output_file_gdal_warp = create_tmp_filename('.tif', 'gdal_warp')
    output_file = create_tmp_filename('.tif', 'output')
    log.info(input_file)

    # crop the layer on cutline
    args = [
        'gdalwarp',
        "-q",
        "-multi",
        "-of", "GTiff",
        "-cutline", db_connection_string,
        "-csql", query,
        "-srcnodata", str(srcnodata),
        "-dstnodata", str(dstnodata),
        # -crop_to_cutline is needed otherwise the layer is not cropped
        # TODO: resolve shifting problem
        # "-crop_to_cutline",
        # "-dstalpha",
        input_file,
        output_file_gdal_warp
    ]
    try:
        log.info(args)
        #TODO: handle subprocess Error (like that is not taken)
        output = subprocess.check_output(args)
        # stdout_value, error = proc.communicate()
        log.info(output)
    except Exception, e:
        raise Exception(e)

        # TODO: is it useful the third opetation?
    args = [
        'gdal_translate',
        "-co", "COMPRESS=DEFLATE",
        "-a_nodata", str(dstnodata),
        output_file_gdal_warp,
        output_file
    ]
    try:
        log.info(" ".join(args))
        #TODO: handle subprocess Error (like that is not taken)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
    except:
        stdout_value = proc.communicate()[0]
        raise Exception(stdout_value)

    #os.remove(output_file_gdal_warp)
    if os.path.isfile(output_file):
        return output_file
    return None



############### OLD METHODS
# TODO: remove the db_spatial from here
def crop_by_vector_database(raster_path, db_spatial, query_extent, query_layer):
    # TODO: make it better
    geom = json.dumps(db_spatial.query(query_extent))
    g = json.loads(geom)
    #log.info(g)
    obj = g[0][0]
    #log.info(obj)
    obj = json.loads(obj)
    # TODO: this is hardcoded because the returning bbox is different from the one used by GDAL processing
    #log.info(obj["coordinates"])
    minlat = obj["coordinates"][0][0][0]
    minlon = obj["coordinates"][0][1][1]
    maxlat = obj["coordinates"][0][2][0]
    maxlon = obj["coordinates"][0][0][1]
    db_connection_string = db_spatial.get_connection_string(True)
    srcnodatavalue = get_nodata_value(raster_path)
    return _crop_by_vector_database(raster_path, query_layer, db_connection_string, minlat, minlon, maxlat, maxlon, srcnodatavalue, srcnodatavalue)


# TODO: instead of the connection string pass the geometry
def _crop_by_vector_database(input_file, query, db_connection_string, minlat, minlon, maxlat, maxlon, srcnodata='nodata', dstnodata='nodata'):
    log.info(query)
    output_file_gdal_translate = create_tmp_filename('.tif', 'gdal_translate')
    output_file_gdal_warp = create_tmp_filename('.tif', 'gdal_warp')
    output_file = create_tmp_filename('.tif', 'output')
    args = [
        'gdal_translate',
        '-projwin',
        str(minlat),
        str(minlon),
        str(maxlat),
        str(maxlon),
        input_file,
        output_file_gdal_translate
    ]
    try:
        log.info(args)
        #TODO: handle subprocess Error (like that is not taken)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
    except:
        stdout_value = proc.communicate()[0]
        raise Exception(stdout_value)

    args = [
        'gdalwarp',
        "-q",
        "-multi",
        "-of", "GTiff",
        "-cutline", db_connection_string,
        "-csql", query,
        "-srcnodata", str(srcnodata),
        "-dstnodata", str(dstnodata),
        # -crop_to_cutline is needed otherwise the layer is not cropped
        # TODO: resolve shifting problem
        # "-crop_to_cutline",
        # "-dstalpha",
        output_file_gdal_translate,
        output_file_gdal_warp
    ]
    try:
        #log.info(args)
        #TODO: handle subprocess Error (like that is not taken)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
    except:
        stdout_value = proc.communicate()[0]
        raise Exception(stdout_value)

    # TODO: is it useful the third opetation?
    args = [
        'gdal_translate',
        "-co", "COMPRESS=DEFLATE",
        "-a_nodata", str(dstnodata),
        output_file_gdal_warp,
        output_file
    ]
    try:
        log.info(args)
        #TODO: handle subprocess Error (like that is not taken)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
    except:
        stdout_value = proc.communicate()[0]
        raise Exception(stdout_value)

    os.remove(output_file_gdal_warp)
    os.remove(output_file_gdal_translate)

    if os.path.isfile(output_file):
        return output_file
    return None


def get_statistics(input_file, config=stats_config):
    """
    :param input_file: file to be processed
    :param config: json config file to be passed
    :return: computed statistics
    """
    #log.info("get_statistics: %s" % input_file)

    if config is None:
        config = copy.deepcopy(stats_config)

    stats = {}
    try:
        if os.path.isfile(input_file):
            ds = gdal.Open(input_file)
            if "descriptive_stats" in config:
                stats["stats"] = _get_descriptive_statistics(ds, config["descriptive_stats"])
            if "histogram" in config:
                stats["hist"] = _get_histogram(ds, config["histogram"])
        else:
            raise Exception("Exceptiuon")
    except Exception, e:
        raise Exception(e)
    return stats


def get_descriptive_statistics(input_file, config=stats_config["descriptive_stats"]):
    """
    :param input_file: file to be processed
    :param config: json config file to be passed
    :return: return and array with the min, max, mean, sd statistics per band i.e. [{"band": 1, "max": 549.0, "mean": 2.8398871527778, "sd": 17.103028971129, "min": 0.0}]
    """
    try:
        if os.path.isfile(input_file):
            ds = gdal.Open(input_file)
            return _get_descriptive_statistics(ds, config)
        else:
            # TODO exception
            raise Exception("Exceptiuon")
    except Exception, e:
        raise Exception(e)


def get_histogram(input_file, config=stats_config["histogram"]):
    """
    :param input_file: file to be processed
    :type string
    :param config: json config file to be passed
    :type json
    :return: return and array with the min, max, mean, sd statistics per band i.e. [{"band": 1, "buckets": 256, "values": [43256, 357, ...], "max": 998.0, "min": 0.0}]
    """
    try:
        if os.path.isfile(input_file):
            ds = gdal.Open(input_file)
            return _get_histogram(ds, config)
        else:
            # TODO exception
            raise Exception("Exceptiuon")
    except Exception, e:
        raise Exception(e)



def get_location_values(input_files, lat, lon, band=None):
    """
    Get the value of a (lat, lon) location

    # TODO:
    1) pass a json, instead of [files] pass file and id
    2) pass as well the projection used i.e. EPSG:4326
    3) for now it's used x, y as lat lon (it's not used the projection)

    :param input_files: files to be processed
    :type array
    :param lat: x value (for now it's used LatLon)
    :type float
    :param lon: y value (for now it's used LatLon)
    :type float
    :param band: band default=None (not yet used)
    :return: and array with the values of the (lat, lon) location
    """
    values = []
    for input_file in input_files:
        values.append(_location_value(input_file, lat, lon, band))
    return values


def _location_value(input_file, lat, lon, band=None):
    """
     Get the value of a (lat, lon) location
    :param input_file: file to be processed
    :type string
    :param x: x value
    :type float
    :param y: y value
    :type float
    :param band: band default=None (not yet used)
    :return: and array with the values of the (lat, lon) location
    """
    # TODO: check with -wgs84 values instead of -geoloc that is the reference system of the image
    cmd = "gdallocationinfo -valonly " + input_file + " -wgs84 " + str(lon) + " " + str(lat)

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.strip()


def _get_descriptive_statistics(ds, config):
    # variables
    force = True if "force" not in config else bool(config["force"])

    # stats
    stats = []
    for band in range(ds.RasterCount):
        band += 1
        srcband = ds.GetRasterBand(band)
        if srcband is None:
            continue
        # TODO: check why the "force" doesn't work on GetStatistics but the ComputeStatistics works
        if force:
            s = srcband.ComputeStatistics(0)
            #s = srcband.ComputeRasterMinMax(False)
        else:
            s = srcband.GetStatistics(False, force)
        if stats is None:
            continue
        if math.isnan(s[2]):
            log.warn("polygon is empty! %s " % s)
        else:
            stats.append({"band": band, "min": s[0], "max": s[1], "mean": s[2], "sd": s[3]})


    return stats


def _get_histogram(ds, config=stats_config["histogram"]):
    #log.info("config %s " % config)
    # variables
    # TODO boolean of config value
    force = True if "force" not in config else bool(config["force"])
    buckets = 256 if "buckets" not in config else int(config["buckets"])
    min = None if "min" not in config else int(config["min"])
    max = None if "max" not in config else int(config["max"])
    include_out_of_range = 0 if "include_out_of_range" not in config else int(config["include_out_of_range"])

    # stats
    stats = []
    for band in range(ds.RasterCount):
        band += 1
        # TODO: handle better min max
        if min is None and max is None:
            if force:
                (min, max) = ds.GetRasterBand(band).ComputeRasterMinMax(0)
            else:
                min = ds.GetRasterBand(band).GetMinimum()
                max = ds.GetRasterBand(band).GetMaximum()
        #hist = ds.GetRasterBand(band).GetDefaultHistogram( force = 0 )
        #stats.append({"band": band, "buckets": hist[2], "min": hist[0], "max": hist[1], "values": hist[3]})
        hist = ds.GetRasterBand(band).GetHistogram(buckets=buckets, min=min, max=max, include_out_of_range=include_out_of_range, approx_ok = False )
        stats.append({"band": band, "buckets": buckets, "min": min, "max": max, "values": hist})
    return stats



def get_nodata_value(file_path, band=1):
    try:
        with rasterio.open(file_path) as src:
            return "none" if "nodata" not in src.meta else str(src.meta["nodata"])
    except Exception, e:
        log.error(e)
        raise Exception(e)

# def get_nodata_value(file_path, band=1):
#     ds = gdal.Open(file_path)
#     return ds.GetRasterBand(band).GetNoDataValue()


def get_authority(file_path):
    '''
    Get the authority used by a raster i.e. EPSG:4326
    :param file_path: path to the file
    :return: return the SRID of the raster projection
    '''
    with rasterio.open(file_path) as src:
        log.info(src.meta)
        if 'init' in src.meta['crs']:
            return src.meta['crs']['init']
        elif 'proj' in src.meta['crs']:
            return src.meta['crs']['proj']
    return None

def get_srid(file_path):
    '''
    Get the SRID of a raster (i.e. 4326 or 3857 and not EPSG:4326)
    :param file_path: path to the file
    :return: return the SRID of the raster projection
    '''
    proj = get_authority(file_path)
    if ":" in proj:
        return proj.split(":")[1]
    if proj.isdigit():
        return proj
    return None