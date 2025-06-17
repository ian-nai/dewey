import sys
import re

master_statement_list = []

num_to_letter_dict = {
    "0": "0",
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h",
    "9": "i",
    "10": "j",
    "11": "k",
    "12": "l",
    "13": "m",
    "14": "n",
    "15": "o",
    "16": "p",
    "17": "q",
    "18": "r",
    "19": "s",
    "20": "t",
    "21": "u",
    "22": "v",
    "23": "w",
    "24": "x",
    "25": "y",
    "26": "z"
}

letter_to_num_dict = {v: k for k, v in num_to_letter_dict.items()}


def process_file(filename):
    with open(filename, 'r') as f:
        content = [line.rstrip() for line in f]
        parse(content)

def parse(program: list[str]):
    # remove all comments
    program_without_comments = []
    sep = '#'

    for line in program:
        comments_removed = line.split(sep, 1)[0]
        program_without_comments.append(comments_removed)

    program_without_comments = [x for x in program_without_comments if x] 
    program_without_comments = [x.strip(' ') for x in program_without_comments]
    
    interpret(program_without_comments)


def interpret(statements: list[str]):

    line_stack = []

    split_statements_list = []
    for statement in statements:
        split_statement = []
        if " " in statement:
            split_statement_1 = statement.split(".")
            split_statement.append(split_statement_1[0])
            for s in split_statement_1:
                if " " in s:
                    split_statement_2 = s.split(" ")
                    for x in split_statement_2:
                        split_statement.append(x)
            split_statements_list.append(split_statement)
        else:
            split_statement_1 = statement.split(".")
            split_statements_list.append(split_statement_1)

    for statement in split_statements_list:
        statement_level_intepretation(statement)
    
    execute_statements(master_statement_list)

def statement_level_intepretation(statement_to_interpret: list[str]):
    statement_stack = []
    for idx,x in enumerate(statement_to_interpret):
        if idx == 0:
            first_parsed_statement, digits_or_string, operator_location = first_section_parsing(x)
            statement_stack.append(first_parsed_statement)
        if idx == 1:
            second_parsed_statement = second_section_parsing(x, digits_or_string, operator_location)
            statement_stack.append(second_parsed_statement)
        if idx == 2:
            third_parsed_statement = third_section_parsing(x, digits_or_string, operator_location)
            statement_stack.append(third_parsed_statement)
        if idx >= 3:
            print("Your statement is too long; it should follow this format: 123.123 Example")

    master_statement_list.append(statement_stack)

def first_section_parsing(first_section: list[str]):
    digits_or_string = 0
    operator_location = 0
    stack_one = []

    for idx, digit in enumerate(first_section):
        if idx == 0:
            if digit == "0":
                stack_one.append("print")
            if digit == "1":
                stack_one.append("var")
            if digit == "2":
                stack_one.append("quotes")
            if digit == "3":
                if first_section[2] == "1":
                    stack_one.append('if')
                elif first_section[2]  == "2":
                    stack_one.append('then')
                elif first_section[2]  == "3":
                    stack_one.append('else')
                elif first_section[2]  == "4":
                    stack_one.append('while')
            if digit == "4":
                if first_section[2] == "1":
                    stack_one.append('+')
                elif first_section[2]  == "2":
                    stack_one.append('-')
            if digit == "5" :
                if first_section[2] == "1":
                    stack_one.append('*')
                elif first_section[2]  == "2":
                    stack_one.append('/')
            if digit == "6":
                stack_one.append('==')
            if digit == "7" :
                stack_one.append('(')
            if digit == "8":
                stack_one.append(')')
            if digit == "9":
                stack_one.append("multiline")

        elif idx == 1:
            if digit == "1":
                digits_or_string = 1
            elif digit == "2":
                digits_or_string = 2
            if digit == "3":
                digits_or_string = 3
            elif digit == "4":
                digits_or_string = 4
            elif digit == "5":
                stack_one.append(' null ')
            elif digit == "6":
                digits_or_string = 6
        

        elif idx == 2:
            operator_location = int(digit)

    if "multiline" in stack_one:
        stack_one.append(str(operator_location))

    stack_one_str = "".join(stack_one)

    return stack_one_str, digits_or_string, operator_location 

