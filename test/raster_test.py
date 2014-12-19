import unittest
from geobricks_gis_raster.core import raster, raster_mapalgebra


class GeobricksTest(unittest.TestCase):

    def test_get_nodata(self):
        print "test_get_authority"
        path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MCD12Q1/processed_2001/4326/final_4326.tiff"
        result = raster.get_nodata_value(path)
        print result
        self.assertEqual(result, True)

    # def test_get_nodata(self):
    #     print "here1"
    #     self.assertEqual(True, True)
    #
    # def test_mapalgebra_mask(self):
    #     print "here2"
    #     self.assertEqual(True, True)

