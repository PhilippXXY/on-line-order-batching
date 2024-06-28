import threading
import time
import uuid
from src.ui import imported_orders
from src.ui.cli.cli_initialize import initialize
import src.vars.shared_variables as shared_variables
import src.ui.imported_orders as imported_orders

class CLIThread(threading.Thread):
    '''
    This class is a thread that initializes the CLI interface and sets the global variables.
    '''
    def __init__(self, event):
        '''
        This function initializes the CLIThread class.
        '''
        # Call the super function
        super().__init__()
        # Set the event
        self.event = event

    def run(self):
        '''
        This function initializes the CLI interface and sets the global variables.
        '''
        # Call the initialize function from the CLI interface
        variables = initialize()
        # Set the variables to the shared variables
        shared_variables['variables'] = variables
        # Get the amount of initial orders
        amount_of_initial_orders = variables['initial_order_release']
        # Release the initial orders
        for i in range(amount_of_initial_orders):
            self.release_order()

        # Signal the initialization of the CLI interface is complete
        self.event.set()

    def get_picker_state():
        '''
        This function returns the picker state.
        '''
        # Get the picker state from the shared variables
        picker_state = shared_variables['picker_state']

        return picker_state
    
    def get_batches_to_select():
        '''
        This function returns the batches to select.
        '''
        # Get the batches to select from the shared variables
        batches_to_select = shared_variables['batches_to_select']

        return batches_to_select
    
    def release_order():
        '''
        This function releases a order from the imported_orders.py and sets it to the shared variables.
        '''
        # Get the first order from the imported_orders.py
        order = imported_orders[0]
        # Add a unique ID to the order
        order['order_id'] = generate_unique_id()
        # Add the arrival time to the order
        order['arrival_time'] = time.time()
        # Remove the order from the imported_orders.py
        imported_orders.remove(order)
        # Write the order to the shared variables
        shared_variables['order'] = order

        return order        
    

def generate_unique_id():
    '''
    This function generates a unique ID.
    '''
    # Generate a unique ID
    unique_id = uuid.uuid4()

    return unique_id