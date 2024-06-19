import unittest
import importlib.util
from src.batch_handler.batch_tour_length_minimizer import create_start_batches
from tabulate import tabulate

class TestBatchTourLengthMinimizer(unittest.TestCase):
    dataset_path = 'tests/data/test_orders.py'

    def load_orders(self, path):
        spec = importlib.util.spec_from_file_location("test_orders", path)
        orders_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(orders_module)
        return orders_module.test_orders

    def test_create_start_batches(self):
        max_batch_size = 15

        # Load orders from the dataset path
        orders = self.load_orders(self.dataset_path)

        # Call the function
        batches = create_start_batches(orders, max_batch_size)
       
       
       # Prepare and print tables for each batch
        for batch in batches:
            table_data = []
            for order in batch['orders']:
                for item in order['items']:
                    table_data.append([
                        order['order_id'],
                        item['item_id'],
                    ])

            headers = ["Order ID", "Item ID"]
            table = tabulate(table_data, headers, tablefmt="simple_grid", showindex="always")

            # Print batch information and the table
            print(f"Batch {batch['batch_id']}")
            print(table)
            print("\n")
        


        for batch in batches:
            # Check if the batch size is within the limits
            self.assertLessEqual(len(batch['orders']), max_batch_size, f"Batch size exceeds the maximum batch size of {max_batch_size}")
            self.assertGreater(len(batch['orders']), 0, "Batch is empty")

        # Check if the returned orders match the expected orders
        order_ids = [order['order_id'] for batch in batches for order in batch['orders']]
        expected_order_ids = [order['order_id'] for order in orders]
        self.assertCountEqual(order_ids, expected_order_ids, "Returned orders do not match the expected orders")

        # Check if orders got split into multiple batches, which means that the same order id appears in multiple batches
        seen_order_ids = set()
        for order_id in order_ids:
            self.assertNotIn(order_id, seen_order_ids, f"Order ID {order_id} appears in multiple batches")
            seen_order_ids.add(order_id)

if __name__ == '__main__':
    unittest.main()
