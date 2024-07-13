import datetime
import time
import traceback
import uuid
import click
import keyboard
from tabulate import tabulate
from src.ui import imported_orders
from src.vars import shared_variables
import src.ui.cli_controller as cli_controller

def runtime():
    '''
    This function is working as the runtime for the CLI. It is responsible for the interaction with the user and the picker.
    '''
    # Update the shared variables to indicate that the input process is running
    shared_variables.variables.update({'input_process_running': True})

    # Define the buttons for the program
    release_button = 'Space'
    end_button = 'Delete'
    # Flag to indicate that the user wants to end the program
    end_input_process = False
    # Initialize the variables
    picker_state = True # True: Picker is available, False: Picker is picking
    batch_to_select = []

    # Define debounce time in seconds
    debounce_time = 0.3
    # Initialize the last release time
    last_release_time = 0
    # Initialize the last end time
    last_end_time = 0
    
    # Store the last printed batch
    last_printed_batch = None

    # Print a message to indicate that the program is running and explain the basic functionality
    click.echo('The program is running. The picker is currently available and can pick the first batch.\n\n')

    # Run the picking process
    while not end_input_process:
        # Check if the logic function has populated the shared variables with the necessary data
        current_picking_batch = shared_variables.variables.get('current_picking_batch')
        if current_picking_batch is not None:
            # Check if the first batch is available and print it
            # Check if the picker state has changed and the picker is now not available anymore
            if (picker_state != get_picker_state()) and not get_picker_state():
                batch_to_select = get_batches_to_select()
                last_printed_batch = batch_to_select
                print_batch_to_select(batch_to_select)
                
        # Update the picker state
        picker_state = get_picker_state()

        # Check if the user has pressed the release button and debounce
        if keyboard.is_pressed(release_button):
            current_time = time.time()
            if current_time - last_release_time >= debounce_time:
                last_release_time = current_time
                # Release the order
                release_order()
        
        # Check if the user has pressed the end button and debounce
        if keyboard.is_pressed(end_button):
            current_time = time.time()
            if current_time - last_end_time >= debounce_time:
                last_end_time = current_time
                # Print a message to indicate that the program will be terminated
                click.secho('The user decided to hand over a last order to the system to pick.', fg='blue')
                click.secho('The program will now output the remaining batches and orders.\n\n', fg='blue')
                # Release the last order
                release_last_order()
                # Set the flag to end the cli program
                # Set the flag to end the logic of the program
                shared_variables.variables.update({'input_process_running': False})
                end_input_process = True

        # Avoid too high CPU usage
        time.sleep(0.01)


    # Wait until the last batches have been formed
    # Otherwise the program would jump to the end before the last batches have been formed
    while shared_variables.variables.get('last_batching_process_finished') is False:
        time.sleep(0.01)
        pass

    # Initialize variables
    amount_of_last_batches = shared_variables.variables.get('amount_of_existing_batches')
    amount_of_last_orders = shared_variables.variables.get('amount_of_existing_orders')
    # Check if there are any batches released before but not printed due to the end of the loop
    forgotten_batch = None
    if get_batches_to_select():
        if last_printed_batch != get_batches_to_select():
            # Get the forgotten batch
            forgotten_batch = get_batches_to_select()
            # Set the amount of last batches to the amount of last batches + 1
            amount_of_last_batches += 1
            # Set the amount of last orders to the amount of last orders + the amount of orders in the forgotten batch
            amount_of_last_orders += forgotten_batch['amount_of_orders']
            # Print the forgotten batch later on for an improved user experience
    
    # Get the last batches and add them to the last batches
    last_batches = shared_variables.last_batches_to_select

    # Give out the selection rule
    click.secho(f'The remaining {amount_of_last_batches} batches and {amount_of_last_orders} orders are given out, ready to be picked sequentially.', fg='blue')
    click.secho(f'The previously selected selection rule is: {shared_variables.variables.get('selection_rule')}\n', fg='blue')
    # Print the forgotten batch
    if forgotten_batch:
        print_last_batch_to_select(forgotten_batch)
    # Print the last batches
    for batch in last_batches:
        print_last_batch_to_select(batch)
    
    # Print a message to indicate that the program has been shut down
    click.secho('All the orders have been picked. The program will now be shut down.\n', fg='green')


def get_picker_state():
    '''
    Get the picker state from the shared variables

    :return: Picker state
    '''
    return shared_variables.picker_state

def get_batches_to_select():
    '''
    Get the batches to select from the shared variables

    :return: Batches to select
    '''
    return shared_variables.variables.get('current_picking_batch', [])

