import json
import click
from InquirerPy import prompt, inquirer
from src.vars import shared_variables

# Define the buttons for the program
release_button = 'Space'
end_button = 'Delete'
# Define the global variables
global debug_mode_global

# Start the CLI program
@click.command()
@click.option('--debug-mode', '-d', is_flag=True, help='Run the program in debug mode.')
@click.pass_context
def initialize(ctx, debug_mode):
    '''
    This function is the initializer function of the program. It initializes the program and gets the inputs from the user.

    :param debug_mode: A boolean value that indicates if the program should run in debug mode.
    '''
    # Call the global variables
    global debug_mode_global
    debug_mode_global = debug_mode
    shared_variables.variables['debug_mode'] = debug_mode

    # Display the welcome message
    display_welcome_message()
    # Get the inputs from the user
    variables = get_inputs()
    # Print the inputs for debug mode
    if debug_mode_global:
        click.echo('The inputs are: ')
        for key, value in variables.items():
            click.echo(f'{key}: {value}')
        click.echo('\n')
    # Display the manual of the program
    program_manual()

    # Ask the user if they want to start the program
    start_program = inquirer.confirm(message='Do you want to start the program with the provided inputs and release the orders?').execute()
    click.echo('\n')
    if start_program:
        # Print a message for debug mode
        if debug_mode_global:
            click.echo('The user has decided to start the program. The program will now be started.\n')
        # Update the shared variables
        shared_variables.variables.update(variables)
        # Return the variables
        return variables
    else:
        click.echo('The program was terminated by the user. Please restart the program if you want to run it again.')
        exit()

def display_welcome_message():
    '''
    This function displays the welcome message of the program.
    '''
    # Call the global variables
    global debug_mode_global
    # Initialize the variables
    hyperlink_paper_henn = 'https://www.sciencedirect.com/science/article/pii/S0305054812000020'
    hyperlink_github = 'https://github.com/PhilippXXY/on-line-order-batching'

    # Display the welcome message
    click.echo('\n')
    click.echo('Welcome to the project ' + click.style(create_hyperlink("'On-line Order Batching in an Order Picking Warehouse'", hyperlink_github), fg='cyan') + ' by Philipp Schmidt!')
    click.echo('\n')
    click.echo('This program is designed to improve the makespan of on-line order batching in a single picker warehouse.')
    click.echo('It is based on the ' + click.style(create_hyperlink('Paper by Sebastian Henn', hyperlink_paper_henn), fg='cyan') + '.')
    click.echo('\n')

    # Display information for debug mode
    if debug_mode_global:
        click.echo('You are running the program in '+ click.style('debug', fg='green')+ ' mode. This means that you will see additional information and messages.')
        click.echo('\n')

def get_inputs():
    '''
    This function gets the inputs from the user and stores them in the global variables. 
    '''
    # Give the user instructions
    click.echo("Please provide the following inputs, as they are required to run the program. If you want to use the default values, just press Enter.")
    click.echo('\n')
    
    # Define the questions
    questions = [
        {
            'type': 'input',
            'name': 'warehouse_layout_path',
            'message': 'Path to the warehouse layout:',
            'default': 'tests/data/warehouse_positions_20x10x5.CSV'
        },
        {
            'type': 'input',
            'name': 'order_path',
            'message': 'Path to the orders:',
            'default': 'tests/data/test_orders.json'
        },
        {
            'type': 'input',
            'name': 'max_batch_size',
            'message': 'Maximum batch size:',
            'default': '15'
        },
        {
            'type': 'input',
            'name': 'initial_order_release',
            'message': 'Initial order release:',
            'default': '10'
        },
        {
            'type': 'input',
            'name': 'rearrangement_parameter',
            'message': 'Rearrangement parameter [0;1]:',
            'default': '0.5'
        },
        {
            'type': 'input',
            'name': 'threshold_parameter',
            'message': 'Threshold parameter [0;1]:',
            'default': '0.5'
        },
        {
            'type': 'input',
            'name': 'release_parameter',
            'message': 'Release parameter [0;1]:',
            'default': '0.5'
        },
        {
            'type': 'input',
            'name': 'time_limit',
            'message': 'Time limit:',
            'default': '1'
        },
        {
            'type': 'list',
            'name': 'selection_rule',
            'message': 'Selection rule:',
            'choices': [
                {
                    'name': 'FIRST',
                    'value': 'FIRST'
                },
                {
                    'name': 'SHORT',
                    'value': 'SHORT'
                },
                {
                    'name': 'LONG',
                    'value': 'LONG'
                },
                {
                    'name': 'SAV',
                    'value': 'SAV'
                }
            ],
            'default': 'FIRST'
        },
    ]

    # Get the answers from the user
    answers = prompt(questions)
    click.echo('\n')
    # Store the answers in the variables
    variables = {
        'warehouse_layout_path': answers['warehouse_layout_path'],
        'max_batch_size': int(answers['max_batch_size']),
        'initial_order_release': int(answers['initial_order_release']),
        'rearrangement_parameter': float(answers['rearrangement_parameter']),
        'threshold_parameter': float(answers['threshold_parameter']),
        'release_parameter': float(answers['release_parameter']),
        'time_limit': int(answers['time_limit']),
        'selection_rule': answers['selection_rule'],
    }

    # Write the JSON orders to a file
    duplicate_orders_to_py(answers['order_path'])

    return variables

def program_manual():
    '''
    This function displays the manual of the program.
    '''
    # Display the manual
    instructions = [
        ("Release", f"Release orders by pressing {click.style(release_button, fg='red')}."),
        ("End", f"Release the last order by pressing {click.style(end_button, fg='red')}, which will terminate the program.")
    ]
    # Display the instructions
    click.echo('While running the program, you can provide the following inputs:\n')
    for name, description in instructions:
        click.echo(f"{name:<8}: {description}")
    click.echo('\n')

def create_hyperlink(text, url):
    '''
    This function creates a hyperlink in the terminal.

    :param text: The text to be displayed.
    :param url: The URL to be linked to.
    :return: The hyperlink.
    '''
    # Return the hyperlink
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def duplicate_orders_to_py(order_path):
    '''
    This function duplicates the orders to a .py file.

    :param order_path: The path to the orders.
    '''
    # Read the orders from the file
    with open(order_path, 'r') as file:
        orders = json.load(file)
    # Clear the .py file content
    open('src/ui/imported_orders.py', 'w').close()
    # Write the orders to the .py file
    with open('src/ui/imported_orders.py', 'a') as file:
        file.write('imported_orders = ' + str(orders) + '\n')
    # Print a message for debug mode
    if debug_mode_global:
        click.echo(f'The orders were duplicated to the file imported_orders.py. The orders are: {orders} \n')

if __name__ == '__main__':
    initialize()

