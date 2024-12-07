# LUPPOLO
Luppolo è un linguaggio di programmazione in grado di manipolare espressioni algebriche creato come progetto per il corso di Linguaggi e Traddutori dell'Università degli Studi di Milano. La traccia completa dello stesso può essere trovata al seguente [link](https://github.com/let-unimi/progetti/blob/master/05-Luppolo/Testo.md).<br>

<p align="center">
  <img src="./imgs/LuppoloIcon.jpg"/>
</p>


## STRUTTURA DEL PROGETTO
Tutti i file sorgente possono essere trovati all'interno della cartella `src`. <br>
Essi sono suddivisi rispettivamente in `ast`, che contiene la definizione degli alberi sintattici astratti, `grammar`, che contiene la grammatica del linguaggio, `interpreter`, che contiene l'interprete del linguaggio e `utils`, che contiene una serie di classi di utilità.<br>
Oltre a `src` è anche presente la cartella `test`, che contiene i test del progetto. <br>

### AST
L'ast rappresenta l'albero astratto del linguaggio, ovvero una semplificazione dell'albero sintattico originale generato dal parser in fase di parsing del codice. <br>
La generazione dell'AST avviene attraverso la classe [AstGenerator](src/ast/AstGenerator.py) che utilizzando un visitor, visita l'albero sintattico generato dal parser e produce per ogni nodo le corrispettive astrazioni che possono essere trovate all'interno della directory [elements](src/ast/elements).

### EXPRESSION
Le espressioni sono le unità fondamentali del linguaggio, e sono rappresentate all'interno della cartella [expression](src/ast/elements/expression). <br>
Sono utilizzate per la rappresentazione di espressioni algebriche e possono essere suddivise in [nodes](src/expression/nodes.py), che rappresentano gli operatori di somma, prodotto e potenza, e [leaf](src/expression/leaf.py), che sono i numeri razionali e i simboli.

### GRAMMAR
Contiene la definizione della [grammatica](src/grammar/LuppoloGrammar.py) del linguaggio Luppolo. <br>
E' presente inoltre la classe [AntlrGrammarCompiler](src/grammar/AntlrGrammarCompiler.py) che permette di compilare la grammatica in modo automatico. Vedi nella Guida all'utilizzo per ulteriori informazioni.

### INTERPRETER
Contiente l'[interprete](src/interpreter/interpreter.py) del linguaggio, che permette di eseguire il codice scritto in Luppolo. <br>
L'interprete è un interprete iterativo che permette di interpretare funzioni e per ognuna di esse possiede una memoria delle variabili, uno stack delle istruzioni e uno stack dei valori computati.

### UTILS
Contiente alcuni elementi utilizzati durante lo sviluppo del progetto, come la classe [LuppoloLogger](src/utils/LuppoloLogger.py) che permette di loggare messaggi in maniera strutturata, e le classi [GenericTreeNode](src/utils/GenericTreeNode.py), che rappresenta un generico nodo con i relativi figli per strutturare una gerarchia di nodi, e [GraphTreeNode](src/utils/GraphTreeNode.py), che permette la rappresentazione grafica di un nodo.

## APPROFONDIMENTO

### RAPPRESENTAZIONE
TODO: Esplicare con esempi grafici tutte le possibili rappresentazioni dei nodi.


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