# UI background tasks: `ui_task` / `background` cookbook

How to write a tab operation that runs work off the UI thread, without reading
the framework source (`Orbitool/UI/manager/task.py`). It covers the thread
model, the three `mode` words, the error/abort contracts, and the "never touch
widgets from a worker" rule. Import `ui_task`/`background`/`progress` from
`.manager` (or `..manager` in a subpackage). A task is an ordinary method — call
it (`self.denoise()`) or `connect` it to a signal; there is no `.func` ceremony.

## Thread model

A task alternates between **main-thread segments** and **worker segments**:

```
main thread   | segment 1: read inputs / touch widgets |
              |   await background(work, "msg") ──────────────────────────┐
              |                              ...suspended...             │
worker thread |                              |---- run work ----|         │
              |   ◀── resume: result or exception thrown at this await ───┘
              | segment 2: update widgets |
              |   await background(work2, "msg2") ─────────────────────────┐
              |                              |---- run work2 ---|          │
              |   ◀── resume: result or exception ─────────────────────────┘
              | segment 3: update widgets; task returns, busy count released |
```

- Everything **outside** `await background(...)` runs on the **main thread**:
  the slot call, code before the first `await`, every resume after an `await`,
  and `try/except/finally`.
- The callable (or worker instance) handed to `background(...)` runs on a
  **worker thread**; its `msg` is shown as the progress message.
- The value of the `await` expression is the worker's return value — any
  value, including falsy ones (`0`, `""`, `None`, `()`). A worker exception is
  thrown **at the await point**, so ordinary `try/except/finally` applies on
  the main thread with the worker's original traceback.
- Only `background(...)` is a worker boundary, but you may also `await` a
  plain `async def` helper that itself awaits only `background(...)` (its
  yielded step bubbles up to the driver). Any other suspendable is rejected
  at the await point by a runtime check (the driver only accepts a background
  step) and goes through the standard error fallback: `asyncio.sleep`, or a
  `@ui_task` method (a task is not awaitable — call it, or relay through
  `join`). This is not asyncio and there is no event loop of your own.
- The framework keeps every started worker alive until Qt reports it
  finished. A step that starts the next worker from its result therefore
  never tears down a thread that is still running.

In the test suite and in `--debug`'s synchronous mode
(`setting.debug.thread_block_gui`) workers run inline for determinism; the
alternation order is identical.

## Modes: default / `join` / `light`

`mode` accepts exactly three words. There are **no letter aliases** — an
unknown word (including the old single letters) raises `ValueError` at
decoration time.

| mode | busy | while busy | uncaught error fallback |
|---|---|---|---|
| *(default, omit the argument)* | holds a busy count (start +1, finish −1) | **refuses to start**: shows "Wait for process", takes no count | log with traceback → dialog → release its count → chain stops |
| `join` | holds a busy count (+1/−1, only ever returns what it took) | **starts anyway** (pipeline relay) | same as default |
| `light` | never touches busy: no check, no count, no busy signal, no start sleep | n/a (it never asks) | log with traceback → dialog only (nothing to release) |

Counting rules (default and `join` only): each task increments a busy count on
start and decrements it on finish — success or failure — so busy clears only
when the **last** holder finishes, regardless of finish order, and no task can
clear someone else's busy. The count is the single source of truth
(`busy == count > 0`); `manager.set_busy(True/False)` simulates a running
operation by taking/returning one hold on the same counter, so call it in pairs.

How to choose:

- long user-triggered work (denoise, calibrate, fit) → **default**;
- a handler that must start while another task still holds busy — finish/relay
  handlers, chained tab steps → **`join`**;
- tiny main-thread work (selection change, drag & drop, preview refresh) →
  **`light`**; also use `light` when you only want the framework's error dialog
  without any busy involvement;
- when unsure → default.

`light` tasks may still `await background(...)`; they simply do not advertise
that work through busy.

## Recipes

