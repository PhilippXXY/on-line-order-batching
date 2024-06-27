import json
import src.vars.shared_variables as shared_variables

def get_warehouse_layout():
    '''
    Get the warehouse layout from the shared variables

    :return: warehouse_layout
    '''
    warehouse_layout_path = shared_variables.variables['warehouse_layout_path']
    warehouse_layout = json.loads(warehouse_layout_path)
    return warehouse_layout

def get_max_batch_size():
    '''
    Get the maximum batch size from the shared variables

    :return: max_batch_size
    '''
    max_batch_size = shared_variables.variables['max_batch_size']
    return max_batch_size

def get_initial_order_release():
    '''
    Get the initial order release from the shared variables

    :return: initial_order_release
    '''
    initial_order_release = shared_variables.variables['initial_order_release']
    return initial_order_release

def get_rearrangement_parameter():
    '''
    Get the rearrangement parameter from the shared variables

    :return: rearrangement_parameter
    '''
    rearrangement_parameter = shared_variables.variables['rearrangement_parameter']
    return rearrangement_parameter

def get_threshold_parameter():
    '''
    Get the threshold parameter from the shared variables

    :return: threshold_parameter
    '''
    threshold_parameter = shared_variables.variables['threshold_parameter']
    return threshold_parameter

def get_time_limit():
    ''' 
    Get the time limit from the shared variables

    :return: time_limit
    '''
    time_limit = shared_variables.variables['time_limit']
    return time_limit

def get_selection_rule():
    '''
    Get the selection rule from the shared variables

    :return: selection_rule
    '''
    selection_rule = shared_variables.variables['selection_rule']
    return selection_rule

def get_input_process_running():
    '''
    Get the input process running variable from the shared variables

    :return: input_process_running
    '''
    input_process_running = shared_variables.variables['input_process_running']
    return input_process_running

def get_new_order():
    '''
    Get the new order from the shared variables

    :return: order
    '''
    # Get the new order from the shared variables
    new_order = shared_variables.variables['order']
    # Remove the new order from the shared variables
    shared_variables.variables['order'] = None
    
    return new_order


def is_new_order_available():
    '''
    Check if a new order is available

    :return: new_order_available: True if a new order is available, False otherwise
    '''
    if get_new_order() is not None:
        new_order_available = True
    else:
        new_order_available = False
    return new_order_available