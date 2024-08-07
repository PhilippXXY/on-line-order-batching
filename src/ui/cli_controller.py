import threading
import time
import traceback
import uuid

import click
from src.ui.cli.cli_runtime import runtime
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

        # Set the input process to running
        shared_variables.variables['input_process_running'] = True
    
        # Release the starting orders based on the initial order release variable
        for i in range(shared_variables.variables.get('initial_order_release')):
            # Release an order
            release_order = self.release_order()
            # If there are no more orders to release, break the loop
            if release_order is None:
                break

    def run(self):
        '''
        Run method of the CLI thread
        '''
        try:
            # Update the shared variables with the variables of the thread
            shared_variables.variables.update(self.variables)
            # Call the runtime method
            runtime()
        # Catch exceptions
        except Exception as e:
            click.secho(f'CLIThread encountered an error: {e}', fg='red')
        # Finally, print a message that the run method has completed
        finally:
            # Set the input process to not running
            shared_variables.variables['input_process_running'] = False


    def release_order(self):
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

                return order
            
            # If there are no more orders in the imported orders
            else:
                # Print a message that there are no more orders to release
                click.echo('No more orders to release')
                # Return None
                return None
        # Catch exceptions
        except Exception as e:
            click.secho(f'release_order encountered an error: {e}', fg='red')
            return None


def generate_unique_id():
    '''
    Generate a unique ID using the UUID library

    :return: Unique ID
    '''
    return uuid.uuid4().hex