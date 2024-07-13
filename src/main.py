import threading
import click
import src.vars.shared_variables as shared_variables
from src.ui.cli_controller import CLIThread
from src.core.logic_controller import LogicThread
from src.ui.cli.cli_initialize import initialize

@click.command()
@click.pass_context
def main(ctx):
    '''
    Main function of the program

    :param ctx: Click context
    '''
    # Create a dictionary in the click context to store the variables
    ctx.ensure_object(dict)

    # Initialize the program
    variables = ctx.invoke(initialize)
    
    # Check if the initialization was successful
    if variables:
        # Create the threads for the CLI and logic
        init_event = threading.Event()
        cli_thread = CLIThread(init_event, variables)
        logic_thread = LogicThread(init_event, variables)

        # Start the threads
        cli_thread.start()
        logic_thread.start()
        cli_thread.join()
        logic_thread.join()

    else:
        # Print a message that the program initialization was aborted
        click.echo("Program initialization was aborted.")


if __name__ == "__main__":
    main(obj={})
