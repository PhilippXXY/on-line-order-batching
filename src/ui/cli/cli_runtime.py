import datetime
import time
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
    # Print a message to indicate that the CLI runtime has been started
    if shared_variables.variables.get('debug_mode'):
        click.echo('CLI Runtime has been started.\n')
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
    debounce_time = 0.5
    # Initialize the last release time
    last_release_time = 0
    # Initialize the last end time
    last_end_time = 0
    

    while not end_input_process:
        # Check if the logic function has populated the shared variables with the necessary data
        current_picking_batch = shared_variables.variables.get('current_picking_batch')
        if current_picking_batch is not None:
            # Check if the picker state has changed and the picker is now not available anymore
            if (picker_state != get_picker_state()) and not get_picker_state():
                print('Inside the if statement')
                # Get the new batch that will be picked next
                print(shared_variables.variables)
                print(get_batches_to_select())
                batch_to_select = get_batches_to_select()
                click.echo("--- New Batch to select ---")
                click.echo(f"Batch ID: {batch_to_select['batch_id']} ― Tour length: {batch_to_select['tour_length']}")
                # Prepare the table
                table_data = [[item['item_id'], item['abs_x_position'], item['abs_y_position'], item['abs_z_position']] for item in batch_to_select['items']]
                headers = ["Item ID", "Aisle No.", "Y Position", "Z Position"]
                # Print table using tabulate
                click.echo(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

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
                # Set the flag to end the program
                end_input_process = True
                shared_variables.variables.update({'input_process_running': False})

        # Avoid too high CPU usage
        time.sleep(0.1)

    # Print a message to indicate that the program will be terminated
    click.echo('The program was terminated by the user. It will shut down after the picker has finished all existing orders.')


    while len(get_batches_to_select()) > 0:
        # Check if the picker state has changed and the picker is now not available anymore
        if (picker_state != get_picker_state()) and not get_picker_state():
            # Get the new batch that will be picked next
            batch_to_select = get_batches_to_select()
            click.echo("--- New Batch to select ---")
            click.echo(f"Batch ID: {batch_to_select['batch_id']} ― Tour length: {batch_to_select['tour_length']}")
            # Prepare the table
            table_data = [[item['item_id'], item['abs_x_position'], item['abs_y_position'], item['abs_z_position']] for item in batch_to_select['items']]
            headers = ["Item ID", "Aisle No.", "Y Position", "Z Position"]
            # Print table using tabulate
            click.echo(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

        # Update the picker state
        picker_state = get_picker_state()

        # Avoid too high CPU usage
        time.sleep(0.1)

    # Print a message to indicate that the program has been shut down
    click.echo('The program has been shut down. If you want to restart it, please run the program again.')


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
            click.echo('No more orders to release')
            # Return None
            return None
    # Catch exceptions
    except Exception as e:
        print(f'release_order encountered an error: {e}')
        return None


def generate_unique_id():
    '''
    Generate a unique ID using the UUID library

    :return: Unique ID
    '''
    return uuid.uuid4().hex