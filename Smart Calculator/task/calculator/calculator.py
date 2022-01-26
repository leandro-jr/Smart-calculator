# write your code here
from string import ascii_letters, digits
from re import findall
variables_dict = {}

def numbers(input_list):
    """not used on the final version of the project"""
    num_list = []
    signs_list = []

    for i in input_list:
        if i.isnumeric():
            num_list.append(int(i))
        if i.isalpha():
            variable = variables_dict.get(i)
            if variable:
                num_list.append(variable)
        if "+" in i:
            signs_list.append("+")
            num_list.append('+')
        if len(i) > 1 and i[0] == '-':
            if i[1].isnumeric():
                num_list.append(int(i))
            elif len(i) % 2 == 0:
                signs_list.append("+")
                num_list.append('+')
            else:
                signs_list.append("-")
                num_list.append('-')
        elif len(i) == 1 and i[0] == '-':
            signs_list.append("-")
            num_list.append('-')

    return num_list, signs_list


def calculate(num_list):
    """not used on the final version of the project"""
    only_num = []
    total = 0
    for index, item in enumerate(num_list):
        if item == '+':
            pass
        elif item == '-':
            only_num.append(-1 * num_list[index + 1])
        elif num_list[index - 1] == '-':
            pass
        else:
            only_num.append(item)

    # print(only_num)
    for i in only_num:
        total += i
    return total


def test_expression_1(input_num):
    """Test if expressions with only one number or variables are valid"""
    if len(input_num) == 2:
        input_num = [input_num[0] + input_num[1]]
    if input_num[0][-1] == '+' or input_num[0][-1] == '-':
        print("Invalid expression")
    elif input_num[0].isnumeric():
        print(input_num[0])
    elif input_num[0][0] == '+':
        input_num[0] = input_num[0][1:]
        print(input_num[0])
    elif input_num[0][0] == '-':
        print(input_num[0])
    elif not all([letter in ascii_letters for letter in input_num[0]]):
        print("Invalid identifier")
    elif variables_dict.get(input_num[0]) != None:
        print(variables_dict.get(input_num[0]))
    else:
        print("Unknown variable")


def test_expression_2(input_num: list):
    """Test if expressions with more than one number or variables are valid"""
    infix_exp = input_num
    stack_brackets = []
    repeated_plus = {}
    repeated_minus = {}
    brackets_flag = 0

    # test expression for + - * /
    if not any(['+' in element for element in input_num]) and not any(['-' in element for element in input_num]) \
            and not any(['*' in element for element in input_num]) and not any(['/' in element for element in input_num]):
        print("Invalid expression")
        return None

    for index, item in enumerate(input_num):
        # test if parentheses are correct
        if item == '(':
            brackets_flag = 1
            stack_brackets.append(item)
        elif item == ')':
            if len(stack_brackets) > 0:
                stack_brackets.pop()
            else:
                print("Invalid expression")
                return None
        # test if there are multiples * or / on the expression
        elif item == '*' and input_num[index - 1] == '*':
            print("Invalid expression")
            return None
        elif item == '/' and input_num[index - 1] == '/':
            print("Invalid expression")
            return None
        elif item == '+':
            if len(repeated_plus) == 0 or input_num[index - 1] == '+':
                repeated_plus.setdefault(item, []).append(index)

    if brackets_flag == 1 and len(stack_brackets) > 0:
        print("Invalid expression")
        return None

    # transform multiples '+' to only one
    if len(repeated_plus) > 0:
        repeated_plus_size = len(repeated_plus['+'])
        if repeated_plus_size > 1:
            intial_index = repeated_plus['+'][0]
            for _ in range(repeated_plus_size - 1):
                infix_exp.pop(intial_index)

    # transform multiples '-' to only one. E.g. '--' is '+', '---' is '-
    for index, item in enumerate(infix_exp):
        if item == '-':
            if len(repeated_minus) == 0 or input_num[index - 1] == '-':
                repeated_minus.setdefault(item, []).append(index)

    if len(repeated_minus) > 0:
        repeated_minus_size = len(repeated_minus['-'])
        if repeated_minus_size > 1:
            intial_index = repeated_minus['-'][0]
            if repeated_minus_size % 2 == 1:
                for _ in range(repeated_minus_size - 1):
                    infix_exp.pop(intial_index)
            else:
                for _ in range(repeated_minus_size - 1):
                    infix_exp.pop(intial_index)
                infix_exp[intial_index] = '+'

    return infix_exp