def release_order():
    '''
    Release an order to the shared variables from the imported orders and remove it from the imported orders

    :return: Released order
    '''
    try:
        # If there are still orders in the imported orders
        if imported_orders.imported_orders:
            # Pop the first order from the imported orders and store it in a variable
            order = imported_orders.imported_orders.pop(0)
            # Generate a unique order ID
            order['order_id'] = generate_unique_id()
            # Set the arrival time of the order to the current time
            order['arrival_time'] = time.time()
            # Update the shared variables with the released order
            shared_variables.orders.append(order)
            # Print the released order
            click.echo(f"Order with the ID {order['order_id']} arrived at {datetime.datetime.fromtimestamp(order['arrival_time']).strftime('%H:%M:%S')} and is handed over to the batching process.")
            click.echo('The order contains the following items:')
            table_data = [[item['item_id']] for item in order['items']]
            headers = ['Item ID']
            click.echo(tabulate(table_data, headers=headers, tablefmt='simple_grid'))
            click.echo('\n')
            return order
        
        # If there are no more orders in the imported orders
        else:
            # Print a message that there are no more orders to release
            click.secho('No more orders to release', fg='red')
            # Return None
            return None
    # Catch exceptions
    except Exception as e:
        click.secho(f'release_order encountered an error: {e}', fg='red')
        if shared_variables.variables.get('debug_mode'):
            traceback.print_exc()
        return None
    

def release_last_order():
    '''
    Release the last order to the shared variables from the imported orders and remove it from the imported orders
    '''
    try:
        # If there are still orders in the imported orders
        if imported_orders.imported_orders:
            # Pop the first order from the imported orders and store it in a variable
            order = imported_orders.imported_orders.pop(0)
            # Generate a unique order ID
            order['order_id'] = generate_unique_id()
            # Set the arrival time of the order to the current time
            order['arrival_time'] = time.time()
            # Update the shared variables with the released order
            shared_variables.last_orders.append(order)
            # Print the released order
            click.echo(f"Last Order with the ID {order['order_id']} arrived at {datetime.datetime.fromtimestamp(order['arrival_time']).strftime('%H:%M:%S')} and is handed over to the batching process.")
            click.echo('This order contains the following items:')
            table_data = [[item['item_id']] for item in order['items']]
            headers = ['Item ID']
            click.echo(tabulate(table_data, headers=headers, tablefmt='simple_grid'))
            click.echo('\n')
            return order
        
        # If there are no more orders in the imported orders
        else:
            # Print a message that there are no more orders to release
            click.secho('No more orders to release', fg='red')
            # Return None
            return None
    # Catch exceptions
    except Exception as e:
        click.secho(f'release_last_order encountered an error: {e}', fg='red')
        if shared_variables.variables.get('debug_mode'):
            traceback.print_exc()
        return None


def generate_unique_id():
    '''
    Generate a unique ID using the UUID library

    :return: Unique ID
    '''
    return uuid.uuid4().hex


def print_batch_to_select(batch):
    '''
    Print the batch to the console

    :param batch: Batch to be printed
    '''
    # Convert the batch structure to a table
    table = []
    # Get the batch ID
    batch_id = batch['batch_id']
    # Get the items sorted by S-Shape-Routing
    batch_sorted_items = batch['sorted_batch_s_shape_routing']
    # Get the amount of orders
    batch_amount_of_orders = batch['amount_of_orders']
    # Get the amount of items
    batch_amount_of_items = batch['amount_of_items']
    # Get the tour length
    batch_tour_length = batch['tour_length']
    # Get the start time and convert it to a readable format
    batch_start_time = datetime.datetime.fromtimestamp(batch['start_time']).strftime('%H:%M:%S.%f')[:-5]
    # Get the arrival time and convert it to a readable format
    batch_arrival_time = datetime.datetime.fromtimestamp(batch['arrival_time']).strftime('%H:%M:%S.%f')[:-5]
    # Get the tour time and convert it to a readable format
    batch_tour_time = datetime.datetime.fromtimestamp(batch['tour_time']).strftime('%M:%S.%f')[:-5]
    # Initialize the orders
    orders = []
    # Iterate over the orders
    for order in batch['orders']:
        # Get the order ID
        order_id = order['order_id']
        # Initialize the items
        items = []
        # Iterate over the items
        if 'items' in order:
            for item in order['items']:
                # Get the item ID, X, Y, and Z position
                item_id = item['item_id']
                abs_x_position = item['abs_x_position']
                abs_y_position = item['abs_y_position']
                abs_z_position = item['abs_z_position']
                # Append the item to the items list
                items.append(f"Item ID: {item_id}, X: {abs_x_position}, Y: {abs_y_position}, Z: {abs_z_position}")
        # Append the order to the orders list
        orders.append(f"Order ID: {order_id}\n" + "\n".join(items))
    # Append the batch ID and the orders to the table
    table.append([f"Batch ID: {batch_id}", "\n\n".join(orders)])
    # Add the items sorted by S-Shape-Routing to the table so that the picker can see the items in the order they should be picked
    sorted_items_table = "\n".join([f"Item ID: {item['item_id']}, X: {item['abs_x_position']}, Y: {item['abs_y_position']}, Z: {item['abs_z_position']}" for item in batch_sorted_items])
    table.append(['Items sorted by S-Shape-Routing:', sorted_items_table])
    # Add the amount of orders to the table
    table.append(['Amount of Orders:', batch_amount_of_orders])
    # Add the amount of items to the table
    table.append(['Amount of Items:', batch_amount_of_items])
    # Add the tour length to the table
    table.append(['Tour Length in warehouse units:', batch_tour_length])
    # Add the start time to the table
    table.append(['Start Time:', batch_start_time])
    # Add the arrival time to the table
    table.append(['Arrival Time:', batch_arrival_time])
    # Add the tour time to the table
    table.append(['Tour Time in seconds:', batch_tour_time])
    # Print the table
    click.echo('--- Released batch to be picked now ---')
    click.echo(tabulate(table, tablefmt='simple_grid'))
    click.echo(remaining_batches_print_return(shared_variables.variables.get('amount_of_existing_batches')))
    click.echo(remaining_orders_print_return(shared_variables.variables.get('amount_of_existing_orders')))
    click.echo('\n')


