import sys

# To remove traceback from error

class LuppoloInterpException(Exception):
    '''
    The exception class for the interpreter. It is used to raise errors during the interpretation of the program.
    '''

    verboseLog = True
    stackTrace = False
    defaultErrorMessage = "An error occurred during the interpretation of the program. Read logs for more info.\n"

    if not stackTrace:
        sys.tracebacklimit=0
    
    def __init__(self, funcMem=None):
        '''
        Initializes the exception passing the function memory at the time of the error.
        If verboseLog is set to True, the function memory will be printed in the error message.
        '''
        errorMessage = LuppoloInterpException.defaultErrorMessage
        if LuppoloInterpException.verboseLog and funcMem is not None:
            errorMessage += "Function memory at the time of the error:\n"
            errorMessage += f"ID_MEM: {funcMem[0]}\n"
            errorMessage += f"INSTR_STACK: {funcMem[1]}\n"
            errorMessage += f"VALUE_STACK: {funcMem[2]}\n"
        super().__init__(errorMessage)