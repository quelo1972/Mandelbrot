#!/usr/bin/python3
"""Visualizzatore interattivo dell'insieme di Mandelbrot con Tkinter.

Caratteristiche principali:
- anteprima veloce e render HQ
- ottimizzazioni matematiche (cardioide/bulbo + simmetria)
- navigazione con mouse (click, drag, zoom)
"""

import os
import time
import tkinter as tk
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from tkinter import ttk


DEFAULTS = {
    "width": 900,
    "height": 600,
    "max_iter": 120,
    "re_min": -2.5,
    "re_max": 1.0,
    "im_min": -1.2,
    "im_max": 1.2,
}


def mandelbrot(c_re: float, c_im: float, max_iter: int) -> int:
    """Restituisce il numero di iterazioni prima della divergenza."""
    # Test rapido: cardioide principale e bulbo di periodo 2.
    # Questi punti sono sicuramente interni all'insieme.
    c_im2 = c_im * c_im
    x = c_re - 0.25
    q = x * x + c_im2
    if q * (q + x) <= 0.25 * c_im2:
        return max_iter
    if (c_re + 1.0) * (c_re + 1.0) + c_im2 <= 0.0625:
        return max_iter

    z_re, z_im = 0.0, 0.0
    for i in range(max_iter):
        z_re2 = z_re * z_re - z_im * z_im + c_re
        z_im2 = 2.0 * z_re * z_im + c_im
        z_re, z_im = z_re2, z_im2
        if z_re * z_re + z_im * z_im > 4.0:
            return i
    return max_iter


def color_from_iter(it: int, max_iter: int) -> str:
    """Mappa il numero di iterazioni in un colore RGB esadecimale."""
    if it == max_iter:
        return "#000000"
    t = it / max_iter
    r = int(9 * (1 - t) * t * t * t * 255)
    g = int(15 * (1 - t) * (1 - t) * t * t * 255)
    b = int(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255)
    return f"#{r:02x}{g:02x}{b:02x}"


def compute_row_data(
    y: int,
    width: int,
    height: int,
    max_iter: int,
    re_min: float,
    re_max: float,
    im_min: float,
    im_max: float,
) -> tuple[int, str]:
    """Calcola una singola riga (y) dell'immagine e la restituisce pronta per PhotoImage.put."""
    x_div = max(width - 1, 1)
    y_div = max(height - 1, 1)
    c_im = im_max - (y / y_div) * (im_max - im_min)

    row = []
    for x in range(width):
        c_re = re_min + (x / x_div) * (re_max - re_min)
        it = mandelbrot(c_re, c_im, max_iter)
        row.append(color_from_iter(it, max_iter))

    return y, "{" + " ".join(row) + "}"


