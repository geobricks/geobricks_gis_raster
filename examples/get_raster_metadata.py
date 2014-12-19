from geobricks_gis_raster.core import raster

try:
    print "test"
    path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MCD12Q1/processed_2001/4326/final_4326.tiff"
    path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MCD12Q1/processed_2001/0.hdf"
    path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/cultivation_organic_soils/3857/cultivation_organic_soils_croplands_3857.tif"
    #path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/Climate_Zones_processed/JRC_CLIMATE_ZONE_0.25deg_3857.tif"
    #path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/Climate_Zones_processed/JRC_CLIMATE_ZONE_0.25deg_4326.tif"

    # multiband
    # path = "/home/vortex/Desktop/LAYERS/MODIS_5600/MODIS_03_2014.hdf"
    print path
    #result = raster.get_nodata_value(path)
    result = raster.get_authority(path)

    print result
except Exception, e:
    print(e)


