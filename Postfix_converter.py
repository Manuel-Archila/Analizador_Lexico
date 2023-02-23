class Postfix_converter(object):
    def __init__(self, regex):
        self.operands = ["|", "+", "*", ".", "?"]
        self.b_operands = ["|", "."]
        self. u_operands = ["+", "*"]
        self.regex = regex
        self.toPostFix()
        self.postfix = self.parseRegex(self.postfix)
    
    def parseRegex(self, regex):
        replaced_regex = regex.replace("?", "ε|")
        #print(replaced_regex)
        return replaced_regex

    
    def isOperand(self, character):
        operands= ["|", ".", "+", "*"]
        return character not in operands

    
    def concatenations(self, regex):
        new_regex = ""
        for i in range(len(regex)):
            character = regex[i]
            try:
                next_character = regex[i+1]
                if (character != '(' and next_character != ')' and next_character not in self.operands and character not in self.b_operands):
                    new_regex += regex[i] + "."
                else:
                    new_regex += regex[i]
            except:
                new_regex += regex[i]
                #print(new_regex)
        return new_regex
    

    def getPrecedence(self, c):
        if c == '(':
            return 1
        if c == '|':
            return 2
        if c == '.':
            return 3
        if c == '*':
            return 4
        if c == '+':
            return 4
        else:
            return 6
        
    # Codigo extraido de https://gist.github.com/gmenard/6161825
    def toPostFix(self):
        cadena = self.concatenations(self.regex)
        print(cadena)
        postfix = ''
        stack = []
        for c in cadena:
            if c == '(':
                stack.append(c)
            elif c == ')':
                while stack[-1] != '(':
                    postfix += stack.pop()
                stack.pop()
            else:
                while len(stack) > 0:
                    peeked = stack[-1]

                    peekedPrecedence = self.getPrecedence(peeked)
                    currentPrecedence = self.getPrecedence(c)

                    if peekedPrecedence >= currentPrecedence:
                        postfix += stack.pop()
                    else:
                        break
                stack.append(c)
        while len(stack) > 0:
            postfix += stack.pop()
        self.postfix = postfix

        return postfix