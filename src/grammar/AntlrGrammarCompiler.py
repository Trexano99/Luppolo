


import subprocess

from src.utils.LuppoloLogger import LuppoloLogger
class AntlrGrammarCompiler:

    @staticmethod
    def compileGrammar(
            syntaxFilePath = 'src\\grammar\\syntax\\luppolo.g',
            targetDir = '../bin',
            antlrJarPath = '%ANTLR4_JAR%'):
        '''
        This method compiles the grammar file using the ANTLR4 tool.
        The method takes the following parameters:
        - syntaxFilePath: the path of the grammar file to compile. Default value is 'grammar\\syntax\\luppolo.g'.
        - targetDir: the directory where the compiled grammar (binary) will be saved. Default value is '../bin'.
        - antlrJarPath: the path of the ANTLR4 jar file. Default value is '%ANTLR4_JAR%'.
        The method returns True if the grammar is compiled successfully, False otherwise.
        '''
        
        command = f'java -jar "{antlrJarPath}" -Dlanguage=Python3 -visitor -o {targetDir} {syntaxFilePath}'
        
        LuppoloLogger.logInfo(f'Compiling Luppolo grammar.')
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            LuppoloLogger.logError(f'Error compiling grammar: {e}')
            return False
        LuppoloLogger.logInfo(f'Grammar compiled successfully in dir: {targetDir}.')
        return True