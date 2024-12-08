

class LuppoloInterpException(Exception):

    verboseLog = True
    defaultErrorMessage = "An error occurred during the interpretation of the program. Read logs for more info.\n"
    
    def __init__(self,funcMem):
        errorMessage = LuppoloInterpException.defaultErrorMessage
        if LuppoloInterpException.verboseLog:
            errorMessage += "Function memory at the time of the error:\n"
            errorMessage += f"ID_MEM: {funcMem[0]}\n"
            errorMessage += f"INSTR_STACK: {funcMem[1]}\n"
            errorMessage += f"VALUE_STACK: {funcMem[2]}\n"
        super().__init__(errorMessage)

    def __init__(self):
        super().__init__(LuppoloInterpException.defaultErrorMessage)