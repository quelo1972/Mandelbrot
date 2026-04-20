# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

## [1.3.0] - 2026-04-20
### Aggiunto
- Nuove palette gradienti: **Ocean**, **Sunset**, **Ice**, **Aurora**, **Viridis**, **Neon**.
- Pulsante **Palette casuale** per cambiare rapidamente combinazione colori.

### Cambiato
- Click sinistro e drag mantengono la modalità corrente:
  - in **Anteprima** restano in Anteprima
  - in **HQ** restano in HQ
- Il cambio palette non forza più il passaggio `Anteprima -> HQ`, ma applica il colore direttamente alla modalità attiva.

### Corretto
- Ripulito il file `CHANGELOG.md` da marker di conflitto di merge lasciati accidentalmente.

## [1.2.0] - 2024-05-22
### Aggiunto
- Supporto per l'**Insieme di Julia**.
- Selettore dinamico nel pannello parametri per passare tra Mandelbrot e Julia.
- Gestione automatica della centratura e dei limiti della vista al cambio di frattale.
- Finestra completamente ridimensionabile.
- Adattamento automatico della finestra alle dimensioni `Larghezza`/`Altezza` impostate.

### Cambiato
- Disabilitato il rendering HQ automatico dopo le interazioni mouse: l'app ora rimane in anteprima finché non viene richiesto manualmente il rendering HQ.

### Ottimizzato
- Ottimizzazione del loop di calcolo (riduzione moltiplicazioni ridondanti).

## [1.1.0] - 2024-05-21
### Aggiunto
- Funzionalita' di salvataggio dell'immagine in formato **PNG**.
- Sistema di navigazione tramite **rettangolo di selezione** (click e trascina) per uno zoom preciso.
- Nuova palette **Emerald** ad alto contrasto.
- Gestione dinamica dell'aspect ratio per evitare distorsioni durante lo zoom.

### Corretto
- Risolto bug nel mapping delle coordinate mouse (ora calcolato sulle dimensioni reali dell'immagine).
- Corretti errori di indentazione nella gestione delle palette.
- Risolto crash `KeyError` all'avvio relativo ai parametri di default.

### Cambiato
- La navigazione "Pan" (trascinamento immagine) è stata sostituita dalla selezione ad area per una migliore esperienza utente.
