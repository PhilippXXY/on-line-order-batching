import threading
from src.ui.cli import imported_orders
from src.ui.cli.cli_initialize import initialize
import vars.shared_variables as shared_variables

class CLIThread(threading.Thread):
    '''
    This class is a thread that initializes the CLI interface and sets the global variables.
    '''
    def __init__(self):
        '''
        This function initializes the CLIThread class.
        '''
        # Call the super function
        super().__init__()
        # Set the ready event
        self.ready = threading.Event()
        # Initialize the variables
        self.variables = {}

    def run(self):
        '''
        This function initializes the CLI interface and sets the global variables.
        '''
        # Call the initialize function from the CLI interface and set the global variables
        self.variables = initialize()
        # Set the ready event
        self.ready.set()

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
        # Remove the order from the imported_orders.py
        imported_orders.remove(order)
        # Write the order to the shared variables
        shared_variables['order'] = order

        return order        