def variables(input_user: str):
    """Attributes a variable to a dictionary"""
    variables_list = input_user.replace(" ", "").split('=')
    if len(variables_list) == 2:
        # test if only letters are used to name the variable
        if not all([letter in ascii_letters for letter in variables_list[0]]):
            print("Invalid identifier")
            return 0
        # test if thr value attributed to the variable is composed only of numbers or letters
        elif any([number in digits for number in variables_list[1]]) and any([letter in ascii_letters for letter in variables_list[1]]):
            print("Invalid assignment")
            return 0
        # save number to the dictionary
        elif variables_list[1].isnumeric():
            variables_dict[variables_list[0]] = int(variables_list[1])
            return variables_dict

        elif len(variables_list[1]) > 1 and variables_list[1][0] == '-':
            if variables_list[1][1].isnumeric():
                variables_dict[variables_list[0]] = int(variables_list[1])

        # if variable was previously used, it is reassigned to the new variable
        elif variables_dict.get(variables_list[1]):
            variables_dict[variables_list[0]] = variables_dict.get(variables_list[1])
            return variables_dict

        elif variables_dict.get(variables_list[1]) == None:
            print("Unknown variable")

    else:
        print("Invalid assignment")
        return 0


def infix_to_postfix(input_exp: list) -> list:
    """Transform the expression from infix to postfix notation:
    Input is the input_exp e.g ['2', '*', '(', '3', '+', '4', ')', '+', '1']
    Output is output_exp [2, 3, 4, '+', '*', 1, '+']
    stack is a list that will be used as an intermediary between the input_exp and the output_exp
    1. Add operands (numbers and variables) to the result (postfix notation) as they arrive.
    2. If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
    3. If the incoming operator has higher precedence than the top of the stack, push it on the stack.
    4. If the precedence of the incoming operator is lower than or equal to that of the top of the stack, pop the stack
    and add operators to the result until you see an operator that has smaller precedence or a left parenthesis on the
    top of the stack; then add the incoming operator to the stack.
    5. If the incoming element is a left parenthesis, push it on the stack.
    6. If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a
    left parenthesis. Discard the pair of parentheses.
    7. At the end of the expression, pop the stack and add all operators to the result."""
    print(input_exp)
    stack = []
    output_exp = []
    precedence = {'*': 1, '/': 1, '+': 0, '-': 0}
    for i in input_exp:
        if len(i) > 1 and i[1].isnumeric():
            output_exp.append(int(i))
        elif i.isnumeric():
            output_exp.append(int(i))
        elif i.isalpha():
            variable = variables_dict.get(i)
            if variable != None:
                output_exp.append(variable)
        elif i in "+-*/":
            if len(stack) == 0:
                stack.append(i)
            elif stack[-1] == '(':
                stack.append(i)
            elif precedence[i] > precedence[stack[-1]]:
                stack.append(i)
            elif precedence[i] <= precedence[stack[-1]]:
                while True:
                    if len(stack) > 0:
                        if stack[-1] == '(':
                            output_exp.append(stack.pop())
                            break
                        elif precedence[i] <= precedence[stack[-1]]:
                            output_exp.append(stack.pop())
                            break
                stack.append(i)
        elif i == '(':
            stack.append(i)
        elif i == ')':
            while stack[-1] != '(':
                output_exp.append(stack.pop())
            stack.pop()

    while len(stack) > 0:
        output_exp.append(stack.pop())

    return output_exp


