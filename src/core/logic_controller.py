import threading
import time

import click
from src.core.logic.input_handler import (
    get_initial_order_release, get_input_process_running, get_max_batch_size, 
    get_new_order, get_rearrangement_parameter, get_release_parameter, get_selection_rule, 
    get_threshold_parameter, get_time_limit, get_warehouse_layout, 
    is_new_order_available
)
from src.core.logic.pivot_logic import initial_orders_arrived, last_order_arrives, new_order_arrives, picker_starts_tour
import src.vars.shared_variables as shared_variables

class LogicThread(threading.Thread):
    '''
    Class for the logic thread
    '''
    def __init__(self, event, variables):
        '''
        Constructor of the logic thread

        :param event: Event to signal the initialization of the thread
        :param variables: Variables for the thread
        '''
        # Call the constructor of the parent class
        super().__init__()
        # Set the event
        self.event = event
        # Set the variables
        self.variables = variables
        # If debug mode is enabled, print the variables
        if shared_variables.variables.get('debug_mode'):
            click.echo(f'LogicThread initialized with variables: {self.variables}\n')

    
    def run(self):
        '''
        Run method of the logic thread
        '''
        # Set the debug mode
        debug_mode = shared_variables.variables.get('debug_mode')
        try:
            # If debug mode is enabled, print a message
            if debug_mode:
                click.echo('LogicThread running\n')
            # Update the shared variables with the variables of the thread
            shared_variables.variables.update(self.variables)
            # Call the logic function
            self.logic_function()
        # Catch exceptions
        except Exception as e:
            click.echo(f'LogicThread encountered an error: {e}')
        # Finally, print a message that the run method has completed
        finally:
            if debug_mode:
                click.echo('LogicThread run method completed')


    def logic_function(self):
        '''
        Logic function of the logic thread
        '''
        try:
            # Get the variables from the shared variables and store them in local variables
            warehouse_layout = get_warehouse_layout()
            max_batch_size = get_max_batch_size()
            initial_order_release = get_initial_order_release()
            rearrangement_parameter = get_rearrangement_parameter()
            threshold_parameter = get_threshold_parameter()
            release_parameter = get_release_parameter()
            time_limit = get_time_limit()
            selection_rule = get_selection_rule()
            input_process_running = get_input_process_running()
            
            # Store the variables in a dictionary
            variables = {
                'warehouse_layout': warehouse_layout,
                'max_batch_size': max_batch_size,
                'initial_order_release': initial_order_release,
                'rearrangement_parameter': rearrangement_parameter,
                'threshold_parameter': threshold_parameter,
                'release_parameter': release_parameter,
                'time_limit': time_limit,
                'selection_rule': selection_rule,
                'input_process_running': input_process_running
            }

            # If debug mode is enabled, print the variables
            if shared_variables.variables.get('debug_mode'):
                click.echo(f'LogicThread variables: {variables}\n')
            
            orders = []
            current_sorted_batches = []
            current_picking_batch = {}
            current_picking_process_start_time = 0
            current_picking_process_arrival_time = 0
            
            # Get the initial order release
            orders = [get_new_order() for _ in range(initial_order_release)]
            # Create a batch for the initial order release
            current_sorted_batches = initial_orders_arrived(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule)
            print(current_sorted_batches)
            # Loops while the input process is running
            while input_process_running:
                print('LogicThread loop running')
                # Check if a new order is available
                if is_new_order_available():
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
                                print(f'Batch picked: {current_picking_batch}')
                                # As the batch is picked, break the loop
                                break

                # Update the input process running variable
                input_process_running = get_input_process_running()

            # As the input process is finished, the last batches are sorted and released
            # Sort the last existing batches and release them sequentially
            current_sorted_batches = last_order_arrives(order, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit, orders)
            # Loops after the input process is finished to process the remaining batches
            while len(current_sorted_batches) > 0:
                print('Processing remaining batches')
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
                            print(f'Batch picked: {current_picking_batch}')
                            # Break the loop
                            break
        except Exception as e:
            print(f'Logic function encountered an error: {e}')
