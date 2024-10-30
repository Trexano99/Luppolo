# LUPPOLO
TODO: Introduzione al progetto


## GUIDA ALL'UTILIZZO
Prima di iniziare ad utilizzare LUPPOLO è necessario compilare la grammatica, che non viene fornita precompilata.
### Compilazione della grammatica
La compilazione della grammatica può essere effettuata o manualmente o automaticamente. La sua compilazione permette la generazione all'interno della cartella bin del `Lexer`, del `Parser`, del `Listener` e del `Visitor`, sui quali è basato il resto del funzionamento del progetto. 
#### Compilazione automatica
Per la compilazione automatica viene messa a disposizione la classe AntlrGrammarCompiler, che permette di compilare la grammatica in modo automatico.<br>
Per avviare la compilazione basta eseguire il metodo `compileGrammar()` della classe `AntlrGrammarCompiler`. Vedere la documentazione del metodo per ulteriori informazioni sui parametri.<br>
#### Compilazione manuale
Per la compilazione manuale è necessario utilizzare il jar di antlr4, che può essere scaricato dal sito ufficiale di antlr4. Una volta scaricato il jar, è possibile compilare la grammatica con il comando `java -jar [YOUR ANTLR_JAR] -Dlanguage=Python3 -visitor -o bin/ grammar\syntax\luppolo.g`.



## TEST
Per approfondire la parte di test fare riferimento al file [README_TEST.md](test/README_TEST.md)