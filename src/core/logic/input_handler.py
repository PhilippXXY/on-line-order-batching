import json
import vars.shared_vars as shared_vars

def get_warehouse_layout():
    warehouse_layout_path = shared_vars.variables['warehouse_layout_path']
    warehouse_layout = json.loads(warehouse_layout_path)
    return warehouse_layout

def get_max_batch_size():
    max_batch_size = shared_vars.variables['max_batch_size']
    return max_batch_size

def get_initial_order_release():
    initial_order_release = shared_vars.variables['initial_order_release']
    return initial_order_release

def get_rearrangement_parameter():
    rearrangement_parameter = shared_vars.variables['rearrangement_parameter']
    return rearrangement_parameter

def get_threshold_parameter():
    threshold_parameter = shared_vars.variables['threshold_parameter']
    return threshold_parameter

def get_time_limit():
    time_limit = shared_vars.variables['time_limit']
    return time_limit

def get_selection_rule():
    selection_rule = shared_vars.variables['selection_rule']
    return selection_rule