def second_section_parsing(second_section: str, digits_or_string: int, operator_location: int):   
    second_section_punct = ""
    second_section_new = ""
    if ":" in second_section:
        split_second_statement = second_section.split(":")
        second_section_punct = split_second_statement[1]
        second_section_new = split_second_statement[0]

    stack_two = []
    second_stack_var = []
    
    enumerating_list = ""

    if second_section_new:
        enumerating_list = second_section_new
    else:
        enumerating_list = second_section
    
    for idx, digit in enumerate(enumerating_list):
        if digits_or_string == 0:
            second_stack_var.append(digit)
        elif digits_or_string == 1:
            if operator_location != 0:
                # keeping non-operator numbers as integers
                if idx != (operator_location - 1):
                    second_stack_var.append(num_to_letter_dict[digit])
                # converting the integer to a letter at the operator location
                else:
                    second_stack_var.append(num_to_letter_dict[digit])
            else:
                second_stack_var.append(num_to_letter_dict[digit])
        elif digits_or_string == 2:
            if operator_location != 0:
                # converting all non-operator digits to letters
                if idx != (operator_location - 1):
                    second_stack_var.append(num_to_letter_dict[digit])
                # capitalizing the letter at our operator location
                else:
                    second_stack_var.append(num_to_letter_dict[digit].capitalize())
            else:
                second_stack_var.append(num_to_letter_dict[digit].capitalize())
        elif digits_or_string >= 7:
            print("Error! Please ensure the second number in your first sequence of three numbers is between 0 and 6.")

        elif digits_or_string == 3:
            if operator_location != 0:
                 # converting all non-operator digits to letters
                if idx != (operator_location - 1):
                    second_stack_var.append(num_to_letter_dict[digit].capitalize())
                # capitalizing the letter at our operator location
                else:
                    second_stack_var.append(num_to_letter_dict[digit])
            else:
                second_stack_var.append(num_to_letter_dict[digit])

                
    # if a variable was declared
    if digits_or_string == 4:
        if operator_location == 0:
            for el in second_section:   
                    second_stack_var.append(el)
        # lowercase
        elif operator_location == 1:
            for el in second_section:   
                second_stack_var.append(num_to_letter_dict[el])
        # uppercase
        else:
             for el in second_section:   
                second_stack_var.append(num_to_letter_dict[el].capitalize())
    
    # if a number has a double digit integer correlate
    if digits_or_string == 6:
        # lowercase
        if operator_location == 0 or operator_location == 1:
            second_stack_var.append(num_to_letter_dict[second_section])
        # uppercase
        else:
            second_stack_var.append(num_to_letter_dict[second_section].capitalize())


    # parsing any numbers after the colon, if one is present
    if second_section_punct:
        for idx, digit in enumerate(second_section_punct):
            if digit == "1":
                second_stack_var.append(":")
            elif digit == "2":
                second_stack_var.append("\t")
            elif digit == "3":
                second_stack_var.append("!")
            elif digit == "4":
                second_stack_var.append("{")
            elif digit == "5":
                second_stack_var.append("}")
            elif digit == "6":
                second_stack_var.append(" ")

    # taking our individual integers or letters and putting them together
    appendable_second_stack_var = ''.join(second_stack_var)
    stack_two.append(appendable_second_stack_var)
    stack_two_str = "".join(stack_two)

    return stack_two_str



def third_section_parsing(third_section: list[str], digits_or_string: int, operator_location: int):

    stack_three = []
    third_stack_var = []
    for letter in third_section:
        if digits_or_string == 0:
            # converting digits to lowercase letters 
            third_stack_var.append(letter_to_num_dict[letter.lower()])
        # making variable names lowercase, as well
        elif digits_or_string == 4:
            third_stack_var.append(letter.lower())
        else:
            third_stack_var.append(letter)
    
    if operator_location == 7:
        third_stack_var.append(" ")
    appendable_third_stack_var = ''.join(third_stack_var)
    stack_three.append(appendable_third_stack_var)
    
    stack_three_str = "".join(stack_three)
    return stack_three_str

