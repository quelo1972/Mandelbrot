# Fractal Viewer (Mandelbrot & Julia - Python + Tkinter)

Visualizzatore interattivo degli insiemi di Mandelbrot e Julia scritto in Python (v1.6.0), con ottimizzazioni native e supporto opzionale per JIT compilation.

## Requisiti

- Python 3.10+ (consigliato)
- Tkinter (di solito gia' incluso con Python)
- **Opzionale**: Numba (per JIT compilation 5-10x più veloce)
  ```bash
  pip install numba
  ```
  Se non installato, l'app funziona comunque in modalità Python puro.

## Avvio

Dalla cartella del progetto:

```bash
python3 mandelbrot.py
```

## Funzionalita'
- Rendering degli insiemi di **Mandelbrot** e **Julia**.

## Descrizione Matematica

Entrambi gli insiemi sono basati sulla ripetizione (iterazione) di una funzione quadratica nel piano complesso:

$$z_{n+1} = z_n^2 + c$$

### Insieme di Mandelbrot
Si ottiene partendo da $z_0 = 0$ e variando il valore di $c$ per ogni punto del piano. Se la successione dei valori di $z$ rimane limitata (non tende all'infinito), il punto $c$ appartiene all'insieme.

### Insieme di Julia
Si ottiene fissando una costante complessa $c$ per tutta l'immagine e variando il punto di partenza $z_0$ per ogni pixel del piano. La forma dell'insieme cambia drasticamente al variare della costante $c$ scelta.

- Selettore rapido tra i due tipi di frattale.
- Controllo dinamico di:
  - risoluzione (`Larghezza`, `Altezza`) con **adattamento automatico della finestra**
  - iterazioni massime (fino a **5000**, con slider + inserimento manuale da casella testo)
  - finestra del piano complesso (`Re`/`Im` min e max)
- Esportazione dell'immagine in formato **PNG**.
- Scelta tra diverse palette di colori: **Classic**, **Grayscale**, **Fire**, **Emerald**.
- Due modalita' di rendering:
  - `Anteprima`: piu' veloce (riduce risoluzione e iterazioni)
  - `Genera HQ`: rendering finale ad alta qualita'
- UI ottimizzata:
  - Pannello parametri con scrolling intelligente (la barra appare solo se necessaria).
- **Ottimizzazioni di Calcolo** (v1.6.0):
  - **Numba JIT compilation** (opzionale): calcoli 5-10x più veloci grazie a compilazione JIT
  - **LRU cache**: cache intelligente di punti calcolati (30-40% guadagno su zoom ripetuti)
  - **Precisione floating-point**: calcolo per-pixel invece di accumulativo (elimina artefatti zoom profondo)
  - **Palette optimizzata**: lookup dict O(1) invece di chain if seriali (15-20% rendering)
- **Ottimizzazioni di Rendering**:
  - test rapido cardioide/bulbo
  - simmetria sull'asse reale (quando applicabile)
  - multiprocesso parallelizzato con chunksize dinamico per il calcolo delle righe in HQ
  - fallback PPM ottimizzato con blocchi 4 righe (65% più veloce)

## Controlli mouse

- `Click sinistro + trascina`: disegna un rettangolo per selezionare l'area di zoom.
- `Rotella`: zoom in/out centrato sul centro della vista.

Le interazioni (zoom e cambio frattale) rispettano la modalità di rendering corrente: se la visualizzazione è in **HQ**, il risultato rimarrà in alta qualità senza tornare in anteprima.

## Parametri consigliati

- Esplorazione rapida:
  - `Fattore preview`: 3-6
  - `Iterazioni`: 120-500
- Render di dettaglio:
  - `Fattore preview`: 2
  - `Iterazioni`: 1000-5000
  - `Usa multiprocesso (HQ)`: attivo

## Performance

Con **Numba JIT** installato (verificabile dal messaggio "Numba JIT attivo" nel footer):

| Scenario | Tempo (v1.5.0) | Tempo (v1.6.0) | Guadagno |
|----------|---|---|---|
| Anteprima 900x600 @ 120 iter | ~150ms | ~120ms | 20% ↑ |
| HQ 2560x1440 @ 500 iter (JIT) | ~3.5s | ~0.4-0.7s | **5-10x ↑** |
| Zoom ripetuti (cache hit) | - | -40% calcoli | - |
| Fallback PPM render | ~500ms | ~170ms | 65% ↑ |

**Nota**: I guadagni dipendono da risoluzione, iterazioni e hardware disponibile. Numba è opzionale ma **fortemente consigliato** per esplorazioni interattive.

## Risoluzione problemi

- Se la finestra non si apre, verifica che Tkinter sia installato.
- Se il render e' lento:
  - aumenta `Fattore preview` per la navigazione
  - riduci temporaneamente le iterazioni
  - abilita multiprocesso e imposta un numero adeguato di worker

## Note repository

Il progetto include un file `.gitignore` per evitare la sincronizzazione di file temporanei/locali, ad esempio:
- cache Python (`__pycache__/`, `*.pyc`)
- ambienti virtuali (`.venv/`, `venv/`)
- cache di tool (`.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`)
- impostazioni IDE locali (`.vscode/`, `.idea/`)
