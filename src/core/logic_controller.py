import copy
import datetime
import threading
import time
import traceback
import click
from src.core.logic.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from src.core.logic.input_handler import (
    get_initial_order_release, get_input_process_running, get_last_order, get_max_batch_size, 
    get_new_order, get_rearrangement_parameter, get_release_parameter, get_selection_rule, 
    get_threshold_parameter, get_time_limit, get_warehouse_layout, get_warehouse_layout_path, 
    is_new_order_available
)
from src.core.logic.pivot_logic import initial_orders_arrived, last_order_arrives, new_order_arrives, one_batch_available, picker_starts_tour
import tabulate
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

    
    def run(self):
        '''
        Run method of the logic thread
        '''
        # Set the debug mode
        debug_mode = shared_variables.variables.get('debug_mode')
        try:
            # If debug mode is enabled, print a message
            if debug_mode:
                click.secho('LogicThread running\n', fg='yellow')
            # Update the shared variables with the variables of the thread
            shared_variables.variables.update(self.variables)
            # Set the logic function variable to running
            shared_variables.variables['logic_function_running'] = True
            # Call the logic function
            self.logic_function()
        # Catch exceptions
        except Exception as e:
            click.secho(f'LogicThread encountered an error: {e}', fg='red')
            if debug_mode:
                click.secho(traceback.print_exc(), fg='red')
        # Finally, print a message that the run method has completed
        finally:
            # Set the logic function variable to not running
            shared_variables.variables['logic_function_running'] = False
            # If debug mode is enabled, print a message
            if debug_mode:
                click.secho('LogicThread run method completed', fg='yellow')


    def logic_function(self):
        '''
        Logic function of the logic thread
        '''
        try:
            # Get the variables from the shared variables and store them in local variables
            warehouse_layout = get_warehouse_layout()
            warehouse_layout_path = get_warehouse_layout_path()
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
                click.secho(f'Variables passed to LogicThread from shared variables: {variables}\n', fg='yellow')
            
            all_orders = []
            current_sorted_batches = []
            current_picking_batch = {}
            current_picking_process_start_time = 0
            current_picking_process_arrival_time = 0
            batch_information_temp = {'orders': []}
            shared_variables.variables['last_batching_process_finished'] = False
            
            # Get the initial order release
            all_orders = copy.deepcopy([get_new_order() for _ in range(initial_order_release)])
            # Create a batch for the initial order release
            current_sorted_batches = copy.deepcopy(initial_orders_arrived(all_orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule))
            # Remove batches with empty orders
            current_sorted_batches = [batch for batch in current_sorted_batches if len(batch['orders']) > 0]

            # Log initial orders and batches
            if shared_variables.variables.get('debug_mode'):
                click.secho('Initial batches:', fg='yellow')
                debug_print_batches(current_sorted_batches)
                click.secho('Initial orders:', fg='yellow')
                debug_print_orders(all_orders)

            # Loops while the input process is running
            while input_process_running:
                # Check if for the current batch the picking process has already ended
                if time.time() < current_picking_process_arrival_time:
                    # Set the picker state to False (not available)
                    shared_variables.picker_state = False
                else:
                    # Set the picker state to True (available)
                    shared_variables.picker_state = True
                # Check if a new order is available and create with them new optimized batches
                if is_new_order_available():
                    # Get the new order
                    order = get_new_order()
                    if shared_variables.variables.get('debug_mode'):
                        click.secho(f'New order arrived:', fg='yellow')
                        debug_print_orders([order])
                        click.secho(f'Current orders:', fg='yellow')
                        debug_print_orders(all_orders)
                    # Pass the new order and receive batches with release times
                    current_sorted_batches = copy.deepcopy(new_order_arrives(order, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule, all_orders))
                    # Remove batches with empty orders
                    current_sorted_batches = [batch for batch in current_sorted_batches if len(batch['orders']) > 0]
                # If no new order is available, release the current batches
                else:
                    # Check if the current picking process has already started
                    if current_picking_process_arrival_time > time.time():
                        # Avoid busy waiting
                        time.sleep(0.05)
                        continue
                    # If the current picking process has not started, start it with the next batch
                    else:
                        for batch in current_sorted_batches:
                            # Check if the batch is ready to be picked
                            if batch['release_time'] < time.time():
                                # Check if there is only one batch left and the orders are different
                                if len(current_sorted_batches) == 1 and batch_information_temp['orders'] != batch['orders']:
                                    # Store the current batch information
                                    batch_information_temp = copy.deepcopy(current_sorted_batches[0])
                                    # Call the one_batch_available function to get a new release time
                                    one_batch_available(all_orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule)
                                # Start the picking process
                                else:
                                    current_picking_batch, current_picking_process_start_time, current_picking_process_arrival_time = picker_starts_tour(batch, warehouse_layout)
                                  
                                    # Store the current batch in the shared variables
                                    shared_variables.variables['current_picking_batch'] = current_picking_batch
                                    # Store the current picking process start time in the shared variables
                                    shared_variables.variables['current_picking_process_start_time'] = current_picking_process_start_time
                                    # Store the current picking process arrival time in the shared variables
                                    shared_variables.variables['current_picking_process_arrival_time'] = current_picking_process_arrival_time
                                   
                                    # Remove the orders of the current batch from the list of all orders
                                    for batch_order in current_picking_batch['orders']:
                                        for all_order in all_orders:
                                            if batch_order['order_id'] == all_order['order_id']:
                                                all_orders.remove(all_order)
                    
                                    # Remove the batch from the list of sorted batches
                                    current_sorted_batches.remove(batch)

                                    # Print for debugging purposes
                                    if shared_variables.variables.get('debug_mode'):
                                        click.secho(f'Released batch with release time: {datetime.datetime.fromtimestamp(batch['release_time']).strftime('%H:%M:%S.%f')[:-5]} and arrival time: {datetime.datetime.fromtimestamp(current_picking_process_arrival_time).strftime('%H:%M:%S.%f')[:-5]}', fg='yellow')
                                        debug_print_batches([batch])
                    
                                    break

                # Update the amount of existing batches
                shared_variables.variables['amount_of_existing_batches'] = len(current_sorted_batches)
                # Update the amount of existing orders
                shared_variables.variables['amount_of_existing_orders'] = len(all_orders)
                # Update the input process running variable
                input_process_running = get_input_process_running()
                # Avoid busy waiting
                time.sleep(0.05)
            
            # As the input process is finished, the last batches are sorted and released
            # Get the last order
            order = get_last_order()

            # Sort the last existing batches and release them sequentially
            current_sorted_batches = last_order_arrives(copy.deepcopy(order), max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, selection_rule, copy.deepcopy(all_orders))
            # Update the amount of existing batches
            shared_variables.variables['amount_of_existing_batches'] = len(current_sorted_batches)
            # Set a flag that the last batching process is finished
            shared_variables.variables['last_batching_process_finished'] = True

            # Loops after the input process is finished to process the remaining batches
            while len(current_sorted_batches) > 0:

                if time.time() < current_picking_process_arrival_time:
                    # Set the picker state to False (not available)
                    shared_variables.picker_state = False
                else:
                    # Set the picker state to True (available)
                    shared_variables.picker_state = True

                    # Go through the remaining batches
                    for batch in current_sorted_batches:
                        # Check if the batch is ready to be picked
                        if batch['release_time'] < time.time():
                            # Start the picking process
                            current_picking_batch, current_picking_process_start_time, current_picking_process_arrival_time = picker_starts_tour(batch, warehouse_layout)

                            # Store the current batch in the shared variables
                            shared_variables.variables['current_picking_batch'] = current_picking_batch
                            # Store the current picking process start time in the shared variables
                            shared_variables.variables['current_picking_process_start_time'] = current_picking_process_start_time
                            # Store the current picking process arrival time in the shared variables
                            shared_variables.variables['current_picking_process_arrival_time'] = current_picking_process_arrival_time
                            
                            # Remove the orders of the current batch from the list of all orders
                            for batch_order in current_picking_batch['orders']:
                                for all_order in all_orders:
                                    if batch_order['order_id'] == all_order['order_id']:
                                        all_orders.remove(all_order)
                            # Remove the batch from the list of sorted batches
                            current_sorted_batches.remove(batch)
                            # Print for debugging purposes
                            if shared_variables.variables.get('debug_mode'):
                                click.secho(f'Released batch with release time: {datetime.datetime.fromtimestamp(current_picking_process_start_time).strftime('%H:%M:%S.%f')[:-5]} and arrival time: {datetime.datetime.fromtimestamp(current_picking_process_arrival_time).strftime('%H:%M:%S.%f')[:-5]}', fg='yellow')
                                debug_print_batches([batch])
                            break

                # Update the amount of existing batches
                shared_variables.variables['amount_of_existing_batches'] = len(current_sorted_batches)
                # Update the amount of existing orders
                shared_variables.variables['amount_of_existing_orders'] = len(all_orders)
                # Avoid busy waiting
                time.sleep(0.05)

        except Exception as e:
            click.secho(f'Logic function encountered an error: {e}', fg='red')
            if shared_variables.variables.get('debug_mode'):
                click.secho(traceback.print_exc(), fg='red')


