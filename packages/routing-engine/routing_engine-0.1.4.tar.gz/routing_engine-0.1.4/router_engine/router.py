from . import rule_parser as parser
from . import rule_executor as executer


class routerClass:
    rules = None
    rules_file = None

    def __init__(self,file_path=None,rules_json=None) -> None:
        if file_path is not None:
            self.load_rules_from_file(file_path)
        elif rules_json is not None:
            self.load_rules_from_json(rules_json)
        else:
            raise Exception("cannot initialize router, check rules")
            
        
    def load_rules_from_file(self,file_path):
        self.rules_file = file_path
        self.rules = parser.load_rules_from_file(file_path=self.rules_file)
    def load_rules_from_json(self,rules_json):
        self.rules = parser.load_rules_from_json(json_data=rules_json)
    
    def apply_rules(self,context, actions):
        sorted_rules = sorted(self.rules, key=lambda r: -r['priority']) # Sorting by descending priority
        rules_status = {} 
        for rule in sorted_rules:
            if executer.evaluate_condition(rule['condition'], context):
                try:
                    result,status = executer.execute_actions(rule['actions'],actions)
                    rules_status[str(rule)] = status
                    if not result is None:
                        return True,result,rule,rules_status # Return if action is successfully executed
                except executer.ExecutionFailed as e:
                    rules_status[str(rule)] = e
                    pass # Continue to the next rule if execution failed
            else:
                rules_status[str(rule)] = "rule doesn't apply"

        return False,None,None,rules_status # Return False if no rules were successfully executed