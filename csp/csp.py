import logging
import datetime
from datetime import datetime
import inspect
import json
from json import JSONEncoder
# from constraint import *

# problem = Problem()
# problem.addVariable("a", [1,2,3])
# problem.addVariable("b", [4,5,6])

# c = 4

# def constraint_1(a, b):
#     return a+c < b


# problem.addConstraint(constraint_1, ("a", "b"))

# print(json.dumps(problem.getSolutions(), indent=4))


class ReprEncoder(JSONEncoder):
    def default(self, o):
        return repr(o)


class ConstraintNotAFunction(Exception):
   def __init__(self, object_name):
      self.msg = f"Object {object_name} exists but it's not a fuction"
      logging.error(self.msg)

   def __str__(self):
      return self.msg


class ConstraintMissingArguments(Exception):
   def __init__(self, function_name, list_of_missing_arguments):
      self.msg = f"Constraint with function '{function_name}' is missing arguments: {list_of_missing_arguments}"
      logging.error(self.msg)

   def __str__(self):
      return self.msg


class ConstraintUnexpectedArguments(Exception):
   def __init__(self, function_name, list_of_unexpected_arguments):
      self.msg = f"Constraint with function '{function_name}' has unexpected arguments: {list_of_unexpected_arguments}"
      logging.error(self.msg)

   def __str__(self):
      return self.msg


class ConstraintArgumentsNotInVariables(Exception):
   def __init__(self, constraint, constraint_arguments_not_in_variables, problem):
      self.msg = f"""Constraint with function '{constraint.function.__name__}' requires arguments {constraint.function_arguments},\nbut arguments {constraint_arguments_not_in_variables} haven't been defined as variables on Problem {problem}"""
      logging.error(self.msg)

   def __str__(self):
      return self.msg


class FunctionConstraint:

    def __init__(self, function, function_arguments):
        self.function = function
        self.function_arguments = function_arguments
        self.__consistent_contraint()

    def __repr__(self):
        return f"{self.function.__name__}({', '.join(self.function_arguments)})"

    def __consistent_contraint(self):

        if not inspect.isfunction(self.function):
            raise ConstraintNotAFunction(self.function)

        missing_arguments = [ arg for arg in inspect.signature(self.function).parameters if arg not in self.function_arguments ]
        if missing_arguments != []:
            raise ConstraintMissingArguments(self.function.__name__, missing_arguments)

        unexpected_arguments = [ arg for arg in self.function_arguments if arg not in inspect.signature(self.function).parameters ]
        if unexpected_arguments != []:
            raise ConstraintUnexpectedArguments(self.function.__name__, unexpected_arguments)

    def satisfied(self, assignment):

        logging.debug(f"Checking current \"{assignment = }\" against constraint '{self}'")
        for required_arg in self.function_arguments:
            if required_arg not in assignment:
                logging.debug(f"{required_arg = } not in assignment")
                return True
        logging.debug(f"All required arguments in assignment")

        kwargs = {
            required_arg: assignment[required_arg]
            for required_arg in self.function_arguments
        }

        return self.function(**kwargs)


class CSP:

    def __init__(self):
        self.variables = []
        self.constraints = {}
        self.assignment = {}
        self.domains = {}

    def __repr__(self):
        return json.dumps({
            var: {
                'domain': self.domains[var],
                'constraints': self.constraints[var]
            }
            for var in self.variables
        }, indent=4, cls=ReprEncoder)

    def __valid_constraint(self, constraint):
        logging.debug(f"Validating new proposed constraint with function {constraint.function.__name__}.")
        constraint_arguments_not_in_variables = list(set(constraint.function_arguments) - set(self.variables))
        if constraint_arguments_not_in_variables != []:
            raise ConstraintArgumentsNotInVariables(constraint, constraint_arguments_not_in_variables, self)
        logging.debug(f"Constraint with function {constraint.function.__name__} added successfully.")

    def add_variable(self, name, domain):
        self.variables.append(name)
        self.domains[name] = domain
        self.constraints[name] = []

    def add_constraint(self, constraint):

        self.__valid_constraint(constraint)

        for variable in constraint.function_arguments:
            self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True
        
    def bt_search(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [ var for var in self.variables if var not in assignment ]

        first = unassigned[0]
        for value in self.domains[first]:
            # Take current assignment
            local_assignment = assignment.copy()
            # Add new variable to curret assignment
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result = self.bt_search(local_assignment)
                if result is not None:
                    return result
        return None


def constraint_1(a):
    return a**2 < 4


def constraint_2(a, b):
    return a*2 < b


def main():

    p = CSP()

    p.add_variable('a', [1,2,3])
    p.add_variable('b', [4,5,6])

    p.add_constraint(FunctionConstraint(constraint_2, ['a', 'b']))

    print(p)

    print(p.bt_search())


if __name__ == "__main__":

    logging.basicConfig(
        filename='/root/log/log.log',
        format='%(levelname)-8s %(message)s',
        filemode='w'
    )
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(f"Starting time of execution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    main()