def debug_print_batches(current_sorted_batches):
    '''
    Print the current sorted batches.

    :param current_sorted_batches: List of current sorted batches
    '''
    # Convert the batch structure to a table
    table = []
    for batch in current_sorted_batches:
        batch_id = batch['batch_id']
        orders = []
        for order in batch['orders']:
            order_id = order['order_id']
            items = []
            for item in order['items']:
                item_id = item['item_id']
                abs_x_position = item['abs_x_position']
                abs_y_position = item['abs_y_position']
                abs_z_position = item['abs_z_position']
                items.append(f"Item ID: {item_id}, X: {abs_x_position}, Y: {abs_y_position}, Z: {abs_z_position}")
            orders.append(f"Order ID: {order_id}\n" + "\n".join(items))
        table.append([f"Batch ID: {batch_id}", "\n\n".join(orders)])

    # Print the table
    click.secho(f'{tabulate.tabulate(table, headers=["Batch", "Orders"], tablefmt="simple_grid")}\n', fg='yellow')


def debug_print_orders(orders):
    '''
    Print the current orders.

    :param orders: List of current orders
    '''
    # Convert the order structure to a table
    table = []
    for order in orders:
        order_id = order['order_id']
        items = []
        for item in order['items']:
            item_id = item['item_id']
            abs_x_position = item['abs_x_position']
            abs_y_position = item['abs_y_position']
            abs_z_position = item['abs_z_position']
            items.append(f"Item ID: {item_id}, X: {abs_x_position}, Y: {abs_y_position}, Z: {abs_z_position}")
        table.append([f"Order ID: {order_id}", "\n".join(items)])

    # Print the table
    click.secho(f'{tabulate.tabulate(table, headers=["Order", "Items"], tablefmt="simple_grid")}\n', fg='yellow')