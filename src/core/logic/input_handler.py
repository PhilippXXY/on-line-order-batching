import pandas as pd
from src.core.logic.join_item_information import join_item_id_and_position_csv
import src.vars.shared_variables as shared_variables


def get_warehouse_layout():
    '''
    Get the warehouse layout from the shared variables

    :return: warehouse_layout
    '''
    warehouse_layout_path = shared_variables.variables.get('warehouse_layout_path')
    # Read the CSV file
    df = pd.read_csv(warehouse_layout_path, sep=';')
    
    # Calculate the max positions and round them in case they are not integers
    max_x_position = round(df['abs_x_position'].max())
    max_y_position = round(df['abs_y_position'].max())
    max_z_position = round(df['abs_z_position'].max())
    
    # Create the warehouse layout dictionary
    warehouse_layout = {
        'max_x_position': max_x_position,
        'max_y_position': max_y_position,
        'max_z_position': max_z_position,
    }
    return warehouse_layout

def get_warehouse_layout_path():
    '''
    Get the warehouse layout path from the shared variables

    :return: warehouse_layout_path
    '''
    warehouse_layout_path = shared_variables.variables.get('warehouse_layout_path')
    return warehouse_layout_path


def get_max_batch_size():
    '''
    Get the maximum batch size from the shared variables

    :return: max_batch_size
    '''
    max_batch_size = shared_variables.variables.get('max_batch_size')
    return max_batch_size


def get_initial_order_release():
    '''
    Get the amount of initial orders releases from the shared variables

    :return: initial_order_release
    '''
    initial_order_release = shared_variables.variables.get('initial_order_release')
    return initial_order_release


def get_rearrangement_parameter():
    '''
    Get the rearrangement parameter from the shared variables

    :return: rearrangement_parameter
    '''
    rearrangement_parameter = shared_variables.variables.get('rearrangement_parameter')
    return rearrangement_parameter


def get_threshold_parameter():
    '''
    Get the threshold parameter from the shared variables

    :return: threshold_parameter
    '''
    threshold_parameter = shared_variables.variables.get('threshold_parameter')
    return threshold_parameter

def get_release_parameter():
    '''
    Get the release parameter from the shared variables

    :return: release_parameter
    '''
    release_parameter = shared_variables.variables.get('release_parameter')
    return release_parameter


def get_time_limit():
    ''' 
    Get the time limit from the shared variables

    :return: time_limit
    '''
    time_limit = shared_variables.variables.get('time_limit')
    return time_limit


def get_selection_rule():
    '''
    Get the selection rule from the shared variables

    :return: selection_rule
    '''
    selection_rule = shared_variables.variables.get('selection_rule')
    return selection_rule


def get_input_process_running():
    '''
    Get the input process running variable from the shared variables

    :return: input_process_running
    '''
    input_process_running = shared_variables.variables.get('input_process_running')
    return input_process_running


def get_new_order():
    '''
    Get the new order from the shared variables

    :return: order
    '''
    # Get the new order and remove it from the list
    if shared_variables.orders:
        new_order = shared_variables.orders.pop(0)
        # Add to each item the absolute position in the warehouse
        for item in new_order['items']:
            item_id = item['item_id']
            item_data = join_item_id_and_position_csv(get_warehouse_layout_path(), item_id)
            item['abs_x_position'] = item_data['abs_x_position']
            item['abs_y_position'] = item_data['abs_y_position']
            item['abs_z_position'] = item_data['abs_z_position']

        return new_order
    else:
        return None


def is_new_order_available():
    '''
    Check if a new order is available

    :return: new_order_available: True if a new order is available, False otherwise
    '''
    if shared_variables.orders.__len__() > 0:
        new_order_available = True
    else:
        new_order_available = False

    return new_order_available