```python
# one or several steps: read inputs on the main thread, compute in the worker,
# update widgets after the await
@ui_task
async def denoise(self):
    folder = self.folderEdit.text()                                    # main thread
    files = await background(lambda: scan_folder(folder), "scanning")  # worker
    self.statusLabel.setText(f"{len(files)} files")                    # main thread
    results = await background(lambda: analyze(files), "analyzing")    # worker
    self.resultLabel.setText(f"done: {len(results)}")                  # main thread
```

`background(work, msg="processing")` accepts a callable **or** an already
constructed `Thread`/`MultiProcess` instance; anything else raises `TypeError`.
The step's `msg` is shown by the framework via `manager.msg`. Inside a worker,
report progress through the module-level `progress.tqdm(...)` accessor:

```python
def work():
    for peak in progress.tqdm(peaks, msg="calc formulas"):
        peak.formulas = calc_formulas(peak)
```

`progress.tqdm(...)` resolves to the running worker's reporter (installed by the
driver), so the worker needs no reference to `Manager`; it only emits a signal,
so it is safe off the main thread. With no worker context (main-thread code) it
is a harmless no-op — it never raises. The `manager.tqdm(...)` object still
exists as the resident implementation the accessor resolves to.

### Multi-process worker instance

For read → process (pooled) → write workloads, subclass `MultiProcess` and
hand the constructed instance straight to `background`:

```python
class Analyze(MultiProcess):
    @staticmethod
    def func(data):
        return analyze_one(data)             # runs in the process pool, per item

    @staticmethod
    def read(file, **kwargs):
        yield from file["inputs"]            # iterate inputs (worker thread)

    @staticmethod
    def read_len(file, **kwargs):
        return len(file["inputs"])           # total for the progress bar

    @staticmethod
    def write(file, rets, **kwargs):
        file["results"] = list(rets)         # consume results (worker thread)
        return len(file["results"])

    @staticmethod
    def exception(file, **kwargs):
        file.pop("results", None)            # rollback hook, runs once on abort

@ui_task
async def analyze(self):
    file = {"inputs": load_inputs()}
    count = await background(Analyze(file), "analyzing")
    self.resultLabel.setText(f"{count} rows")
```

The framework reports the subclass's `read`/`write` progress automatically; the
step `msg` is the progress message. `progress.tqdm(...)` is only meaningful on
the worker thread — a subclass's `func` runs in the process pool, so per-item
progress there stays with the framework's automatic `read`/`write` reporting.

### `join`: pipeline relay

A relay handler fires while the task that triggered it still holds busy:

```python
class PipelineTab(QtCore.QObject):  # Signal must live on a QObject subclass
    stepFinished = QtCore.Signal()

    @ui_task
    async def run(self):                     # default: holds busy for the whole run
        await background(step_one, "step one")
        self.stepFinished.emit()             # relay while this task still holds busy
        await background(step_two, "step two")

    @ui_task(mode="join")
    async def on_step_finished(self):        # starts despite busy, holds its own count
        self.logLabel.setText("step one done")
```

A *default* task fired during busy would be refused with "Wait for process";
`join` starts anyway and releases only its own count, so busy stays until both
tasks finish.

### `light`: main-thread micro work

```python
@ui_task(mode="light")
async def refresh_preview(self):         # milliseconds: must not disable the UI
    item = self.listWidget.currentItem()
    self.previewLabel.setText(item.text() if item else "")
```

No busy check, no busy signal, no progress bar (a `light` task that runs a
`tqdm`-driven worker still shows that bar until the next busy→idle transition,
which `light` itself never produces) — but uncaught errors still get the
standard log + dialog.

### Slot arguments: forwarded by signature

The decorated coroutine's own signature decides what the slot receives:

```python
class Emitter(QtCore.QObject):
    fired = QtCore.Signal(int, str)

class Tab:
    def __init__(self):
        super().__init__()
        self.emitter = Emitter()
        self.emitter.fired.connect(self.on_fired)

    @ui_task(mode="light")
    async def on_fired(self, number):        # declares one parameter
        ...

tab = Tab()
tab.emitter.fired.emit(7, "extra")           # → number=7; "extra" is truncated
```