def execute_statements(master_statement_list: list[str]):
    # converting our statement stacks to Python code and executing it

    # tracking if a statement is multiline or single
    multiline_tracker = False

    first_pass_list = []
    second_pass_list = []
    executable_string = ""
    joined_statement_list = []
    
    for list_of_statements in master_statement_list:
        # printing our statements if the first command in the statement is 'print'
        if list_of_statements[0] == "print":
            printable_string = []
            if list_of_statements[1].isalpha():
                #if list_of_statements[2]:
                if 0 <= 2 < len(list_of_statements):
                     new_string = '"' + list_of_statements[1] + list_of_statements[2] + '"'
                else:
                    new_string = '"' + list_of_statements[1] + '"'

                printable_string.append(new_string)
                printable_string.insert(0, "print(")
                printable_string.append(")")
                first_pass_list.append("".join(printable_string))
            # appending only "print"
            elif list_of_statements[1] == "000":
                first_pass_list.append("print")
            # handling integers for print statements
            else:
                new_string = 'int(' + list_of_statements[1] + ')'
                printable_string.append(new_string)
                printable_string.insert(0, "print(")
                printable_string.append(")")
                first_pass_list.append("".join(printable_string))

        elif list_of_statements[0].strip() == "quotes null":
                to_add_to = list_of_statements[1:]               
                joined_list = "".join(to_add_to)
                first_pass_list.append(joined_list)

        elif list_of_statements[0] == "quotes":
                to_add_to = list_of_statements[1:]
                to_add_to.insert(0, '"')
                to_add_to.append('"')

                joined_list = "".join(to_add_to)
                first_pass_list.append(joined_list)

        elif list_of_statements[0] == "if" or list_of_statements[0] == "then":
            joined_statement = ' '.join(list_of_statements) 
            first_pass_list.append(joined_statement)

        elif list_of_statements[0] == "var":
           list_of_statements.append(' = ')
           list_of_statements.append(list_of_statements.pop(1))
           joined_statement = ' '.join(list_of_statements) 
           first_pass_list.append(joined_statement)

        else:
            if master_statement_list.index(list_of_statements) != 0:
                joined_statement = ' '.join(list_of_statements) 
                first_pass_list.append(joined_statement)
            else:
                joined_statement = ' '.join(list_of_statements) 
                first_pass_list.append(joined_statement)

    for joined_statements in first_pass_list:
        if "multiline" in joined_statements:
            num_of_lines = joined_statements.split()[1]
            start_index = first_pass_list.index(joined_statements)
            lines_in_statement = get_next_n_elements(first_pass_list, start_index + 1, int(num_of_lines))
            tab_counter = 0
            indented = False
            # removing the statements from our lines_in_statement list to avoid duplicates after parsing the multiline statement  
            for line in lines_in_statement:
                first_pass_list.remove(line)
            
            for idx, line in enumerate(lines_in_statement):
                # making sure our string prints by appending () and quotation marks
                if indented == False:
                    if "\t" in lines_in_statement[idx - 1]:
                        if idx == int(num_of_lines) - 1:
                            joined_statement_list.append("\t" + line + '\n')
                            indented = True
                            tab_counter +=1
                        else:
                            joined_statement_list.append("\t" + line)
                            indented = True
                            tab_counter +=1
                    else:
                        if idx == int(num_of_lines) - 1:
                            joined_statement_list.append(line + '\n')
                        else:
                            joined_statement_list.append(line)
                
                elif indented == True:
                    if tab_counter >= 1:
                        if "\t" not in lines_in_statement[idx - 1]:
                            if idx == int(num_of_lines) - 1:
                                joined_statement_list.append(("\t" * tab_counter) + line + '\n')
                            else:
                                joined_statement_list.append(("\t" * tab_counter) + line)
                        elif "\t" in lines_in_statement[idx - 1]:
                            if idx == int(num_of_lines) - 1:
                                joined_statement_list.append(("\t" * tab_counter) + line + '\n')
                                tab_counter += 1
                            else:
                                joined_statement_list.append(("\t" * tab_counter) + line)
                                tab_counter += 1

            final_string = ''.join(joined_statement_list)
            executable_string += final_string

            multiline_tracker = False
        else:
            joined_statement_list.append(joined_statements + '\n')

    almost_final_statement_list = []
    for x in joined_statement_list:
        new_string = x.replace('000', '')
        new_string_2 = new_string.replace('var', '')
        almost_final_statement_list.append(new_string_2)

    final_statement_list = []
    for idx, statement in enumerate(almost_final_statement_list):
        new_statement = statement.strip()
        if new_statement[-1] == ":":
            appended_statement = new_statement + "\n"
            final_statement_list.append(appended_statement)
        else:
            final_statement_list.append(statement)
        
    executable_string = ''.join(final_statement_list)
    executable_string.strip()
    execute_code(executable_string.strip())

def execute_code(executable_string):
    exec(executable_string)

            
def get_next_n_elements(data_list, start_index, n):
    if start_index + n <= len(data_list):
        return data_list[start_index:start_index + n]
    else:
        return []
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the filename as an argument.")
    else:
        filename = sys.argv[1]
        process_file(filename)