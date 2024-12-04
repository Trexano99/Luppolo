
from src.utils.LuppoloLogger import LuppoloLogger
from src.ast.elements.Function import Function
from src.ast.elements.expression.BinOp import BinOp
from src.ast.elements.condition.BinCond import BinCond
from src.ast.elements.condition.TrueFalse import TrueFalse


from src.ast.elements.instruction.Assignment import Assignment

from src.expression.leaf import *
from src.expression.nodes import *

class LuppoloInterpreter:

    def __init__(self, functions):
        self.functions = functions

    def interpretFunc(self, funcName="Main", params=[]):
        '''
        This funciont is an iterative interpreter for a Luppolo function.
        '''
        # Il dizionario che mappa gli ID con i loro valori
        ID_MEM = {}
        # Lo stack dei nodi da eseguire. Tupla (nodo, vis), dove vis indica se i figli del nodo sono stati visitati
        INSTR_STACK = []
        # Lo stack dei valori computati
        VALUE_STACK = []

        # Controllo che la funzione chiamata esista
        if funcName not in self.functions:
            LuppoloLogger.logError(err:=f"Function {funcName} not found.")
            raise LuppoloInterpException(self)
        
        # Controllo che il numero di parametri passati alla funzione sia corretto
        if len(params) != len(expFuncParams :=self.functions[funcName].funcParams):
            error = f"Function {funcName} called with wrong number of parameters."
            error += f"Expected {len(expFuncParams)} [{[param.value for param in expFuncParams]}]"
            error += f", got {len(params)} [{params}]."
            
            LuppoloLogger.logError(error)
            raise LuppoloInterpException(self)
        
        interpFunc : Function = self.functions[funcName]

        INSTR_STACK = [(instr, False) for instr in reversed(interpFunc.children)]

        while INSTR_STACK:
            node, visited = INSTR_STACK.pop()
            match node.__class__.__name__:

            ##########
            # BLOCCO #
            ##########

                case "InstrBlock":
                    INSTR_STACK.extend([(instr, False) for instr in reversed(node.children)])


            ##############
            # ISTRUZIONI #
            ##############

                case "Assignment":
                    # Se il nodo è già stato visitato, allora possiamo eseguire
                    # l'assegnamento prendendo il valore dallo stack 
                    if visited:
                        ID_MEM[node.varName] = VALUE_STACK.pop()
                    
                    # Altrimenti dobbiamo visitare l'espessione 
                    else:
                        INSTR_STACK.append((node, True))
                        INSTR_STACK.append((node.children[0], False))

                case "Foreach":
                    expr, block = node.children
                    # Se abbiamo già visitato il nodo, allora rimuoviamo la variabile
                    # utilizzata dalla memoria. Non succede se la variabile era già
                    # presente prima di entrare nel ciclo. Vedi commenti sotto.
                    if visited:
                        ID_MEM[node.varName] = None
                    else:
                        # Se stiamo sovrascrivendo una variabile già esistente ci 
                        # salviamo come assegnamento il suo valore per ripristinarlo
                        # alla fine del ciclo. Non serve visitare nuovamente questo nodo
                        if node.varName in ID_MEM:
                            INSTR_STACK.append((Assignment(node.varName, ID_MEM[node.varName]), False))
                        # Altrimenti visitiamo nuovamente il nodo che rimuoverà 
                        # dalla memoria la variabile utilizzata
                        else:
                            INSTR_STACK.append(node, True)

                        # Appendiamo per ogni elemento nell'espressione il blocco di istruzioni
                        # ma prima andiamo ad assegnare il valore dell'espressione alla variabile
                        for exprEl in reversed(expr.children):
                            INSTR_STACK.append(block, False)
                            INSTR_STACK.append((Assignment(node.varName, exprEl), False))
                
                case "IfElse":
                    cond, trueBlock = node.children[:2]
                    falseBlock = node.children[2] if len(node.children) == 3 else None
                    # Se il nodo è già stato visitato, allora valutiamo la condizione
                    # e decidiamo quale blocco di istruzioni eseguire
                    if visited:
                        if VALUE_STACK.pop():
                            INSTR_STACK.append(trueBlock, False)
                        elif falseBlock is not None:
                            INSTR_STACK.append(falseBlock, False)
                    # Altrimenti valutiamo la condizione e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append(node, True)
                        INSTR_STACK.append(cond, False)
            
                case "Repeat":
                    expr, block = node.children

                    # Se il valore dell'espressione di repeat non è un intero positivo
                    # segnalo l'errore e sollevo un'eccezione
                    if not expr.__class__.__name__ == "Rational" or expr.denominator != 1 or expr.negated:
                        LuppoloLogger.logError("Repeat expression must be a positive integer number.")
                        raise LuppoloInterpException(self)
                    
                    INSTR_STACK.extend([(block,False) for _ in range(expr.numerator)])

                case "Return":
                    
                    # Se il nodo è già stato visitato, allora possiamo restituire il valore
                    if visited:
                        return VALUE_STACK.pop()
                    # Altrimenti visitiamo l'espressione e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append(node, True)
                        INSTR_STACK.append(node.children[0], False)
                    
                case "While":
                    cond, block = node.children
                    # Se il nodo è già stato visitato, allora valutiamo il risultato della condizione
                    if visited:
                        # Se la condizione è vera, allora eseguo il blocco e torno a rieseguire me stesso
                        if VALUE_STACK.pop():
                            INSTR_STACK.append(node, False)
                            INSTR_STACK.append(block, False)
                    # Se il nodo non è stato visitato, valutiamo la condizione e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append(node, True)
                        INSTR_STACK.append(cond, False)


            ###############
            # ESPRESSIONI #
            ###############
                
                case "NAT":
                    VALUE_STACK.append(Rational(node.value), negated=node.negated)

                case "SYM":
                    VALUE_STACK.append(Symbol(node.value), negated=node.negated)
                
                case "ID":
                    # Controllo che la variabile sia stata definita
                    if node.varName not in ID_MEM:
                        LuppoloLogger.logError(f"Variable {node.varName} not found.")
                        raise LuppoloInterpException(self)
                    
                    VALUE_STACK.append(ID_MEM[node.varName].copy_with())

                case "BinOp":
                    # Se il nodo è già stato visitato, allora possiamo eseguire l'operazione
                    if visited:
                        left = VALUE_STACK.pop()
                        right = VALUE_STACK.pop()
                        match node.op:
                            case BinOp.BinOpType.SUM:
                                VALUE_STACK.append(Add(left, right, node.negated).simplify())
                            case BinOp.BinOpType.SUB:
                                right = right.copy_with(negated = not right.negated)
                                VALUE_STACK.append(Add(left, right, node.negated).simplify())
                            case BinOp.BinOpType.MUL:
                                VALUE_STACK.append(Mult(left, right, node.negated).simplify())
                            case BinOp.BinOpType.DIV:
                                VALUE_STACK.append(Mult(left, Pow(right, Rational(-1)), node.negated).simplify())
                            case BinOp.BinOpType.POW:
                                VALUE_STACK.append(Pow(left, right, node.negated).simplify())
                    # Altrimenti dobbiamo visitare i figli. Aggiungiamo allo stack prima
                    # il nodo stesso, poi il nodo di sinistra e dunque il destro.
                    # Così nell'esecuzione verrà eseguito prima il destro e messo nello 
                    # stack dei valori, dunque il sinistro e infine nuovamente l'operazione.
                    # Il primo risultato estratto sarà dunque il sinistro, il secondo il destro.
                    else:
                        INSTR_STACK.append(node, True)
                        INSTR_STACK.append(node.children[0], False)
                        INSTR_STACK.append(node.children[1], False)


            ##############
            # CONDIZIONI #
            ##############                

                case "BinCond":

                    # Se il nodo è già stato visitato, allora possiamo eseguire la condizione
                    if visited:
                        left = VALUE_STACK.pop()
                        right = VALUE_STACK.pop()
                        match node.op:
                            case BinCond.BinCondType.EQ:
                                VALUE_STACK.append(left == right)
                            case BinCond.BinCondType.GREATER:
                                VALUE_STACK.append(right < left)
                            case BinCond.BinCondType.GEQ:
                                VALUE_STACK.append((right < left) or (right == left))
                            case BinCond.BinCondType.LESS:
                                VALUE_STACK.append(left < right)
                            case BinCond.BinCondType.LEQ:
                                VALUE_STACK.append((left < right) or (left == right))
                            case BinCond.BinCondType.AND:
                                VALUE_STACK.append(left and right)
                            case BinCond.BinCondType.OR:
                                VALUE_STACK.append(left or right)

                    # Altrimenti dobbiamo visitare i figli. Vedi spiegazione ordine in BinOp.
                    else:
                        INSTR_STACK.append(node, True)
                        INSTR_STACK.append(node.children[0], False)
                        INSTR_STACK.append(node.children[1], False)

                case "TrueFalse":
                    VALUE_STACK.append(True if node.value == TrueFalse.TrueFalseType.TRUE else False)

                
            ##############
            # FUNCCALL #
            ##############  

                case "FuncCall":
                    
                    # Se il nodo è già stato visitato, allora possiamo eseguire la funzione
                    if visited:
                        funcName = node.funcName
                        params = [VALUE_STACK.pop() for _ in range(len(node.children))]
                        
                        VALUE_STACK.append(self.interpretFunc(funcName, params))

                    # Altrimenti valutiamo i parametri e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append(node, True)
                        for arg in node.args:
                            INSTR_STACK.append(arg, False)
                        

                case _:
                    LuppoloLogger.logError(f"Node {node.__class__.__name__} not recognized to be interpretated.")
                    raise LuppoloInterpException(self)
                
        # Se non è stato restituito nulla, allora la funzione non ha un return statement
        LuppoloLogger.logError(f"Function {funcName} has no return statement.")
        raise LuppoloInterpException(self)
        




class LuppoloInterpException(Exception):

    verboseLog = True
    
    def __init__(self,interpreter):
        errorMessage = "An error occurred during the interpretation of the program. Read logs for more info"
        if LuppoloInterpException.verboseLog:
            errorMessage += f"ID_MEM: {interpreter.ID_MEM}\n"
            errorMessage += f"INSTR_STACK: {interpreter.INSTR_STACK}\n"
            errorMessage += f"VALUE_STACK: {interpreter.VALUE_STACK}\n"
        super().__init__(errorMessage)