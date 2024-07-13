import json
import click
from InquirerPy import prompt, inquirer
from src.vars import shared_variables

# Define the buttons for the program
release_button = 'Space'
end_button = 'Delete'

# Start the CLI program
@click.command()
@click.pass_context
def initialize(ctx):
    '''
    This function is the initializer function of the program. It initializes the program and gets the inputs from the user.
    '''
    # Display the welcome message
    display_welcome_message()
    # Get the inputs from the user
    variables = get_inputs()
    # Display the manual of the program
    program_manual()

    # Ask the user if they want to start the program
    start_program = inquirer.confirm(message='Do you want to start the program with the provided inputs and release the orders?').execute()
    click.echo('\n')
    if start_program:
        # Update the shared variables
        shared_variables.variables.update(variables)
        # Return the variables
        return variables
    else:
        click.secho('The program was terminated by the user. Please restart the program if you want to run it again.', fg='red')
        exit()

def display_welcome_message():
    '''
    This function displays the welcome message of the program.
    '''
    # Initialize the variables
    hyperlink_paper_henn = 'https://www.sciencedirect.com/science/article/pii/S0305054812000020'
    hyperlink_github = 'https://github.com/PhilippXXY/on-line-order-batching'

    # Display the welcome message
    click.echo('\n')
    click.echo('Welcome to the project ' + click.style(create_hyperlink("'On-line Order Batching in an Order Picking Warehouse'", hyperlink_github), fg='blue') + ' by Philipp Schmidt!')
    click.echo('\n')
    click.echo('This program is designed to improve the makespan of on-line order batching in a single picker warehouse.')
    click.echo('It is based on the ' + click.style(create_hyperlink('Paper by Sebastian Henn', hyperlink_paper_henn), fg='blue') + '.')
    click.echo('\n')

def get_inputs():
    '''
    This function gets the inputs from the user and stores them in the global variables. 
    '''
    # Give the user instructions
    click.echo("Please provide the following inputs, as they are required to run the program. If you want to use the default values, just press Enter. \n")
    
    # Define the questions
    questions = [
        {
            'type': 'input',
            'name': 'warehouse_layout_path',
            'message': 'Path to the warehouse layout [.csv]:',
            'default': 'tests/data/warehouse_positions.csv'
        },
        {
            'type': 'input',
            'name': 'order_path',
            'message': 'Path to the orders [.json]:',
            'default': 'tests/data/test_orders.json'
        },
        {
            'type': 'input',
            'name': 'max_batch_size',
            'message': 'Maximum batch size [>1]:',
            'default': '15'
        },
        {
            'type': 'input',
            'name': 'initial_order_release',
            'message': 'Initial order release: [>1]',
            'default': '10'
        },
        {
            'type': 'input',
            'name': 'tour_length_units_per_second',
            'message': 'Tour length units per Second: [>0]',
            'default': '20'

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
            'message': 'Time limit: [>0]',
            'default': '0.5'
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
        'tour_length_units_per_second': int(answers['tour_length_units_per_second']),
        'rearrangement_parameter': float(answers['rearrangement_parameter']),
        'threshold_parameter': float(answers['threshold_parameter']),
        'release_parameter': float(answers['release_parameter']),
        'time_limit': float(answers['time_limit']),
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
        ("Release", f"Release orders during runtime by pressing {click.style(release_button, fg='red')}."),
        ("End", f"Release the last order by pressing {click.style(end_button, fg='red')}.")
    ]
    # Display the instructions
    click.echo('While running the program, you can provide the following keyboard inputs:\n')
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


if __name__ == '__main__':
    initialize()

