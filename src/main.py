import threading

from src.ui.cli_controller import CLIThread
from src.core.logic_controller import LogicThread
from src.core.logic.batch_selector import batch_selector_logic
from src.core.logic.batch_tour_length_calculator import batch_tour_length_calculator_logic
from src.core.logic.batch_tour_length_minimizer import batch_tour_length_minimizer_logic
from src.core.logic.join_item_information import join_item_information_logic

import src.vars.shared_variables as shared_variables

global input_process_running

if __name__ == "__main__":
    cli_initialized_event = threading.Event()

    # Initialize the CLI thread
    cli_thread = CLIThread(cli_initialized_event)

    # Initialize the logic threads
    logic_threads = [
        LogicThread(cli_thread, batch_selector_logic),
        LogicThread(cli_thread, batch_tour_length_calculator_logic),
        LogicThread(cli_thread, batch_tour_length_minimizer_logic),
        LogicThread(cli_thread, join_item_information_logic)
    ]

    # Start the CLI thread
    cli_thread.start()
    # Wait for the CLI initialization to complete before starting the logic threads
    cli_initialized_event.wait()

    # Set the shared variables
    shared_variables.variables = cli_thread.variables

    # Start the logic threads
    for thread in logic_threads:
        thread.start()
    # Join the CLI thread
    cli_thread.join()

    # Join the logic threads
    for thread in logic_threads:
        thread.join()

    
