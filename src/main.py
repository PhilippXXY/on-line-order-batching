import threading
import click
import src.vars.shared_variables as shared_variables
from src.ui.cli_controller import CLIThread
from src.core.logic_controller import LogicThread
from src.ui.cli.cli_initialize import initialize

@click.command()
@click.option('--debug-mode', '-d', is_flag=True, help='Run the program in debug mode.')
@click.pass_context
def main(ctx, debug_mode):
    '''
    Main function of the program

    :param ctx: Click context
    :param debug_mode: Flag to run the program in debug mode
    '''
    # Set the debug mode in the shared variables
    shared_variables.variables['debug_mode'] = debug_mode
    # Create a dictionary in the click context to store the variables
    ctx.ensure_object(dict)

    # Initialize the program
    variables = ctx.invoke(initialize, debug_mode=debug_mode)
    
    # Check if the initialization was successful
    if variables:
        # Create the threads for the CLI and logic
        init_event = threading.Event()
        cli_thread = CLIThread(init_event, variables)
        logic_thread = LogicThread(init_event, variables)

        # Start the threads
        cli_thread.start()
        cli_thread.join()
        logic_thread.start()
        logic_thread.join()
    else:
        # Print a message that the program initialization was aborted
        click.echo("Program initialization was aborted.")


if __name__ == "__main__":
    main(obj={})
