import unittest
import pandas as pd
from src.core.join_item_information import join_item_id_and_position_csv
from tabulate import tabulate

class TestJoinItemInformation(unittest.TestCase):
    dataset_path = 'tests/data/warehouse_positions_20x10x5.CSV'

    def test_get_item_with_position_existing_item(self):
        # Test for an existing item
        item_id = 1
        expected_output = {'item_id': 1, 'abs_x_position': 0, 'abs_y_position': 0, 'abs_z_position': 0}
        result = join_item_id_and_position_csv(self.dataset_path, item_id)
        
        # Print the result in a table
        table_data = list(result.items())
        headers = ["Field", "Value"]
        print(f"Returned values for item_id {item_id}:")
        print(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

        self.assertEqual(result, expected_output)

    def test_get_item_with_position_non_existing_item(self):
        # Test for a non-existing item
        item_id = 9999
        with self.assertRaises(ValueError) as context:
            join_item_id_and_position_csv(self.dataset_path, item_id)
        self.assertTrue(f"Item ID {item_id} not found in the dataset." in str(context.exception))

    def test_non_integer_values_in_row(self):
        # Test for non-integer values in the specified row
        item_id = 1001
        with self.assertRaises(ValueError) as context:
            join_item_id_and_position_csv(self.dataset_path, item_id)
        self.assertTrue("The value in column abs_z_position is not an integer." in str(context.exception))


if __name__ == '__main__':
    unittest.main()
