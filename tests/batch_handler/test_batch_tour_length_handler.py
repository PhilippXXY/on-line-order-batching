import unittest
from src.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from tests.data.test_batch_10 import test_batches, warehouse_layout

class TestBatchTourLengthHandler(unittest.TestCase):
    
    def test_calculate_tour_length_s_shape_routing(self):
        for i, batch in enumerate(test_batches):
            with self.subTest(batch=i):
                result = calculate_tour_length_s_shape_routing(batch, warehouse_layout)
                self.assertIsInstance(result, float, f"Test batch {i} failed: Result is not a float")

if __name__ == '__main__':
    unittest.main()