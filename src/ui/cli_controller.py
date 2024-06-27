import click
from InquirerPy import prompt, inquirer

# Define global variables
layout_path = ""
order_path = ""
max_batch_size = 0
initial_order_release = 0
rearrangement_parameter = 0.0
threshold_parameter = 0.0
time_limit = 0
# Sets the mode of the program
debug_mode = False
# Define the buttons for the program
release_button = 'Space'
end_button = 'Delete'

# Start the CLI program
@click.command()
@click.option('--debug-mode', '-d', is_flag=True, help='Run the program in debug mode.')
def main(debug_mode):
    '''
    This function is the main function of the program. It initializes the program and gets the inputs from the user.

    :param debug_mode: A boolean value that indicates if the program should run in debug mode.
    '''
    # Set the global variables
    global layout_path, order_path, max_batch_size, initial_order_release, rearrangement_parameter, threshold_parameter, time_limit
    global debug_mode_global

    # Set the global debug_mode
    debug_mode_global = debug_mode

    # Display the welcome message
    display_welcome_message()
    # Get the inputs from the user
    get_inputs()
    # Display the manual of the program
    program_manual()

    # Ask the user if they want to start the program
    start_program = inquirer.confirm(message='Do you want to start the program with the provided inputs and release the orders?').execute()
    click.echo('\n')
    if start_program:
        run_program()
    else:
        click.echo('The program was terminated by the user. Please restart the program if you want to run it again.')

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
    # Call the global
    global layout_path, order_path, max_batch_size, initial_order_release, rearrangement_parameter, threshold_parameter, time_limit

    # Give the user instructions
    click.echo("Please provide the following inputs, as they are required to run the program. If you want to use the default values, just press Enter.")
    click.echo('\n')
    
    # Define the questions
    questions = [
        {
            'type': 'input',
            'name': 'layout_path',
            'message': 'Path to the warehouse layout:',
            'default': 'tests/data/warehouse_positions_20x10x5.CSV'
        },
        {
            'type': 'input',
            'name': 'order_path',
            'message': 'Path to the orders:',
            'default': 'tests/data/test_orders.py'
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
            'message': 'Rearrangement parameter:',
            'default': '0.5'
        },
        {
            'type': 'input',
            'name': 'threshold_parameter',
            'message': 'Threshold parameter:',
            'default': '0.5'
        },
        {
            'type': 'input',
            'name': 'time_limit',
            'message': 'Time limit:',
            'default': '5'
        }
    ]
    # Get the answers from the user
    answers = prompt(questions)
    click.echo('\n')
    # Store the answers in the global variables
    layout_path = answers['layout_path']
    order_path = answers['order_path']
    max_batch_size = int(answers['max_batch_size'])
    initial_order_release = int(answers['initial_order_release'])
    rearrangement_parameter = float(answers['rearrangement_parameter'])
    threshold_parameter = float(answers['threshold_parameter'])
    time_limit = int(answers['time_limit'])

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

def run_program():
    '''
    This function runs the program with the provided global variables.
    '''
    click.echo("Starting the program with the provided inputs...")
    click.echo('Initial order release: ' + str(initial_order_release))

    # Add your actual program logic here
    # For lightweight mode, you might skip some steps or load fewer resources

def create_hyperlink(text, url):
    '''
    This function creates a hyperlink in the terminal.

    :param text: The text to be displayed.
    :param url: The URL to be linked to.
    :return: The hyperlink.
    '''
    # Return the hyperlink
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"
    

if __name__ == '__main__':
    main()