def calculate_postfix(postfix_exp: list):
    """Calculates the expression and provides the result.
    Input postfix_exp e.g. [2, 3, 4, '+', '*', 1, '+']
    stack is a list that will be used to calculate the output_exp
    When we have an expression in postfix notation, we can calculate it using another stack. To do that, scan the
    postfix expression from left to right:
    1. If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
    2. If the incoming element is the name of a variable, push its value into the stack.
    3. If the incoming element is an operator, then pop twice to get two numbers and perform the operation; push the
    result on the stack.
    4. When the expression ends, the number on the top of the stack is a final result.
    """
    stack = []
    print(postfix_exp)

    for i in postfix_exp:
        if type(i) == int or type(i) == float:
            stack.append(i)
        elif i == "+":
            result = stack.pop() + stack.pop()
            stack.append(result)
        elif i == "-":
            result = -1 * stack.pop() + stack.pop()
            stack.append(result)
        elif i == "*":
            result = stack.pop() * stack.pop()
            stack.append(result)
        elif i == "/":
            result = (1 / stack.pop()) * stack.pop()
            stack.append(result)

    if stack[0] == round(stack[0], 0):
        return round(stack[0])
    return stack[0]


def main():
    help_1 = """
    This program calculates the sum/subtraction/multiplication/division (or a mix of them) of numbers/variables.")
    E.g. -2 + 4 - 5 + 6   
    It also accepts to save variables (composed of letters) that can be used later on.
    E.g. a = -5
    E.g. 2 + a * 3
    To get help type /help
    To quit the program type /exit
    """
    help_2 = """
    Parentheses can be used to give priority on expressions.
    E.g. 2 + 1 * (3 - a)
    The program accepts expressions with multiples '+' or '-'
    E.g. 3 ++ 2 * 1 or 5 -- 3 / 1
    But does not accept multiples '*' or '/'
    E.g. 3 *** 5
    Other expressions like '22-' or '/go' will not be accepted
    """
    print("-" * 120)
    print(help_1)
    print("-" * 120)
    print()
    # runs the calculator while /exit is not entered by the user
    while True:
        input_user = input()
        if not input_user:
            pass
        # attributes variables
        elif '=' in input_user:
            if variables(input_user) == 0:
                pass
        else:
            if input_user == "/exit":
                print("Bye!")
                break
            elif input_user == "/help":
                print("-" * 120)
                print(help_1)
                print(help_2)
                print("-" * 120)
            elif input_user[0] == "/":
                print("Unknown command")
            else:
                # split the expression to a list
                negative_number_flag = False
                input_num = []
                input_split = findall('[+-]|[/*]|[()]|[0-9]+|[a-zA-z]+', input_user)
                for index, item in enumerate(input_split):
                    if item == '-' and input_split[index - 1] in '+*/':
                        input_num.append('-' + input_split[index + 1])
                        negative_number_flag = True
                    elif negative_number_flag == True:
                        pass
                    else:
                        input_num.append(item)

                # verify if the expression is valid
                if len(input_num) <= 2:
                    test_expression_1(input_num)
                elif len(input_num) > 2:
                    infix_exp = test_expression_2(input_num)
                    # transform from infix to postfix notation
                    if infix_exp:
                        postfix_exp = infix_to_postfix(infix_exp)
                        # calculate the result
                        print(calculate_postfix(postfix_exp))

if __name__ == '__main__':
    main()

"""In this project I had the opportunity to work with strings, regex, dictionaries, lists, stack and conditions creating
a calculator that can deal with four operations (*, /, +, -). It accept parentheses and variables can be provided.
In order to deal with the priorities among the operations, the program transform expressions from infix to postfix 
notations. The program also deals with the entries provided by the users like multiples '+'.
"""
