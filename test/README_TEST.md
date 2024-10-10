# LUPPOLO TEST

## GRAMMAR
All'interno della folder `grammar` sono presenti alcune batterie di test per la grammatica del linguaggio. <br>
I testi sono stati suddivisi tra `correct`, in cui sono presenti test che dovrebbero essere accettati dalla grammatica, e `erroneus`, in cui sono presenti test che dovrebbero essere rifiutati dalla grammatica.<br>
<br>
**NOTA**: Alcuni test sono subordinati alla correttezza di altri costrutti sintattici, altrimenti sarebbero rifiutati a prescindere dalla grammatica.<br>
Es: _Id è subordinato alla correttezza di function(vedi [emptyFunc](grammar\valid\function\emptyFunc.lp)), poichè il funzionamento è stato testato nella dichiarazione di funzione._