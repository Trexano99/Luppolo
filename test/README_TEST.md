# LUPPOLO TEST
In questo progetto sono stati forniti dei test di base che permettono di verificare il corretto funzionamento del linguaggio. <br>
I test non devono essere intesi come esaustivi e non seguono nessun tipo di specifica formale quale unit test o integration test o analoghi, ma sono stati creati per verificare il corretto funzionamento del linguaggio durante lo sviluppo.<br><br>
Sono state create molteplici cartelle con dentro i corrispettivi test (spiegati di seguito) e sono stati divisi in due categorie: `valid` e `invalid`. <br>
I test `valid` sono test che dovrebbero essere accettati dal linguaggio, mentre i test `invalid` sono test che dovrebbero essere rifiutati.<br>

**NOTA**: Alcuni test sono subordinati alla correttezza di altri costrutti sintattici, altrimenti sarebbero rifiutati a prescindere dalla grammatica.<br>
Es: In grammar _Id è subordinato alla correttezza di function(vedi [emptyFunc](grammar/valid/function/emptyFunc.lp)), poichè il funzionamento è stato testato nella dichiarazione di funzione._

### GRAMMAR
All'interno della folder [grammar](grammar) sono presenti alcune batterie di test per la grammatica del linguaggio. <br>
Sono stati testati tutti i costrutti sintattici del linguaggio e per ognuno di essi sono stati sono stati creati dei test che permettono di provare le varie configurazioni che devono essere rispettate.

### INTERPRETER
All'interno di [interpreter](interpreter) sono presenti dei test che permettono di verificare il corretto funzionamento dell'interprete. <br>

## HOW TO
TODO: Come eseguire i test