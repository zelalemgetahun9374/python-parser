class Node:
    def __init__(self):
        self._neighbours = []
    
    def connect(self, node):
        self._neighbours.append(node)
    
class FunctionBlock(Node):
    def __init__(self, block, arguments = []):
        super().__init__()
        self._function_body = block
        self._arguments = arguments

    def getBody(self):
        return self._function_body
    
    def getArguments(self):
        return self._arguments

class ConditionalBlock(Node):
    def __init__(self, condition, block, negated = False):
        super().__init__()
        self._condition = condition
        self._block = block
        self._negated = negated

    def getBody(self):
        return self._block
    
    def __repr__(self):
        return "\n\nexpr: {0}\ntype: {1}\n\n".format(" AND ".join(map(lambda x: x.getExpression(), self._condition)), "".join(self._block.getCode()))

class GlobalBlock(Node):
    def __init__(self, block):
        super().__init__()
        self._block = block

    def getBody(self):
        return self._block


class Block:
    def __init__(self, code):
        self._code = code
    
    def getCode(self):
        return self._code   
 
class Condition:
    def __init__(self, statement, expression, negated = False):
        self._statement = statement
        self._expression = expression
        self._negated = negated

    def getExpression(self):
        return self._expression
    
    def negate(self):
        return Condition(self._statement, self._expression, negated = True)

    def __str__(self):
        return "block with: "+ ("!" if self._negated else "") + self._expression + " == True"
    
    def __repr__(self):
        return self._expression