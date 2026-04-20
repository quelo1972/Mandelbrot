# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

## [1.2.0] - 2024-05-22

### Aggiunto
- Finestra ora completamente ridimensionabile.
- La finestra si adatta automaticamente alle dimensioni di Larghezza/Altezza impostate nei parametri.

### Cambiato
- Disabilitato il rendering HQ automatico dopo le interazioni mouse: l'app ora rimane in anteprima finché non viene richiesto manualmente il rendering HQ.

### Aggiunto
- Funzionalità di salvataggio dell'immagine in formato **PNG**.
- Sistema di navigazione tramite **rettangolo di selezione** (click e trascina) per uno zoom preciso.
- Nuova palette **Emerald** ad alto contrasto.
- Gestione dinamica dell'aspect ratio per evitare distorsioni durante lo zoom.

### Corretto
- Risolto bug nel mapping delle coordinate mouse (ora calcolato sulle dimensioni reali dell'immagine).
- Corretti errori di indentazione nella gestione delle palette.
- Risolto crash `KeyError` all'avvio relativo ai parametri di default.

### Cambiato
- La navigazione "Pan" (trascinamento immagine) è stata sostituita dalla selezione ad area per una migliore esperienza utente.