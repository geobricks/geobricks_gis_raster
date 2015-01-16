import unittest
import os
from geobricks_gis_raster.core.raster import get_location_values, get_srid, get_authority, get_nodata_value, get_histogram, get_descriptive_statistics, get_statistics


class GeobricksTest(unittest.TestCase):

    def test_get_nodata(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        result = get_nodata_value(path)
        self.assertEqual(result, '8.99999982852e+20')

    def test_get_statistics(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        result = get_statistics(path)
        self.assertEqual(result, {'hist': [{'band': 1, 'buckets': 256, 'values': [2038201, 37421, 20886, 13506, 9780, 7553, 6260, 5304, 4485, 4115, 3789, 3437, 3115, 3324, 2229, 1952, 1919, 1808, 1745, 1584, 1486, 1468, 1299, 1146, 1144, 1139, 1053, 961, 924, 879, 794, 818, 747, 788, 724, 709, 677, 643, 595, 626, 552, 581, 602, 494, 507, 420, 463, 466, 418, 410, 432, 364, 368, 362, 424, 315, 319, 260, 275, 235, 250, 232, 211, 205, 230, 207, 200, 228, 212, 209, 202, 174, 213, 238, 153, 165, 134, 158, 161, 122, 116, 112, 103, 119, 117, 93, 97, 106, 95, 78, 82, 90, 96, 86, 69, 105, 91, 76, 83, 76, 78, 88, 92, 59, 76, 90, 61, 69, 96, 81, 60, 64, 52, 70, 56, 52, 72, 62, 89, 58, 82, 69, 63, 64, 78, 42, 62, 37, 40, 47, 59, 41, 39, 48, 33, 52, 38, 35, 58, 32, 22, 26, 19, 26, 25, 12, 20, 12, 13, 18, 21, 41, 17, 10, 10, 9, 17, 9, 30, 10, 6, 7, 11, 4, 7, 3, 7, 7, 4, 1, 8, 5, 6, 6, 17, 10, 6, 4, 6, 6, 9, 6, 8, 8, 4, 6, 10, 5, 7, 7, 24, 4, 0, 3, 18, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 2, 5, 0, 0, 5, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 'max': 1.9333192110061646, 'min': 0.0}], 'stats': [{'band': 1, 'max': 1.9333192110061646, 'mean': 0.008779648138849024, 'sd': 0.056981237827174326, 'min': 0.0}]})

    def test_get_histogram(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        result = get_histogram(path)
        self.assertEqual(result, [{'band': 1, 'buckets': 256, 'values': [2038201, 37421, 20886, 13506, 9780, 7553, 6260, 5304, 4485, 4115, 3789, 3437, 3115, 3324, 2229, 1952, 1919, 1808, 1745, 1584, 1486, 1468, 1299, 1146, 1144, 1139, 1053, 961, 924, 879, 794, 818, 747, 788, 724, 709, 677, 643, 595, 626, 552, 581, 602, 494, 507, 420, 463, 466, 418, 410, 432, 364, 368, 362, 424, 315, 319, 260, 275, 235, 250, 232, 211, 205, 230, 207, 200, 228, 212, 209, 202, 174, 213, 238, 153, 165, 134, 158, 161, 122, 116, 112, 103, 119, 117, 93, 97, 106, 95, 78, 82, 90, 96, 86, 69, 105, 91, 76, 83, 76, 78, 88, 92, 59, 76, 90, 61, 69, 96, 81, 60, 64, 52, 70, 56, 52, 72, 62, 89, 58, 82, 69, 63, 64, 78, 42, 62, 37, 40, 47, 59, 41, 39, 48, 33, 52, 38, 35, 58, 32, 22, 26, 19, 26, 25, 12, 20, 12, 13, 18, 21, 41, 17, 10, 10, 9, 17, 9, 30, 10, 6, 7, 11, 4, 7, 3, 7, 7, 4, 1, 8, 5, 6, 6, 17, 10, 6, 4, 6, 6, 9, 6, 8, 8, 4, 6, 10, 5, 7, 7, 24, 4, 0, 3, 18, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 2, 5, 0, 0, 5, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 'max': 1.9333192110061646, 'min': 0.0}])

    def test_get_descriptive_statistics(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        result = get_descriptive_statistics(path)
        self.assertEqual(result, [{'band': 1, 'max': 1.9333192110061646, 'mean': 0.008779648138849024, 'sd': 0.056981237827174326, 'min': 0.0}])

    def test_get_srid(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        result = get_srid(path)
        self.assertEqual(result, '4326')

    def test_get_authority(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        result = get_authority(path)
        self.assertEqual(result, 'epsg:4326')

    def test_get_location_values(self):
        path = "../test_data/storage/raster/rice_area_4326/rice_area_4326.geotiff"
        path = [os.path.normpath(os.path.join(os.path.dirname(__file__), path))]
        result = get_location_values(path, 45.1709201, 7.985972)
        self.assertEqual(result, ['0.1346156001091'])


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()