def print_last_batch_to_select(batch):
    '''
    Print the batch to the console

    :param batch: Batch to be printed
    '''
    # Convert the batch structure to a table
    table = []
    # Get the batch ID
    batch_id = batch['batch_id']
    # Get the items sorted by S-Shape-Routing
    batch_sorted_items = batch['sorted_batch_s_shape_routing']
    # Get the amount of orders
    batch_amount_of_orders = batch['amount_of_orders']
    # Get the amount of items
    batch_amount_of_items = batch['amount_of_items']
    # Get the tour length
    batch_tour_length = batch['tour_length']
    # Get the tour time
    batch_tour_time = datetime.datetime.fromtimestamp(batch['tour_time']).strftime('%M:%S.%f')[:-5]
    # Initialize the orders
    orders = []
    # Iterate over the orders
    for order in batch['orders']:
        # Get the order ID
        order_id = order['order_id']
        # Initialize the items
        items = []
        # Iterate over the items
        if 'items' in order:
            for item in order['items']:
                # Get the item ID, X, Y, and Z position
                item_id = item['item_id']
                abs_x_position = item['abs_x_position']
                abs_y_position = item['abs_y_position']
                abs_z_position = item['abs_z_position']
                # Append the item to the items list
                items.append(f"Item ID: {item_id}, X: {abs_x_position}, Y: {abs_y_position}, Z: {abs_z_position}")
        # Append the order to the orders list
        orders.append(f"Order ID: {order_id}\n" + "\n".join(items))
    # Append the batch ID and the orders to the table
    table.append([f"Batch ID: {batch_id}", "\n\n".join(orders)])
    # Add the items sorted by S-Shape-Routing to the table so that the picker can see the items in the order they should be picked
    sorted_items_table = "\n".join([f"Item ID: {item['item_id']}, X: {item['abs_x_position']}, Y: {item['abs_y_position']}, Z: {item['abs_z_position']}" for item in batch_sorted_items])
    table.append(['Items sorted by S-Shape-Routing:', sorted_items_table])
    # Add the amount of orders to the table
    table.append(['Amount of Orders:', batch_amount_of_orders])
    # Add the amount of items to the table
    table.append(['Amount of Items:', batch_amount_of_items])
    # Add the tour length to the table
    table.append(['Tour Length in warehouse units:', batch_tour_length])
    # Add the tour time to the table
    table.append(['Calculated Tour Time in seconds:', batch_tour_time])
    # Print the table
    click.echo(tabulate(table, tablefmt='simple_grid'))
    click.echo('\n')

 
def remaining_batches_print_return(amount_of_existing_batches):
    '''
    Gives the amount of remaining batches to select

    :param amount_of_existing_batches: Amount of existing batches
    :return: Remaining batches as string
    '''
    if amount_of_existing_batches == 0:
        return 'No more batches to select.'
    else:
        return f'Amount of remaining batches to get picked: {amount_of_existing_batches}'
    

def remaining_orders_print_return(amount_of_existing_orders):
    '''
    Gives the amount of remaining orders to select

    :param amount_of_existing_orders: Amount of existing orders
    :return: Remaining orders as string
    '''
    if amount_of_existing_orders == 0:
        return 'There are no more open orders.'
    else:
        return f'Amount of open orders: {amount_of_existing_orders}'