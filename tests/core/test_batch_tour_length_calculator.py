import unittest
from src.core.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from tests.data.test_batch import test_batches, warehouse_layout
from tabulate import tabulate

class TestBatchTourLengthHandler(unittest.TestCase):
    
    def test_calculate_tour_length_s_shape_routing(self):
        '''
        This function tests the calculate_tour_length_s_shape_routing function.
        '''
        for i, batch in enumerate(test_batches):
            with self.subTest(batch=i):
                # Wrap the batch in the expected structure like it would be in the process
                wrapped_batch = {'orders': [{'items': batch}]}

                # Calculate the tour length
                result, sorted_batch = calculate_tour_length_s_shape_routing(wrapped_batch, warehouse_layout)
                # Print the result
                print(f"Batch {i} tour length: {result}")
                
                 # Prepare the table
                table_data = [[item['item_id'], item['abs_x_position'], item['abs_y_position'], item['abs_z_position']] for item in sorted_batch]
                headers = ["Item ID", "Aisle No.", "Y Position", "Z Position"]
                
                # Print table using tabulate
                print(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

                print("\n")
                
                # Check if the result is a int
                self.assertIsInstance(result, int, f"Test batch {i} failed: Result is not an int")

                # Additional checks to ensure batch 1 and 2 have the same distance, as they are the same batch in different order (see test_batch.py)
                if i == 1:
                    batch_1_result = result
                if i == 2:
                    batch_2_result = result
                    self.assertEqual(batch_1_result, batch_2_result, f"Test batch 1 and 2 failed: Distances do not match")

                # Additional checks to ensure batch 10 and 11 have the same distance, as they are the same batch in different order with one duplicate (see test_batch.py)
                if i == 10:
                    batch_10_result = result
                if i == 11:
                    batch_11_result = result
                    self.assertEqual(batch_10_result, batch_11_result, f"Test batch 10 and 11 failed: Distances do not match")


if __name__ == '__main__':
    unittest.main()
