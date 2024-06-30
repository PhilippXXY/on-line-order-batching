import threading
import time
import uuid

import click
import src.vars.shared_variables as shared_variables
import src.ui.imported_orders as imported_orders

class CLIThread(threading.Thread):
    '''
    Class for the CLI thread
    '''
    def __init__(self, event, variables):
        '''
        Constructor of the CLI thread

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
            click.echo(f'CLIThread initialized with variables: {self.variables}\n')


    def run(self):
        '''
        Run method of the CLI thread
        '''
        # Set the debug mode
        debug_mode = shared_variables.variables.get('debug_mode')
        try:
            # If debug mode is enabled, print a message
            if debug_mode:
                click.echo('CLIThread running\n')
            # Update the shared variables with the variables of the thread
            shared_variables.variables.update(self.variables)
            # If debug mode is enabled, print a message
            if debug_mode:
                click.echo(f'Amount of orders to release: {shared_variables.variables.get("initial_order_release")}\n')
            # Release the starting orders based on the initial order release variable
            for i in range(shared_variables.variables.get('initial_order_release')):
                # Release an order
                release_order = self.release_order()
                # If there are no more orders to release, break the loop
                if release_order == None:
                    break
        # Catch exceptions	
        except Exception as e:
            print(f'CLIThread encountered an error: {e}')
        # Finally, print a message that the run method has completed
        finally:
            print('CLIThread run method completed')


    def get_picker_state(self):
        '''
        Get the picker state from the shared variables

        :return: Picker state
        '''
        return shared_variables.variables.get('picker_state', None)

    def get_batches_to_select(self):
        '''
        Get the batches to select from the shared variables

        :return: Batches to select
        '''
        return shared_variables.variables.get('batches_to_select', None)

    def release_order(self):
        '''
        Release an order to the shared variables from the imported orders and remove it from the imported orders

        :return: Released order
        '''
        try:
            # If there are still orders in the imported orders
            if imported_orders.imported_orders:
                # Pop the first order from the imported orders
                order = imported_orders.imported_orders.pop(0)
                # Generate a unique order ID
                order['order_id'] = generate_unique_id()
                # Set the arrival time of the order to the current time
                order['arrival_time'] = time.time()
                # Update the shared variables with the released order
                shared_variables.variables['order'] = order
                # If debug mode is enabled, print a message
                if shared_variables.variables.get('debug_mode'):
                    click.echo(f'Order released: {order}\n')
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
    return uuid.uuid4()
    