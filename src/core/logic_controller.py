import threading
import time

from src.core.logic.input_handler import get_initial_order_release, get_input_process_running, get_max_batch_size, get_new_order, get_rearrangement_parameter, get_selection_rule, get_threshold_parameter, get_time_limit, get_warehouse_layout, is_new_order_available
from src.core.logic.pivot_logic import last_order_arrives, new_order_arrives,  picker_starts_tour

import src.vars.shared_variables as shared_variables



orders = []
current_sorted_batches = []
current_picking_batch = {}
current_picking_process_start_time = 0
current_picking_process_arrival_time = 0

# Get the shared variables
warehouse_layout = get_warehouse_layout()
max_batch_size = get_max_batch_size()
initial_order_release = get_initial_order_release()
rearrangement_parameter = get_rearrangement_parameter()
threshold_parameter = get_threshold_parameter()
time_limit = get_time_limit()
selection_rule = get_selection_rule()
input_process_running = get_input_process_running()


class LogicThread(threading.Thread):
    '''
    Thread class for the logic controller
    '''
    def __init__(self, cli_controller, logic_function):
        '''
        Constructor

        :param cli_controller: CLIController
        :param logic_function: function
        '''
        super().__init__()
        self.cli_controller = cli_controller
        self.logic_function = logic_function
    
    def run(self):
        '''
        Run the logic controller
        '''
        self.cli_controller.ready.wait()
        self.logic_function(self.cli_controller.variables)


    def logic_function(variables):
        '''
        Logic function for the logic controller

        :param variables: dict
        '''
        # Loops while the input process is running
        while input_process_running() == True:
            # Check if a new order is available
            if is_new_order_available() == True:
                # Get the new order
                order = get_new_order()
                # Pass the new order and receive batches with release times
                current_sorted_batches = new_order_arrives(order, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, initial_order_release, selection_rule, orders)
            else:
                # Check if the current picking process has already started
                if current_picking_process_arrival_time > time.time():
                    break
                else:
                    # Iterate over the sorted batches
                    for batch in current_sorted_batches:
                        # Check if the batch is ready to be picked
                        if batch['release_time'] < time.time():
                            current_picking_batch, current_picking_process_start_time, current_picking_process_arrival_time = picker_starts_tour(batch, warehouse_layout)
                            current_sorted_batches.remove(batch)

                            # Store the current batch in the shared variables
                            shared_variables.variables['current_picking_batch'] = current_picking_batch
                            # Store the current picking process start time in the shared variables
                            shared_variables.variables['current_picking_process_start_time'] = current_picking_process_start_time
                            # Store the current picking process arrival time in the shared variables
                            shared_variables.variables['current_picking_process_arrival_time'] = current_picking_process_arrival_time
                            # As the batch is picked, break the loop
                            break

            # Update the input process running variable
            input_process_running = get_input_process_running()

        # As the input process is finished, the last batches are sorted and released
        # Sort the last existing batches and release them sequentially
        current_sorted_batches = last_order_arrives(order, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit, orders)
        # Loops after the input process is finished to process the remaining batches
        while len(current_sorted_batches) > 0:
            # Check if the current picking process has already started
            if current_picking_process_arrival_time > time.time():
                    break
            else:
                # Iterate over the sorted batches
                for batch in current_sorted_batches:
                    # Check if the batch is ready to be picked
                    if batch['release_time'] < time.time():
                        # Start the picking process
                        current_picking_batch, current_picking_process_start_time, current_picking_process_arrival_time = picker_starts_tour(batch, warehouse_layout)
                        # Remove the batch from the list of sorted batches
                        current_sorted_batches.remove(batch)
                        # Store the current batch in the shared variables
                        shared_variables.variables['current_picking_batch'] = current_picking_batch
                        # Store the current picking process start time in the shared variables
                        shared_variables.variables['current_picking_process_start_time'] = current_picking_process_start_time
                        # Store the current picking process arrival time in the shared variables
                        shared_variables.variables['current_picking_process_arrival_time'] = current_picking_process_arrival_time
                        # Break the loop
                        break

    
        
