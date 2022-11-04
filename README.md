# WhereIsPartyBackend
Backend per un progetto che si basa sulla realizzazione di una piattaforma per la prenotazione nei locali per le serate chiamata WhereIsParty. Attualmente la piattaforma mette a disposizioni solo alcune funzionalità, come quella di login, registrazione e possibilità di prenotarsi e vedere la propria prenotazione.

## Dev details
Il backend è composta da una REST API python realizzata tramite FASTApi, insieme a sqlalchemy per la modellazzione del database relazionele il quale è appossiggiato su Postgresql. Viene inoltre utilizzata la libreria boto3 per interfacciarsi con tutte le tecnologie AWS utilizzate (ess. S3).
