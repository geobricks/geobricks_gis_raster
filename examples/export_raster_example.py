from geobricks_gis_raster.core.raster import crop_by_vector_database, get_statistics, get_authority
from geobricks_gis_raster.config.config import config
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
import rasterio

config = config["settings"]

# request (to be passed to the distribution service)
r = {
    "raster": {
        "uids":["fenix:gfed4_burnedarea_lc_12_2012"]
    },
    "vector": {
        "query_extent": "SELECT ST_AsGeoJSON(ST_Transform(ST_SetSRID(ST_Extent(geom), 3857), {{SRID}})) FROM {{SCHEMA}}.gaul0_2014_2013_3857 WHERE adm0_code IN ('122')",
        "query_layer":  "SELECT * FROM {{SCHEMA}}.gaul0_2014_2013_3857 WHERE adm0_name IN ('Portugal')"
    }
}


# DB Instance
db_spatial = DBMSPostgreSQL(config["db"]["spatial"])

# queries
raster_path = "../test_data/MODIS/MOD13A2/MOD13A2_3857.tif"
query_extent = "SELECT ST_AsGeoJSON(ST_Transform(ST_SetSRID(ST_Extent(geom), 3857), 3857)) FROM spatial.gaul0_2014_2013_3857 WHERE adm0_name IN ('Portugal')"
query_layer = "SELECT * FROM spatial.gaul0_2014_2013_3857 WHERE adm0_name IN ('Portugal')"

# cutting the layer
result = crop_by_vector_database(raster_path, db_spatial, query_extent, query_layer)
print result
print get_statistics(result)
print get_authority(result)

