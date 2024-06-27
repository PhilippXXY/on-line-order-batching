import time
import click
import keyboard
from tabulate import tabulate
from ui.cli_controller import get_picker_state, get_batches_to_select, release_order

# Define the buttons for the program
release_button = 'Space'
end_button = 'Delete'
# Flag to indicate that the user wants to end the program
end_program = False
# Initialize the variables
picker_state = True # True: Picker is available, False: Picker is picking
batch_to_select = []

# Define debounce time in seconds
debounce_time = 0.5
last_release_time = 0
last_end_time = 0

def runtime():
    # While loop to keep the program running until the user presses the end button
    while not end_program:
        # Check if the picker state has changed and the picker is now not available anymore
        if (picker_state != get_picker_state_local()) and not get_picker_state_local():
            # Get the new batch that will be picked next
            batch_to_select = get_batches_to_select_local()[0]
            click.echo("--- New Batch to select ---")
            click.echo(f"Batch ID: {batch_to_select['batch_id']} ― Tour length: {batch_to_select['tour_length']}")
            # Prepare the table
            table_data = [[item['item_id'], item['abs_x_position'], item['abs_y_position'], item['abs_z_position']] for item in batch_to_select['items']]
            headers = ["Item ID", "Aisle No.", "Y Position", "Z Position"]
            # Print table using tabulate
            click.echo(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

        # Update the picker state
        picker_state = get_picker_state_local()

        # Check if the user has pressed the release button and debounce
        if keyboard.is_pressed(release_button):
            current_time = time.time()
            if current_time - last_release_time >= debounce_time:
                last_release_time = current_time
                # Release the order
                release_order_local()
        
        # Check if the user has pressed the end button and debounce
        if keyboard.is_pressed(end_button):
            current_time = time.time()
            if current_time - last_end_time >= debounce_time:
                last_end_time = current_time
                # Set the flag to end the program
                end_program = True

    # Print a message to indicate that the program will be terminated
    click.echo('The program was terminated by the user. It will shut down after the picker has finished all existing orders.')


    while len(get_batches_to_select_local) > 0:
        # Check if the picker state has changed and the picker is now not available anymore
        if (picker_state != get_picker_state_local()) and not get_picker_state_local():
            # Get the new batch that will be picked next
            batch_to_select = get_batches_to_select_local()[0]
            click.echo("--- New Batch to select ---")
            click.echo(f"Batch ID: {batch_to_select['batch_id']} ― Tour length: {batch_to_select['tour_length']}")
            # Prepare the table
            table_data = [[item['item_id'], item['abs_x_position'], item['abs_y_position'], item['abs_z_position']] for item in batch_to_select['items']]
            headers = ["Item ID", "Aisle No.", "Y Position", "Z Position"]
            # Print table using tabulate
            click.echo(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

        # Update the picker state
        picker_state = get_picker_state_local()

    # Print a message to indicate that the program will be terminated
    click.echo('The program has been shut down. If you want to restart it, please run the program again.')



def get_picker_state_local():
    '''
    This function returns the current state of the picker.
    '''
    return get_picker_state()
    

def get_batches_to_select_local():
    '''
    This function returns the batches that are available to select.
    '''
    return get_batches_to_select()
    

def release_order_local():
    '''
    This function releases the orders.
    '''
    release_order()
    click.echo('--- Order released ---')