- **Signal has more parameters than the slot declares** → the excess positionals
  are truncated. `*args` (without a `self`) keeps the host plus every signal
  argument; `**kwargs` absorbs undeclared keywords (others are dropped, logged
  at debug level).
- A **required** parameter that cannot be filled raises a clear `TypeError`
  (`cannot forward call arguments ...`) through the standard error fallback.
- Bindings are cached with weak references: closing a window makes it
  collectable; calling through a stale binding raises `ReferenceError`. The
  binding identity is stable while the host lives (a host that cannot be
  weak-referenced gets an uncached binding).

## Error handling

Handle errors inside the task with ordinary `try/except/finally` — it runs at
the await point, on the main thread:

```python
@ui_task
async def read_files(self):
    try:
        count = await background(load_files, "read files")  # worker error arrives here
    except OSError as e:             # caught on the main thread
        self.statusLabel.setText(f"read failed: {e}")
    else:
        self.statusLabel.setText(f"{count} files")
    finally:                         # always runs, on the main thread
        self.progressLabel.setText("")
```

Anything you do not catch goes through the framework's uniform fallback, in
order: **log with the original traceback** (`logger.error(str(e), exc_info=e)`
on the `Orbitool` logger) → **one dialog** (`showInfo(str(e))`) → **busy release
per mode** (default/`join` return their count, `light` releases nothing) →
**the chain terminates**. Argument-binding failures and `background(42)`-style
payload errors enter the same fallback.

## Abort semantics

- `MultiProcess.abort()` sets the aborted flag **first**, then requests
  completion — and **the first terminal notification wins**: whichever of abort
  and natural completion notifies first is kept, the other suppressed. The
  completion notification fires **exactly once**, so the driver never completes
  a task twice.
- If abort takes effect **while the worker is running**, the worker's
  `exception(file)` rollback hook runs **exactly once** via `run()`'s `finally`
  (guarded by `_rolled_back`) — in real multiprocessing mode and in the
  `NO_MULTIPROCESS` debug mode alike. An abort arriving after natural
  completion does not roll back. Subclasses must override `exception()`.
- The abort surfaces as a worker exception (`RuntimeError("Aborted")`) on the
  normal result channel, so it reaches your await point / the standard error
  fallback like any other worker error.
- **Only `MultiProcess` workers are abortable**: the Abort button
  (`MainUiPy.abort_process`) acts only when `manager.running_thread` is a
  `MultiProcess`; plain closures / `Thread` steps ignore it (button policy is
  tracked separately in the spec).

## Rules: never touch widgets from a worker

Qt widgets (and the widget tree under `self.ui.*`) are main-thread-only —
reading or writing them from a worker is undefined behavior. Capture plain
values before the `await`, touch widgets only in the main-thread segments:

```python
# ✗ wrong: the closure runs on a worker thread and calls into widgets
await background(lambda: self.table.setRowCount(3), "updating")
# ✗ also wrong: reading widget state inside the closure is a cross-thread read
rows = await background(lambda: self.table.rowCount(), "counting")

# ✓ correct: read inputs on the main thread, compute in the worker, update after
folder = self.folderEdit.text()            # main thread: read widget state
rows = await background(lambda: count_rows(folder), "counting")  # pure computation
self.table.setRowCount(rows)               # main thread: touch widgets
```

Inside a worker, `progress.tqdm(...)` progress reporting is fine (it only emits
a signal); anything that draws, reads, or mutates widgets is not.

## One task style

All UI tasks use `ui_task` / `background`; there is no second mechanism. The
driver advances the task coroutine over one send/throw protocol, and busy is a
single count, so `busy_signal` fires only on a change.

## Examples are test-backed

Every example/claim above has an executable twin in
`Orbitool/UI/manager/tests/` (`test_cookbook_*` in `test_ui_task.py` plus the
`test_busy_modes.py` behaviours); the default `uv run --group dev pytest` run
keeps doc and tests in step.