class MandelbrotApp:
    """Gestisce UI, navigazione e pipeline di rendering."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Insieme di Mandelbrot")
        self.root.geometry("1240x780")

        cpu = os.cpu_count() or 2

        self.status_var = tk.StringVar(value="Pronto")
        self.max_iter_var = tk.IntVar(value=DEFAULTS["max_iter"])
        self.width_var = tk.StringVar(value=str(DEFAULTS["width"]))
        self.height_var = tk.StringVar(value=str(DEFAULTS["height"]))
        self.re_min_var = tk.StringVar(value=str(DEFAULTS["re_min"]))
        self.re_max_var = tk.StringVar(value=str(DEFAULTS["re_max"]))
        self.im_min_var = tk.StringVar(value=str(DEFAULTS["im_min"]))
        self.im_max_var = tk.StringVar(value=str(DEFAULTS["im_max"]))
        self.preview_scale_var = tk.IntVar(value=2)
        self.use_mp_var = tk.BooleanVar(value=True)
        self.workers_var = tk.StringVar(value=str(max(1, cpu - 1)))

        container = ttk.Frame(root, padding=8)
        container.pack(fill=tk.BOTH, expand=True)

        controls = ttk.LabelFrame(container, text="Parametri")
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        canvas_frame = ttk.Frame(container)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=DEFAULTS["width"],
            height=DEFAULTS["height"],
            highlightthickness=0,
            bg="black",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        ttk.Label(controls, text="Iterazioni massime").pack(anchor="w", pady=(8, 0), padx=8)
        iter_scale = ttk.Scale(
            controls,
            from_=20,
            to=2500,
            orient=tk.HORIZONTAL,
            variable=self.max_iter_var,
        )
        iter_scale.pack(fill=tk.X, padx=8)
        ttk.Label(controls, textvariable=self.max_iter_var).pack(anchor="e", padx=8)

        self._add_entry(controls, "Larghezza", self.width_var)
        self._add_entry(controls, "Altezza", self.height_var)
        self._add_entry(controls, "Re minimo", self.re_min_var)
        self._add_entry(controls, "Re massimo", self.re_max_var)
        self._add_entry(controls, "Im minimo", self.im_min_var)
        self._add_entry(controls, "Im massimo", self.im_max_var)

        sep = ttk.Separator(controls, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, padx=8, pady=6)

        ttk.Label(controls, text="Fattore preview").pack(anchor="w", padx=8)
        preview_scale = ttk.Scale(controls, from_=2, to=8, orient=tk.HORIZONTAL, variable=self.preview_scale_var)
        preview_scale.pack(fill=tk.X, padx=8)
        ttk.Label(controls, text="2=piu' veloce, 8=molto veloce").pack(anchor="w", padx=8)

        ttk.Checkbutton(controls, text="Usa multiprocesso (HQ)", variable=self.use_mp_var).pack(
            anchor="w", padx=8, pady=(8, 2)
        )
        self._add_entry(controls, "Worker", self.workers_var)

        buttons = ttk.Frame(controls)
        buttons.pack(fill=tk.X, pady=8, padx=8)
        ttk.Button(buttons, text="Anteprima", command=lambda: self.render(preview=True)).pack(fill=tk.X, pady=2)
        ttk.Button(buttons, text="Genera HQ", command=lambda: self.render(preview=False)).pack(fill=tk.X, pady=2)
        ttk.Button(buttons, text="Reset", command=self.reset_defaults).pack(fill=tk.X, pady=2)

        ttk.Label(
            controls,
            text=(
                "Workflow consigliato:\n"
                "1) Anteprima per trovare l'area\n"
                "2) Genera HQ per il dettaglio finale\n\n"
                "Mouse:\n"
                "- Click sx: ricentra\n"
                "- Click sx + trascina: sposta vista\n"
                "- Rotella: zoom sul centro"
            ),
            justify=tk.LEFT,
        ).pack(anchor="w", padx=8, pady=(8, 10))

        ttk.Label(root, textvariable=self.status_var, anchor="w").pack(fill=tk.X, padx=10, pady=(0, 6))

        self.image: tk.PhotoImage | None = None
        # ID del timer che scatena un render HQ ritardato dopo interazioni rapide.
        self.hq_after_id: str | None = None
        # Stato del drag: punto iniziale in pixel e finestra complessa iniziale.
        self.drag_start_xy: tuple[int, int] | None = None
        self.drag_start_view: tuple[float, float, float, float] | None = None
        self.drag_moved = False
        self.last_drag_preview_ts = 0.0

        self.canvas.bind("<ButtonPress-1>", self.on_left_press)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)

        self.render(preview=True)

    def _add_entry(self, parent: ttk.LabelFrame, label: str, variable: tk.StringVar) -> None:
        """Aggiunge una riga label + entry nel pannello parametri."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=8, pady=2)
        ttk.Label(frame, text=label, width=13).pack(side=tk.LEFT)
        ttk.Entry(frame, textvariable=variable, width=12).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _read_params(self) -> tuple[int, int, int, float, float, float, float, int, int]:
        """Legge e valida i parametri UI per il rendering."""
        width = int(self.width_var.get())
        height = int(self.height_var.get())
        max_iter = int(self.max_iter_var.get())
        re_min = float(self.re_min_var.get())
        re_max = float(self.re_max_var.get())
        im_min = float(self.im_min_var.get())
        im_max = float(self.im_max_var.get())
        preview_scale = int(self.preview_scale_var.get())
        workers = int(self.workers_var.get())

        if width < 100 or height < 100:
            raise ValueError("Larghezza e altezza devono essere almeno 100.")
        if max_iter < 1:
            raise ValueError("Le iterazioni devono essere almeno 1.")
        if re_min >= re_max:
            raise ValueError("Serve Re minimo < Re massimo.")
        if im_min >= im_max:
            raise ValueError("Serve Im minimo < Im massimo.")
        if preview_scale < 2:
            raise ValueError("Il fattore preview deve essere >= 2.")
        if workers < 1:
            raise ValueError("Il numero di worker deve essere >= 1.")

        return width, height, max_iter, re_min, re_max, im_min, im_max, preview_scale, workers

    def _read_view_window(self) -> tuple[float, float, float, float]:
        """Legge e valida solo la finestra complessa corrente."""
        re_min = float(self.re_min_var.get())
        re_max = float(self.re_max_var.get())
        im_min = float(self.im_min_var.get())
        im_max = float(self.im_max_var.get())
        if re_min >= re_max or im_min >= im_max:
            raise ValueError("Finestra complessa non valida.")
        return re_min, re_max, im_min, im_max

    def _set_view_window(self, re_min: float, re_max: float, im_min: float, im_max: float) -> None:
        """Aggiorna i campi UI della finestra complessa."""
        self.re_min_var.set(f"{re_min:.15g}")
        self.re_max_var.set(f"{re_max:.15g}")
        self.im_min_var.set(f"{im_min:.15g}")
        self.im_max_var.set(f"{im_max:.15g}")

    def _pixel_to_complex(
        self, px: int, py: int, re_min: float, re_max: float, im_min: float, im_max: float
    ) -> tuple[float, float]:
        """Converte coordinate canvas (pixel) in coordinate del piano complesso."""
        width = max(self.canvas.winfo_width(), 2)
        height = max(self.canvas.winfo_height(), 2)
        nx = min(max(px, 0), width - 1) / (width - 1)
        ny = min(max(py, 0), height - 1) / (height - 1)
        c_re = re_min + nx * (re_max - re_min)
        c_im = im_max - ny * (im_max - im_min)
        return c_re, c_im

    def _schedule_hq_render(self) -> None:
        """Programma un render HQ ritardato, cancellando eventuali timer precedenti."""
        if self.hq_after_id is not None:
            self.root.after_cancel(self.hq_after_id)
        self.hq_after_id = self.root.after(350, self._run_scheduled_hq)

    def _run_scheduled_hq(self) -> None:
        """Callback timer: lancia effettivamente il render HQ."""
        self.hq_after_id = None
        self.render(preview=False)

    def on_left_press(self, event: tk.Event) -> None:
        """Inizio interazione tasto sinistro: prepara stato drag."""
        try:
            self.drag_start_view = self._read_view_window()
        except ValueError:
            self.status_var.set("Errore: parametri complessi non validi.")
            return

        self.drag_start_xy = (event.x, event.y)
        self.drag_moved = False
        self.last_drag_preview_ts = 0.0
        if self.hq_after_id is not None:
            self.root.after_cancel(self.hq_after_id)
            self.hq_after_id = None

    def on_left_drag(self, event: tk.Event) -> None:
        """Pan della finestra complessa durante il trascinamento."""
        if self.drag_start_xy is None or self.drag_start_view is None:
            return

        start_x, start_y = self.drag_start_xy
        dx = event.x - start_x
        dy = event.y - start_y
        if abs(dx) < 2 and abs(dy) < 2:
            return

        self.drag_moved = True
        re_min0, re_max0, im_min0, im_max0 = self.drag_start_view
        width = max(self.canvas.winfo_width(), 2)
        height = max(self.canvas.winfo_height(), 2)
        re_span = re_max0 - re_min0
        im_span = im_max0 - im_min0

        shift_re = -(dx / (width - 1)) * re_span
        shift_im = (dy / (height - 1)) * im_span
        self._set_view_window(
            re_min0 + shift_re,
            re_max0 + shift_re,
            im_min0 + shift_im,
            im_max0 + shift_im,
        )

        # Throttle sull'anteprima per mantenere il drag fluido.
        now = time.perf_counter()
        if now - self.last_drag_preview_ts >= 0.05:
            self.render(preview=True)
            self.last_drag_preview_ts = now

    def on_left_release(self, event: tk.Event) -> None:
        """Fine click/drag: click ricentra, drag conferma pan e pianifica HQ."""
        if self.drag_start_view is None:
            return

        if not self.drag_moved:
            re_min, re_max, im_min, im_max = self.drag_start_view
            c_re, c_im = self._pixel_to_complex(event.x, event.y, re_min, re_max, im_min, im_max)
            re_span = re_max - re_min
            im_span = im_max - im_min
            self._set_view_window(
                c_re - re_span / 2.0,
                c_re + re_span / 2.0,
                c_im - im_span / 2.0,
                c_im + im_span / 2.0,
            )
            self.render(preview=True)
        else:
            self.render(preview=True)

        self.drag_start_xy = None
        self.drag_start_view = None
        self.drag_moved = False
        self._schedule_hq_render()

    def on_mouse_wheel(self, event: tk.Event) -> None:
        """Zoom in/out centrato sul centro della vista corrente."""
        try:
            re_min, re_max, im_min, im_max = self._read_view_window()
        except ValueError:
            self.status_var.set("Errore: parametri complessi non validi.")
            return

        zoom_in = False
        if hasattr(event, "delta") and event.delta != 0:
            zoom_in = event.delta > 0
        elif hasattr(event, "num"):
            zoom_in = event.num == 4

        factor = 0.8 if zoom_in else 1.25
        c_re = (re_min + re_max) / 2.0
        c_im = (im_min + im_max) / 2.0
        self._set_view_window(
            c_re - (c_re - re_min) * factor,
            c_re + (re_max - c_re) * factor,
            c_im - (c_im - im_min) * factor,
            c_im + (im_max - c_im) * factor,
        )
        self.render(preview=True)
        self._schedule_hq_render()

    def reset_defaults(self) -> None:
        """Ripristina tutti i parametri di default e rigenera anteprima."""
        cpu = os.cpu_count() or 2
        self.width_var.set(str(DEFAULTS["width"]))
        self.height_var.set(str(DEFAULTS["height"]))
        self.max_iter_var.set(DEFAULTS["max_iter"])
        self.re_min_var.set(str(DEFAULTS["re_min"]))
        self.re_max_var.set(str(DEFAULTS["re_max"]))
        self.im_min_var.set(str(DEFAULTS["im_min"]))
        self.im_max_var.set(str(DEFAULTS["im_max"]))
        self.preview_scale_var.set(2)
        self.use_mp_var.set(True)
        self.workers_var.set(str(max(1, cpu - 1)))
        self.render(preview=True)

    def _render_rows(
        self,
        image: tk.PhotoImage,
        y_values: list[int],
        width: int,
        height: int,
        max_iter: int,
        re_min: float,
        re_max: float,
        im_min: float,
        im_max: float,
        use_symmetry: bool,
        use_mp: bool,
        workers: int,
    ) -> None:
        """Renderizza righe su PhotoImage in single-process o multiprocesso."""
        total = len(y_values)

        if use_mp and workers > 1:
            with ProcessPoolExecutor(max_workers=workers) as executor:
                rows_iter = executor.map(
                    compute_row_data,
                    y_values,
                    repeat(width),
                    repeat(height),
                    repeat(max_iter),
                    repeat(re_min),
                    repeat(re_max),
                    repeat(im_min),
                    repeat(im_max),
                    chunksize=8,
                )
                for idx, (y, row_data) in enumerate(rows_iter, 1):
                    image.put(row_data, to=(0, y))
                    if use_symmetry:
                        mirror_y = height - 1 - y
                        if mirror_y != y:
                            image.put(row_data, to=(0, mirror_y))
                    if idx % 10 == 0:
                        pct = int((idx / total) * 100)
                        self.status_var.set(f"Generazione in corso... {pct}%")
                        self.root.update_idletasks()
        else:
            for idx, y in enumerate(y_values, 1):
                _, row_data = compute_row_data(
                    y,
                    width,
                    height,
                    max_iter,
                    re_min,
                    re_max,
                    im_min,
                    im_max,
                )
                image.put(row_data, to=(0, y))
                if use_symmetry:
                    mirror_y = height - 1 - y
                    if mirror_y != y:
                        image.put(row_data, to=(0, mirror_y))
                if idx % 20 == 0:
                    pct = int((idx / total) * 100)
                    self.status_var.set(f"Generazione in corso... {pct}%")
                    self.root.update_idletasks()

    def render(self, preview: bool) -> None:
        """Pipeline completa di rendering (anteprima o HQ)."""
        try:
            width, height, max_iter, re_min, re_max, im_min, im_max, preview_scale, workers = self._read_params()
        except ValueError as exc:
            self.status_var.set(f"Errore: {exc}")
            return

        mode = "HQ"
        use_mp = self.use_mp_var.get()
        if preview:
            # In anteprima riduciamo risoluzione/iterazioni per feedback rapido.
            width = max(100, width // preview_scale)
            height = max(100, height // preview_scale)
            max_iter = max(20, max_iter // preview_scale)
            mode = f"Anteprima x{preview_scale}"
            use_mp = False

        self.status_var.set(f"Generazione in corso... ({mode})")
        self.root.update_idletasks()

        self.canvas.config(width=width, height=height)
        image = tk.PhotoImage(width=width, height=height)
        self.canvas.delete("all")
        self.canvas.create_image((0, 0), image=image, state="normal", anchor=tk.NW)

        start = time.perf_counter()

        # Se la finestra è simmetrica sull'asse reale calcoliamo solo metà righe.
        symmetry_eps = (im_max - im_min) * 1e-12 + 1e-15
        use_symmetry = abs(im_max + im_min) <= symmetry_eps
        y_values = list(range((height + 1) // 2)) if use_symmetry else list(range(height))

        self._render_rows(
            image,
            y_values,
            width,
            height,
            max_iter,
            re_min,
            re_max,
            im_min,
            im_max,
            use_symmetry,
            use_mp,
            workers,
        )

        elapsed = (time.perf_counter() - start) * 1000.0
        self.image = image
        self.canvas.image = image

        opt = "cardioide/bulbo"
        if use_symmetry:
            opt += ", simmetria"
        if use_mp and workers > 1:
            opt += f", multiprocesso={workers}"

        self.status_var.set(
            f"Pronto ({mode}) - {width}x{height}, iter={max_iter}, "
            f"tempo={elapsed:.0f} ms, ottimizzazioni: {opt}"
        )


def main() -> None:
    root = tk.Tk()
    MandelbrotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
