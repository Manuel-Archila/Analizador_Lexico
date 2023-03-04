class Checker(object):
    def __init__(self, regex):
        self.regex = regex
        self.operands = ["|", "+", "*", ".", "?"]
        self.b_operands = ["|", "."]
        self. u_operands = ["+", "*"]

    
    def checkRegex(self):
        #print(len(self.regex))
        valid = True
        errors = []
        self.regex = self.regex.replace(" ", "")
        #print(len(self.regex))
        if self.regex == "":
            errors.append("Error: no ingreso una expresion regular")
            return False, self.regex
        
        closing_par = 0
        opening_par = 0
        for i in range(len(self.regex)):
            if self.regex[i] == " ":
                self.regex[i] = ""

            
            if self.regex[i] == "(":
                opening_par += 1
            elif self.regex[i] == ")":
                closing_par += 1
            
            if closing_par > opening_par:
                errors.append("Error: hay un parentesis de cierre antes de un parentesis de apertura.")
                valid = False

            if self.regex[i].isalnum() == False and self.regex[i] not in self.operands and self.regex[i] != "(" and self.regex[i] != ")" and self.regex[i] != "ε":
                errors.append("Error: caracter invalido.")
                valid = False
            
            try:
                if self.regex[i] == "(" and self.regex[i + 1] in self.operands:
                    errors.append("Error: no puede haber un operador despues de un parentesis de apertura.")
                    valid = False

                if self.regex[i] == "(" and self.regex[i + 1] == ")":
                    errors.append("Error: no puede haber un parentesis de apertura seguido de un parentesis de cierre.")
                    valid = False

                if self.regex[i] in self.b_operands and self.regex[i + 1] in self.b_operands:
                    errors.append("Error: no puede haber dos operadores binarios seguidos.")
                    valid = False

                if self.regex[i] in self.b_operands and self.regex[i + 1] in self.u_operands:
                    errors.append("Error: no puede haber un operador unario sobre un operador binaro.")
                    valid = False
                    
            except:
                pass


        if opening_par != closing_par:
            errors.append("Error: no hay el mismo numero de parentesis de apertura y cierre.")
            valid = False
        
        if self.regex[0] in self.operands:
            errors.append("Error: no puede empezar con un operador.")
            valid = False
        
        if self.regex[-1] in self.b_operands:
            errors.append("Error: en la expresion regular, no puede terminar con un operador binario.")
            valid = False
        
        return valid, errors, self.regex