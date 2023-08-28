from .rule_evaluator import evaluate_condition

class ExecutionFailed(Exception):
    pass

def get_function_by_name(name,actions):
    return actions.get(name, None)

def execute_actions(action_names, actions):
    for action_name in action_names:
        function = get_function_by_name(action_name, actions)
        if not function:
            continue  # Skip to the next action if this one is not found
        
        try:
            result = function()
            if result:  # If the function returns True, exit the function
                return
        except Exception as e:
            continue  # Continue to the next action if this one fails to execute

    # If we reach here, all actions have either failed to execute or returned False
    failed_actions = ', '.join(action_names)
    raise ExecutionFailed(f"All actions {failed_actions} failed to execute or returned False")