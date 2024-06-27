import threading
from src.ui.cli.cli_initialize import initialize

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
