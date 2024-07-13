import datetime
import importlib
import os
import random
import time
import unittest

from src.core.logic.batch_selector import calculate_delay_single_batch
from src.core.logic.batch_tour_length_minimizer import create_start_batches
from src.core.logic.join_item_information import join_item_id_and_position_csv
from src.vars import shared_variables
from tests.data.test_batch import warehouse_layout

class TestBatchSelector(unittest.TestCase):
    '''
    This class contains the unit tests for the batch selector.
    '''
    # Path
    # Path to the test orders
    dataset_orders_path = os.path.join('tests', 'data', 'test_orders.py')
    dataset_csv_path = os.path.join('tests', 'data', 'warehouse_positions.CSV')
    # Maximum batch size
    max_batch_size = 15
    # Release parameter
    release_parameter = 0.6

    def setUp(self):
        # Set up the shared variables
        shared_variables.variables = {
            'tour_length_units_per_second': 20
    }

    def test_calculate_delay_single_batch(self):
        '''
        Test the calculation of the delay for a single batch.
        '''
        # Load the test orders
        orders = self.load_orders(self.dataset_orders_path)[:5]
        orders = self.add_positions_to_items(orders, self.dataset_csv_path)
        # Add random arrival times to the orders
        for order in orders:
            # Generate a random arrival time in the last five minutes
            arrival_time = random.randint(0, 5*60)
            order['arrival_time'] = time.time() - arrival_time

        # Create batches
        start_batches = create_start_batches(orders, self.max_batch_size)
        # Get the first batch
        batch = start_batches[0]

        # Get the current time
        current_time = time.time()
        current_time_ts = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
        # Calculate the delay
        batch = calculate_delay_single_batch(batch, warehouse_layout, self.release_parameter)
        # Get the release time
        delay = float(batch['release_time']) - current_time

        # Print the delay
        print(f"Delay: {delay}")
        # Check if the delay is positive
        self.assertGreaterEqual(delay, 0)


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