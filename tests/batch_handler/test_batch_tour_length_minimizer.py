import unittest
import importlib.util
import os
from tabulate import tabulate
from src.batch_handler.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from src.batch_handler.batch_tour_length_minimizer import create_start_batches, local_search_shift, local_search_swap
from src.data_handler.join_item_information import join_item_id_and_position_csv
from tests.data.test_batch import warehouse_layout

class TestBatchTourLengthMinimizer(unittest.TestCase):
    '''
    This class contains the unit tests for the batch tour length minimizer.
    '''
    # Path to the test orders
    dataset_orders_path = os.path.join('tests', 'data', 'test_orders.py')
    dataset_csv_path = os.path.join('tests', 'data', 'warehouse_positions_20x10x5.CSV')
    # Maximum batch size
    max_batch_size = 15


    def load_orders(self, path):
        '''
        This function loads the test orders from the specified path.
        :param path: The path to the test orders.
        '''
        # Load the test orders
        spec = importlib.util.spec_from_file_location("test_orders", path)
        # Check if the file exists
        if spec is None:
            raise FileNotFoundError(f"File not found: {path}")
        # Load the module
        orders_module = importlib.util.module_from_spec(spec)
        # Execute the module
        spec.loader.exec_module(orders_module)
        return orders_module.test_orders


    def add_positions_to_items(self, orders, dataset_csv_path):
        '''
        This function adds the positions to the items in the orders.
        :param orders: The orders to which the positions should be added.
        :param dataset_csv_path: The path to the dataset CSV file.
        '''
        # Add the positions to the items
        for order in orders:
            for item in order['items']:
                # Update the item with the position
                item.update(join_item_id_and_position_csv(dataset_csv_path, item['item_id']))
        return orders


    def test_create_start_batches(self):
        '''
        This function tests the creation of the start batches.
        '''
        # Load the test orders
        orders = self.load_orders(self.dataset_orders_path)
        # Call the function to create the start batches
        batches = create_start_batches(orders, self.max_batch_size)

        # Print the initial batches
        print("Initial Batches")
        for batch in batches:
            table_data = []
            for order in batch['orders']:
                for item in order['items']:
                    table_data.append([order['order_id'], item['item_id']])

            headers = ["Order ID", "Item ID"]
            table = tabulate(table_data, headers, tablefmt="simple_grid", showindex="always")
            print(f"Batch {batch['batch_id']}")
            print(table)
            print("\n")

        # Check the batch sizes
        for batch in batches:
            # Check if the batch size is less than or equal to the maximum batch size
            self.assertLessEqual(len(batch['orders']), self.max_batch_size, f"Batch size exceeds the maximum batch size of {self.max_batch_size}")
            # Check if the batch is not empty
            self.assertGreater(len(batch['orders']), 0, "Batch is empty")

        # Store the order IDs
        order_ids = [order['order_id'] for batch in batches for order in batch['orders']]
        # Store the expected order IDs
        expected_order_ids = [order['order_id'] for order in orders]
        # Check if the order IDs and the expected order IDs match
        self.assertCountEqual(order_ids, expected_order_ids, "Returned orders do not match the expected orders")

        seen_order_ids = set()
        for order_id in order_ids:
            #Check if the order ID appears in multiple batches, which means it has been split
            self.assertNotIn(order_id, seen_order_ids, f"Order ID {order_id} appears in multiple batches")
            # Add the order ID to the set
            seen_order_ids.add(order_id)

        # Check the batch sizes
        self.check_batch_sizes(batches, self.max_batch_size)


    def test_local_search_swap(self):
        '''
        This function tests the local search swap algorithm.
        '''
        # Load the test orders
        orders = self.load_orders(self.dataset_orders_path)
        orders = self.add_positions_to_items(orders, self.dataset_csv_path)
        # Create the start batches
        start_batches = create_start_batches(orders, self.max_batch_size)
        # Calculate the total tour length of the initial batches        
        start_batches_tour_length = self.calculate_total_tour_length(start_batches, warehouse_layout)
        # Improve the batches using the local search swap algorithm
        improved_batches = local_search_swap(start_batches, self.max_batch_size, warehouse_layout)

        # Print the improved batches
        for batch in improved_batches:
            table_data = []
            for order in batch['orders']:
                for item in order['items']:
                    table_data.append([order['order_id'], item['item_id']])

            headers = ["Order ID", "Item ID"]
            table = tabulate(table_data, headers, tablefmt="simple_grid", showindex="always")
            print(f"Improved Batch {batch['batch_id']}")
            print(table)
            print("\n")

        # Calculate the total tour length of the improved batches and print the results
        improved_batches_tour_length = self.calculate_total_tour_length(improved_batches, warehouse_layout)
        print(f"Total tour length of initial batches: {start_batches_tour_length}")
        print(f"Total tour length of improved batches: {improved_batches_tour_length}")

        # Check if the total tour length of the improved batches is less than the total tour length of the initial batches
        # If the total tour length of the improved batches is not less this could be due to a too small maximum batch size
        self.assertLess(improved_batches_tour_length, start_batches_tour_length, "Total tour length of improved batches is not less than the total tour length of the initial batches")
        
        # Check the batch sizes
        self.check_batch_sizes(improved_batches, self.max_batch_size)


    def test_local_search_shift(self):
        '''
        This function tests the local search shift algorithm.
        '''
        # Load the test orders
        orders = self.load_orders(self.dataset_orders_path)
        orders = self.add_positions_to_items(orders, self.dataset_csv_path)
        # Create the start batches
        start_batches = create_start_batches(orders, self.max_batch_size)
        # Calculate the total tour length of the initial batches
        start_batches_tour_length = self.calculate_total_tour_length(start_batches, warehouse_layout)
        # Improve the batches using the local search shift algorithm
        improved_batches = local_search_shift(start_batches, self.max_batch_size, warehouse_layout)
        
        # Print the improved batches
        for batch in improved_batches:
            table_data = []
            for order in batch['orders']:
                for item in order['items']:
                    table_data.append([order['order_id'], item['item_id']])

            headers = ["Order ID", "Item ID"]
            table = tabulate(table_data, headers, tablefmt="simple_grid", showindex="always")
            print(f"Improved Batch {batch['batch_id']}")
            print(table)
            print("\n")

        # Calculate the total tour length of the improved batches and print the results
        improved_batches_tour_length = self.calculate_total_tour_length(improved_batches, warehouse_layout)
        print(f"Total tour length of initial batches: {start_batches_tour_length}")
        print(f"Total tour length of improved batches: {improved_batches_tour_length}")

        # Check if the total tour length of the improved batches is less than the total tour length of the initial batches
        self.assertLess(improved_batches_tour_length, start_batches_tour_length, "Total tour length of improved batches is not less than the total tour length of the initial batches")

        # Check the batch sizes
        self.check_batch_sizes(improved_batches, self.max_batch_size)


    def calculate_total_tour_length(self, batches, warehouse_layout):
        '''
        This function calculates the total tour length of the batches.

        :param batches: The batches for which the total tour length should be calculated.
        :param warehouse_layout: The warehouse layout.
        :return: The total tour length of the batches.
        '''
        total_length = 0
        # Calculate the total tour length of the batches
        for batch in batches:
            tour_length, _ = calculate_tour_length_s_shape_routing(batch, warehouse_layout)
            total_length += tour_length
        return total_length


    def check_batch_sizes(self, batches, max_batch_size):
        '''
        This function checks if the batch sizes exceed the maximum batch size and if the batches are empty.
        '''
        for batch in batches:
            # Check if the batch size is less than or equal to the maximum batch size
            self.assertLessEqual(len(batch['orders']), max_batch_size, f"Batch size exceeds the maximum batch size of {max_batch_size}")
            # Check if the batch is not empty
            self.assertGreater(len(batch['orders']), 0, "Batch is empty")


if __name__ == '__main__':
    unittest.main()
