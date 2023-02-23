class Checker(object):
    def __init__(self, regex):
        self.regex = regex
        self.operands = ["|", "+", "*", ".", "?"]
        self.b_operands = ["|", "."]
        self. u_operands = ["+", "*"]

    
    def checkRegex(self):
        #print(len(self.regex))
        errors = []
        self.regex = self.regex.replace(" ", "")
        #print(len(self.regex))
        if self.regex == "":
            return False, "Error: no ingreso una expresion regular", self.regex
        
        closing_par = 0
        opening_par = 0
        for i in range(len(self.regex)):
            if self.regex[i] == " ":
                self.regex[i] = ""

            if closing_par > opening_par:
                return False, "Error: hay un parentesis de cierre antes de un parentesis de apertura.", self.regex
            
            if self.regex[i] == "(":
                opening_par += 1
            elif self.regex[i] == ")":
                closing_par += 1
            
            if self.regex[i] == "(" and self.regex[i + 1] in self.operands:
                return False, "Error: no puede haber un operador despues de un parentesis de apertura.", self.regex
            
            try:
                if self.regex[i] == "(" and self.regex[i + 1] == ")":
                    return False, "Error: existen parentesis vacios."
                
                if self.regex[i] in self.operands and self.regex[i + 1] in self.operands:
                    return False, "Error: no puede haber dos operadores seguidos.", self.regex
            except:
                pass

        if opening_par != closing_par:
            return False, "Error: en la expresion regular, no hay el mismo numero de parentesis de apertura y cierre.", self.regex
        
        if self.regex[0] in self.operands:
            return False, "Error: en la expresion regular, no puede empezar con un operador.", self.regex
        
        if self.regex[-1] in self.b_operands:
            return False, "Error: en la expresion regular, no puede terminar con un operador binario.", self.regex
        
        return True, "Expresion regular aceptada.", self.regex