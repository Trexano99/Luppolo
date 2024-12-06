
from src.utils.LuppoloLogger import LuppoloLogger
from src.ast.elements.Function import Function
from src.ast.elements.expression.BinOp import BinOp
from src.ast.elements.condition.BinCond import BinCond
from src.ast.elements.condition.TrueFalse import TrueFalse


from src.ast.elements.instruction.Assignment import Assignment

from src.expression.leaf import *
from src.expression.nodes import *

class LuppoloInterpreter:
    '''
    LuppoloInterpreter is an interpreter for the Luppolo programming language. It interprets
    functions defined in the language and executes them iteratively.
    '''


    def __init__(self, functions):
        '''
        This function initializes the interpreter with the functions to interpret.
        If there are multiple functions with the same name and the same number of parameters,
        an error is raised.
        '''

        # Controllo che non ci siano funzioni con lo stesso nome e lo stesso numero di parametri
        for func in functions:
            if any([len(f.funcParams) == len(func.funcParams) for f in functions if func.funcName.value == f.funcName.value and id(f) != id(func)]):
                LuppoloLogger.logError(f"Function {func.funcName.value} defined multiple times.")
                raise Exception("An error occurred during the initialization of the interpreter. Read logs for more info.")
        
        self.functions = functions

    def interpretFunc(self, funcName="Main", params=[]):
        '''
        This function is an iterative interpreter for a Luppolo function.
        '''

        # Il dizionario che mappa gli ID con i loro valori
        ID_MEM = {}
        # Lo stack dei nodi da eseguire. Tupla (nodo, vis), dove vis indica se i figli del nodo sono stati visitati
        INSTR_STACK = []
        # Lo stack dei valori computati. Possono essere espressioni o risultati di condizioni
        VALUE_STACK = []

        # La memoria della funzione. Utilizzata per il log in caso di errore
        funcMem = (ID_MEM, INSTR_STACK, VALUE_STACK)

        # Controllo che la funzione chiamata esista
        if not any([funcName == func.funcName.value for func in self.functions]):
            LuppoloLogger.logError(f"Function {funcName} not found.")
            raise LuppoloInterpException(funcMem)
        
        # Estraggo la funzione chiamata
        interpFunc : Function = next((func for func in self.functions if func.funcName.value == funcName and len(func.funcParams) == len(params)), None)
        
        # Se non è stata trovata una funzione con lo stesso numero di parametri, allora segnalo l'errore
        if interpFunc is None:
            error = f"Function {funcName} with {len(params)} parameters not found."
            possibleAlternative =  [func for func in self.functions if func.funcName.value == funcName]
            error += "\nPossible alternatives are:"
            for func in possibleAlternative:
                error += f"\n{func.funcName.value}({[param.value for param in func.funcParams]})"

            LuppoloLogger.logError(error)
            raise LuppoloInterpException(funcMem)

        # Controllo che non ci siano parametri con lo stesso nome
        if len([par.value for par in interpFunc.funcParams]) != len({par.value for par in interpFunc.funcParams}):
            LuppoloLogger.logError(f"Function {funcName} has multiple parameters with the same name. Ambiguity is not allowed.")
            raise LuppoloInterpException(funcMem)
        
        #Carico in memoria i parametri passati alla funzione
        for param, value in zip(interpFunc.funcParams, params):
            ID_MEM[param.value] = value

        # Carico nello stack delle istruzioni le istruzioni della funzione
        INSTR_STACK = [(instr, False) for instr in reversed(interpFunc.children)]

        # Ciclo finchè ci sono istruzioni da eseguire
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
                    
                    # Se il nodo passato nell'assegnamento è un'espressione, allora
                    # lo salviamo direttamente nella memoria.
                    # Questo è utile nei casi in cui si voglia asseggnare un valore
                    # già computato in un altro step. Vedi Foreach. 
                    if isinstance(node.children[0], BaseLuppExpr):
                        ID_MEM[node.varName.value] = node.children[0]
                        continue

                    # Se il nodo è già stato visitato, allora possiamo eseguire
                    # l'assegnamento prendendo il valore dallo stack 
                    if visited:
                        ID_MEM[node.varName.value] = VALUE_STACK.pop()
                    
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
                        evaluatedExpr = VALUE_STACK.pop()
                        print("DEBUG: IN FOREACH. Expr :", evaluatedExpr)
                        if isinstance(evaluatedExpr, Add) or isinstance(evaluatedExpr, Mult):
                            foreachExpr = evaluatedExpr.children
                        else:
                            foreachExpr = [evaluatedExpr]
                        print("DEBUG: IN FOREACH. Expr :", foreachExpr)
                        # Appendiamo per ogni elemento nell'espressione il blocco di istruzioni
                        # ma prima andiamo ad assegnare il valore dell'espressione alla variabile
                        for exprEl in foreachExpr:
                            INSTR_STACK.append((block, False))
                            INSTR_STACK.append((Assignment(node.varName, exprEl), False))
                    else:
                        # Se stiamo sovrascrivendo una variabile già esistente ci 
                        # salviamo come assegnamento il suo valore per ripristinarlo
                        # alla fine del ciclo. 
                        if node.varName.value in ID_MEM:
                            INSTR_STACK.append((Assignment(node.varName, ID_MEM[node.varName.value]), False))
                        # Altrimenti aggiungiamo la funzione di rimozione del nodo
                        else:
                            param = node.varName.value
                            def remove_var():
                                del ID_MEM[param]
                            INSTR_STACK.append((remove_var, False))
                        
                        # Aggiungo alle istruzioni il nodo da eseguire nuovamente dopo la valutazione
                        # dell'espressione.
                        INSTR_STACK.append((node, True))
                        # Aggiungo la valutazione dell'espressione
                        INSTR_STACK.append((expr, False))

                
                case "IfElse":
                    cond, trueBlock = node.children[:2]
                    falseBlock = node.children[2] if len(node.children) == 3 else None
                    # Se il nodo è già stato visitato, allora valutiamo la condizione
                    # e decidiamo quale blocco di istruzioni eseguire
                    if visited:
                        if VALUE_STACK.pop():
                            INSTR_STACK.append((trueBlock, False))
                        elif falseBlock is not None:
                            INSTR_STACK.append((falseBlock, False))
                    # Altrimenti valutiamo la condizione e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append((node, True))
                        INSTR_STACK.append((cond, False))
            
                case "Repeat":
                    expr, block = node.children

                    # Se il valore dell'espressione di repeat non è un intero positivo
                    # segnalo l'errore e sollevo un'eccezione
                    if not expr.__class__.__name__ == "Rational" or expr.denominator != 1 or expr.negated:
                        LuppoloLogger.logError("Repeat expression must be a positive integer number.")
                        raise LuppoloInterpException(funcMem)
                    
                    INSTR_STACK.extend([(block,False) for _ in range(expr.numerator)])

                case "Return":
                    
                    # Se il nodo è già stato visitato, allora possiamo restituire il valore
                    if visited:
                        return VALUE_STACK.pop()
                    # Altrimenti visitiamo l'espressione e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append((node, True))
                        INSTR_STACK.append((node.children[0], False))
                    
                case "While":
                    cond, block = node.children
                    # Se il nodo è già stato visitato, allora valutiamo il risultato della condizione
                    if visited:
                        # Se la condizione è vera, allora eseguo il blocco e torno a rieseguire me stesso
                        if VALUE_STACK.pop():
                            INSTR_STACK.append((node, False))
                            INSTR_STACK.append((block, False))
                    # Se il nodo non è stato visitato, valutiamo la condizione e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append((node, True))
                        INSTR_STACK.append((cond, False))


            ###############
            # ESPRESSIONI #
            ###############
                
                case "NAT":
                    VALUE_STACK.append(Rational(int(node.value), negated=node.negated).simplify())

                case "SYM":
                    VALUE_STACK.append(Symbol(node.value, negated=node.negated).simplify())
                
                case "ID":
                    # Controllo che la variabile sia stata definita
                    if node.value not in ID_MEM:
                        LuppoloLogger.logError(f"Variable {node.value} not found.")
                        raise LuppoloInterpException(funcMem)
                    
                    VALUE_STACK.append(ID_MEM[node.value].copy_with().simplify())

                case "BinOp":
                    # Se il nodo è già stato visitato, allora possiamo eseguire l'operazione
                    if visited:
                        left = VALUE_STACK.pop()
                        right = VALUE_STACK.pop()
                        match node.op:
                            case BinOp.BinOpType.SUM:
                                VALUE_STACK.append(Add([left, right], node.negated).simplify())
                            case BinOp.BinOpType.SUB:
                                right = right.copy_with(negated = not right.negated)
                                VALUE_STACK.append(Add([left, right], node.negated).simplify())
                            case BinOp.BinOpType.MUL:
                                VALUE_STACK.append(Mult([left, right], node.negated).simplify())
                            case BinOp.BinOpType.DIV:
                                VALUE_STACK.append(Mult([left, Pow(right, Rational(-1))], node.negated).simplify())
                            case BinOp.BinOpType.POW:
                                VALUE_STACK.append(Pow(left, right, node.negated).simplify())
                    # Altrimenti dobbiamo visitare i figli. Aggiungiamo allo stack prima
                    # il nodo stesso, poi il nodo di sinistra e dunque il destro.
                    # Così nell'esecuzione verrà eseguito prima il destro e messo nello 
                    # stack dei valori, dunque il sinistro e infine nuovamente l'operazione.
                    # Il primo risultato estratto sarà dunque il sinistro, il secondo il destro.
                    else:
                        INSTR_STACK.append((node, True))
                        INSTR_STACK.append((node.children[0], False))
                        INSTR_STACK.append((node.children[1], False))


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
                        INSTR_STACK.append((node, True))
                        INSTR_STACK.append((node.children[0], False))
                        INSTR_STACK.append((node.children[1], False))

                case "TrueFalse":
                    VALUE_STACK.append(True if node.value == TrueFalse.TrueFalseType.TRUE else False)

                
            ############
            # FUNCCALL #
            ############

                case "FuncCall":
                    
                    # Se il nodo è già stato visitato, allora possiamo eseguire la funzione
                    if visited:
                        funcName = node.funcName
                        params = [VALUE_STACK.pop() for _ in range(len(node.children))]
                        
                        VALUE_STACK.append(self.interpretFunc(funcName, params))

                    # Altrimenti valutiamo i parametri e torniamo a visitare il nodo
                    else:
                        INSTR_STACK.append((node, True))
                        for arg in node.children:
                            INSTR_STACK.append((arg, False))
                        
                    
            #################
            # LUPPOLOLAMBDA #
            #################

                case "function":
                    node()
                    

            #########
            # ALTRO #
            #########  

                case _:
                    LuppoloLogger.logError(f"Node {node.__class__.__name__} not recognized to be interpretated.")
                    raise LuppoloInterpException(funcMem)
                
        # Se non è stato restituito nulla, allora la funzione non ha un return statement
        LuppoloLogger.logError(f"Function {funcName} has no return statement.")
        raise LuppoloInterpException(funcMem)
        




class LuppoloInterpException(Exception):

    verboseLog = True
    
    def __init__(self,funcMem):
        errorMessage = "An error occurred during the interpretation of the program. Read logs for more info.\n"
        if LuppoloInterpException.verboseLog:
            errorMessage += "Function memory at the time of the error:\n"
            errorMessage += f"ID_MEM: {funcMem[0]}\n"
            errorMessage += f"INSTR_STACK: {funcMem[1]}\n"
            errorMessage += f"VALUE_STACK: {funcMem[2]}\n"
        super().__init__(errorMessage)