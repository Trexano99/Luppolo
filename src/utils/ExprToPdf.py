import os
import subprocess

from graphviz import Digraph
from antlr4.tree.Trees import Trees

from src.expression.BaseLuppExpr import BaseLuppExpr
from src.utils.LuppoloLogger import LuppoloLogger


def generateLatex(
        expr : BaseLuppExpr, 
        resultDir = './output',
        resultFileName = 'result',
        includeThreeGraph = True,
        includeLatex = True,
        includeRaw = True):
    '''
    This method generates the LaTeX representation of the expression.
    The method takes the following parameters:
    - expr: the expression to represent.
    - resultDir: the directory where the output will be saved.
    - resultFileName: the name of the output file.
    - includeThreeGraph: a boolean value indicating if the pdf should include the graph representation of the expression.
    - includeLatex: a boolean value indicating if the pdf should include the LaTeX representation of the expression.
    - includeRaw: a boolean value indicating if the pdf should include the raw representation of the expression.
    Return the path of the generated LaTeX file.
    '''
    LuppoloLogger.logInfo("Generating expression LaTeX representation")
    pathGen = __generateLatex(expr, resultDir, resultFileName, includeThreeGraph, includeLatex, includeRaw)
    LuppoloLogger.logInfo(f"LaTeX representation generated in {pathGen}")
    return pathGen

def generatePdf(
        expr : BaseLuppExpr, 
        resultDir = './output',
        resultFileName = 'result',
        includeThreeGraph = True,
        includeLatex = True,
        includeRaw = True):
    '''
    This method generates the PDF representation of the expression.
    The method takes the following parameters:
    - expr: the expression to represent.
    - resultDir: the directory where the output will be saved.
    - resultFileName: the name of the output file.
    - includeThreeGraph: a boolean value indicating if the pdf should include the graph representation of the expression.
    - includeLatex: a boolean value indicating if the pdf should include the LaTeX representation of the expression.
    - includeRaw: a boolean value indicating if the pdf should include the raw representation of the expression.
    Return the path of the generated PDF file.
    '''
    
    LuppoloLogger.logInfo("Generating expression PDF representation")
    # Genero il file latex da aggiungere al PDF
    __generateLatex(expr, resultDir, resultFileName, includeThreeGraph, includeLatex, includeRaw)

    # Cancello il vecchio file pdf se esiste e nel caso lo rimuovo
    if os.path.exists(f'{resultDir}/{resultFileName}.pdf'):
        try:
            LuppoloLogger.logDebug("Removing old PDF file")
            os.remove(f'{resultDir}/{resultFileName}.pdf')
        except OSError as e:
            LuppoloLogger.logError(f"Error removing old PDF file: {resultDir}/{resultFileName}.pdf. Error: {e}")
            raise e

    # Creo il pdf da latex
    LuppoloLogger.logDebug("Generating PDF from LaTeX using pdflatex")
    subprocess.run(['pdflatex', '-halt-on-error', '-interaction=nonstopmode', '-aux-directory', f'{resultDir}/temp/', '-output-directory', resultDir, f'{resultDir}/{resultFileName}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Rimuovo il file latex generato
    LuppoloLogger.logDebug("Removing LaTeX file used for creating the PDF")
    os.remove(f'{resultDir}/{resultFileName}.tex')
    pathFileGenerated = f"{resultDir}/{resultFileName}.pdf"
    LuppoloLogger.logInfo(f"PDF representation generated in {pathFileGenerated}")

    return pathFileGenerated
    


def __generateLatex(
        expr : BaseLuppExpr,
        resultDir = './output',
        resultFileName = 'result',
        includeLogo = True,
        includeThreeGraph = True,
        includeLatex = True,
        includeRaw = True):
    
    resultLtx = r"""
        \documentclass{article}
        \usepackage{graphicx}
        \usepackage{amsmath}
        \usepackage{geometry}
        \usepackage{fancyvrb}
        
        \geometry{a4paper, margin=1in}

        \begin{document}
        """
    
    if includeLogo:
        resultLtx += r"""
        \begin{center}
        \includegraphics[width=0.2\textwidth]{./imgs/LuppoloIcon.jpg}
        \end{center}
        """

    if includeLatex:
        exprLatex = expr.getLatexRapresentation()
        resultLtx += r"""
        \section*{LaTeX Representation}
        \vspace{-2em}
        \begin{center}
        \LARGE
        \begin{equation*}
        %s
        \end{equation*}
        \end{center}
        \vspace{1em}
        """ % exprLatex

    if includeThreeGraph:
        d = Digraph()
        expr.getGraphRapresentation(d)
        d.render('./output/temp/graph', format = "pdf", view=False)

        resultLtx += r"""
        \section*{Graph Representation}
        \vspace{-2em}
        \begin{center}
        \includegraphics{./output/temp/graph.pdf}
        \end{center}
        """
    
    if includeRaw:
        exprRaw = Trees.toStringTree(expr).strip()
        resultLtx +=  r"""
        \section*{Raw Representation}
        \vspace{1em}
        \begin{center}
        \Large
        \texttt{%s} 
        \end{center}
        """ % exprRaw

    resultLtx += r"""
        \end{document}
    """

    LuppoloLogger.logDebug("Creating the LaTeX file")
    with open(f'{resultDir}/{resultFileName}.tex', 'w') as f:
        f.write(resultLtx)

    return f'{resultDir}/{resultFileName}.tex'