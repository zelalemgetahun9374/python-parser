import re
from models import Condition, ConditionalBlock, Block, FunctionBlock, Node, GlobalBlock

graph = Node()
sample = "test 2.py"

no_of_tabs = 0
identation_expression = r"^([ ]+)?"
conditional_expression = r"^(if|while|elif)[ ]?\(?(True|False|.+)?\)?:"
else_expression = r"^(else)"
block_buffer = []
condition_stack = []

for_else = []

def main():
    global no_of_tabs, block_buffer, condition_stack
    print("opening: {0}".format(sample))
    with open(sample) as file:
        lines = file.readlines()
        for eachline in lines:
            eachline = eachline.strip()
            matched = re.match(identation_expression, eachline).groups()
            if matched[0] is not None:
                tabs = len(matched[0])
            else:
                tabs = 0
            if tabs > no_of_tabs:
                block_buffer = [eachline]
            elif tabs < no_of_tabs:
                conditional_block = ConditionalBlock(condition_stack, Block(block_buffer))
                graph.connect(conditional_block)
                condition_stack.pop()
                # if(isOnElse):
                #     condition_stack.pop()
            else:
                block_buffer.append(eachline)
            no_of_tabs = tabs
            print("inside :", " AND ".join(map(lambda x: "'{0}'".format(x), condition_stack if len(condition_stack) > 0 else ["global"])), end=" ")
            print("   ------------->  ", eachline.strip()) 
            is_conditional_statement = re.match(conditional_expression, eachline.strip())
            is_else_conditional_statement = re.match(else_expression, eachline.strip())
            if is_conditional_statement is not None:
                if eachline.startswith('elif'):
                    condition_stack.pop()
                condition_stack.append(Condition(is_conditional_statement.groups()[0], is_conditional_statement.groups()[1]))
                for_else.append(Condition(is_conditional_statement.groups()[0], is_conditional_statement.groups()[1]))
                no_of_tabs -= 1
                isOnElse = False

            elif is_else_conditional_statement is not None:
                condition_stack.append(condition_stack.pop().negate())
                no_of_tabs -= 1
                isOnElse = True
                condition_stack.pop()
            else:
                isOnElse = False
           
if __name__ == '__main__':
    main()
    print(graph._neighbours)
