# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

## [1.5.0] - 2026-04-21
### Aggiunto
- **Relazione Mandelbrot-Julia**: Nuova sezione "Analisi Julia" nella sidebar.
- **Esplorazione Dinamica**: Aggiunta opzione per generare l'insieme di Julia cliccando direttamente sui punti dell'insieme di Mandelbrot.
- **Sincronizzazione C**: Funzione per copiare le coordinate centrali della vista nei parametri $c$ di Julia.

## [1.4.1] - 2026-04-21
### Cambiato
- **Coerenza Rendering**: Lo zoom (rotella) e il cambio di tipo di frattale ora rispettano la modalità di rendering corrente. 
- Se l'utente è in modalità **HQ**, le operazioni di zoom e switch mantengono l'alta qualità senza forzare il passaggio dall'anteprima.

## [1.4.0] - 2026-04-21
### Aggiunto
- **Finestra Adattiva**: La finestra principale ora si ridimensiona dinamicamente in base alle dimensioni dell'immagine generata (Preview e HQ).
- **Sidebar Intelligente**: La barra di scorrimento laterale appare solo se i controlli eccedono l'altezza della finestra; lo scroll del mouse è inibito quando non necessario.
- Esteso il limite massimo di iterazioni a **5000** per esplorazioni più profonde.
- Documentazione interna del codice migliorata con commenti tecnici.

## [1.3.2] - 2026-04-20
### Aggiunto
- Sezione `Note repository` nel README con indicazioni sui file non sincronizzati.

### Cambiato
- Introdotto `.gitignore` per escludere artefatti locali/temporanei dal versionamento.
- Rimosso il bytecode Python in `__pycache__/` dai file tracciati dal repository.

## [1.3.1] - 2026-04-20
### Aggiunto
- Campo di input manuale per `Iterazioni massime`, in aggiunta allo slider.

### Cambiato
- `Reset Globale` ora rispetta la modalità attiva: in **Anteprima** resta in Anteprima, in **HQ** resta in HQ.

## [1.2.0] - 2026-04-20
### Aggiunto
- Supporto per l'**Insieme di Julia**.
- Selettore dinamico nel pannello parametri per passare tra Mandelbrot e Julia.
- Gestione automatica della centratura e dei limiti della vista al cambio di frattale.
- Ottimizzazione del loop di calcolo (riduzione moltiplicazioni ridondanti).
- Finestra ora completamente ridimensionabile.
### Cambiato
- Disabilitato il rendering HQ automatico dopo le interazioni mouse: l'app ora rimane in anteprima finché non viene richiesto manualmente il rendering HQ.

## [1.1.0] - 2024-05-21
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