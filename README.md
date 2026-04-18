# Mandelbrot Viewer (Python + Tkinter)

Visualizzatore interattivo dell'insieme di Mandelbrot scritto in Python, senza dipendenze esterne.

## Requisiti

- Python 3.10+ (consigliato)
- Tkinter (di solito gia' incluso con Python)

## Avvio

Dalla cartella del progetto:

```bash
python3 mandelbrot.py
```

## Funzionalita'

- Rendering dell'insieme di Mandelbrot in finestra grafica.
- Controllo dinamico di:
  - risoluzione (`Larghezza`, `Altezza`)
  - iterazioni massime
  - finestra del piano complesso (`Re`/`Im` min e max)
- Esportazione dell'immagine in formato **PNG**.
- Scelta tra diverse palette di colori: **Classic**, **Grayscale**, **Fire**, **Emerald**.
- Due modalita' di rendering:
  - `Anteprima`: piu' veloce (riduce risoluzione e iterazioni)
  - `Genera HQ`: rendering finale ad alta qualita'
- Ottimizzazioni:
  - test rapido cardioide/bulbo
  - simmetria sull'asse reale (quando applicabile)
  - multiprocesso parallelizzato per il calcolo delle righe in HQ

## Controlli mouse

- `Click sinistro + trascina`: disegna un rettangolo per selezionare l'area di zoom.
- `Rotella`: zoom in/out centrato sul centro della vista.

Dopo interazioni mouse, l'app mostra prima un'anteprima veloce e poi programma automaticamente un render HQ.

## Parametri consigliati

- Esplorazione rapida:
  - `Fattore preview`: 3-6
  - `Iterazioni`: 100-300
- Render di dettaglio:
  - `Fattore preview`: 2
  - `Iterazioni`: 800+
  - `Usa multiprocesso (HQ)`: attivo

## Risoluzione problemi

- Se la finestra non si apre, verifica che Tkinter sia installato.
- Se il render e' lento:
  - aumenta `Fattore preview` per la navigazione
  - riduci temporaneamente le iterazioni
  - abilita multiprocesso e imposta un numero adeguato di worker
