# UI background tasks: `ui_task` / `background` cookbook

How to write a tab operation that runs work off the UI thread, without reading
the framework source (`Orbitool/UI/manager/task.py`,
`Orbitool/UI/manager/state_node.py`). It covers the thread model, the three
`mode` words, recipes, the error/abort contracts, the "never touch widgets
from a worker" rule, and the migration table for the legacy `@state_node`
style. Every task-shaped example here is executable-checked — see
[Example → test map](#example--test-map).

Imports used below (pick the one matching your module's depth):

```python
# Orbitool/UI/*.py            →  from .manager import ui_task, background
# Orbitool/UI/<package>/*.py  →  from ..manager import ui_task, background
# or explicitly               →  from Orbitool.UI.manager import ui_task, background
```

A task is an ordinary method: call it (`self.denoise()`) or connect it to a
signal (`button.clicked.connect(self.denoise)`). There is no `.func` ceremony
in application code.

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
  thrown **at the await point**, so ordinary `try/except/finally` applies, on
  the main thread.
- Only `await background(...)` may be awaited. This is not asyncio and there
  is no event loop of your own.

Why it is shaped this way: Qt widgets may only be touched from the main
thread, while heavy work must leave it — so the boundary has to be
unmistakable. The legacy `@state_node` style encoded the same alternation as
a *convention* (code before `yield` = main thread); `await background(...)`
makes it *syntax*, which is also what `except`/`finally` hang on: worker
errors surface with their original traceback at a normal Python error
handling site instead of being smuggled across threads.

(In the test suite and in `--debug`'s synchronous thread mode
`setting.debug.thread_block_gui`, workers run inline for determinism; the
alternation order is identical.)

## Modes: default / `join` / `light`

`mode` accepts exactly three words. There are **no letter aliases** —
`ui_task(mode="w")` (or `"x"`/`"a"`/`"e"`/`"n"`) raises `ValueError` at
decoration time. An unknown word does the same.

| mode | busy | while busy | uncaught error fallback |
|---|---|---|---|
| *(default, omit the argument)* | holds a busy count (start +1, finish −1) | **refuses to start**: shows "Wait for process", takes no count | log with traceback → dialog → release its count → chain stops |
| `join` | holds a busy count (+1/−1, only ever returns what it took) | **starts anyway** (pipeline relay) | same as default |
| `light` | never touches busy: no check, no count, no busy signal, no start sleep | n/a (it never asks) | log with traceback → dialog only (nothing to release) |

Counting rules (default and `join` only): busy is *legacy flag* **or**
*count > 0*, so old and new tasks share one busy state safely. Each task
increments on start and decrements on finish — success or failure — so busy
clears only when the **last** holder finishes, regardless of finish order,
and no task can clear someone else's busy. `light` skips all of this; it is
for millisecond-scale work that must not disable the UI or flash the
progress bar.

How to choose:

- long user-triggered work (denoise, calibrate, fit) → **default**;
- a handler that must start while another task still holds busy — finish/relay
  handlers, chained tab steps → **`join`**;
- tiny main-thread work (selection change, drag & drop, preview refresh) →
  **`light`**; also use `light` when you only want the framework's error
  dialog without any busy involvement;
- when unsure → default.

`light` tasks may still `await background(...)`; they simply do not advertise
that work through busy.

## Recipes

### Single step

```python
class DenoiseTab:
    @ui_task
    async def denoise(self):
        folder = self.folderEdit.text()                       # main thread: read inputs
        noise = await background(lambda: compute_noise(folder), "denoising")  # worker
        self.noiseLabel.setText(f"{noise:.3f}")               # main thread: touch widgets
```

`background(work, msg="processing")` accepts a callable **or** an already
constructed `Thread`/`MultiProcess` instance; anything else raises
`TypeError`. The step's `msg` string is shown by the framework via
`manager.msg`; inside a longer worker you can also drive
`manager.tqdm(...)` yourself to report progress (it only emits a signal, so
it is safe off the main thread).

### Multi-step pipeline

Main-thread segments and worker segments simply alternate; widget updates
belong in the segments, computation in the workers:

```python
class PipelineTab:
    @ui_task
    async def run_pipeline(self):
        folder = self.folderEdit.text()                       # main segment
        files = await background(lambda: scan_folder(folder), "scanning")   # worker 1
        self.statusLabel.setText(f"{len(files)} files")        # main segment
        preview = summarize(files)          # fast bookkeeping stays on the main thread
        self.previewTable.setRowCount(len(preview))  # main segment
        for row, entry in enumerate(preview):
            self.previewTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(entry)))
        results = await background(lambda: analyze(files), "analyzing")     # worker 2
        self.resultLabel.setText(f"done: {len(results)}")      # main segment
```

### Multi-process worker instance

For read → process (pooled) → write workloads, subclass `MultiProcess` and
hand the constructed instance straight to `background`:

```python
from .manager import MultiProcess, ui_task, background

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

class AnalyzeTab:
    @ui_task
    async def analyze(self):
        file = {"inputs": load_inputs()}
        count = await background(Analyze(file), "analyzing")
        self.resultLabel.setText(f"{count} rows")
```

Progress for the subclass's `read`/`write` stages is reported automatically
by the framework (the driver hands the worker its progress reporter); the
step `msg` shows up as the progress message.

### `join`: pipeline relay

A relay handler fires while the task that triggered it still holds busy:

```python
class PipelineTab(QtCore.QObject):  # pyqtSignal must live on a QObject subclass
    stepFinished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stepFinished.connect(self.on_step_finished)

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
`join` starts anyway and releases only its own count, so busy stays until
both tasks finish.

### `light`: main-thread micro work

```python
class SpectraListTab:
    def __init__(self):
        super().__init__()
        self.listWidget.currentItemChanged.connect(self.refresh_preview)

    @ui_task(mode="light")
    async def refresh_preview(self):         # milliseconds: must not disable the UI
        item = self.listWidget.currentItem()
        self.previewLabel.setText(item.text() if item else "")
```

No busy check, no busy signal, no progress bar (this example runs no worker;
if a `light` task does run a `tqdm`-driven worker, its progress bar still
appears and stays until the next busy→idle transition — `light` itself never
produces that edge) — but uncaught errors still get the standard log +
dialog.

### Slot arguments: forwarded by signature (no `withArgs`)

The decorated coroutine's own signature decides what the slot receives:

```python
class Emitter(QtCore.QObject):
    fired = QtCore.pyqtSignal(int, str)

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
  are truncated (`(int, str)` signal into a 1-parameter slot works).
- Declaring `*args` (without a `self`) keeps the host plus every signal
  argument; `**kwargs` absorbs undeclared keywords (other undeclared keywords
  are dropped, logged at debug level).
- A **required** parameter that cannot be filled does not fail silently: the
  binding raises a clear `TypeError` (`cannot forward call arguments ...`)
  that goes through the standard error fallback (log + dialog + busy release).
- `withArgs` does not exist on `ui_task` — passing it raises `TypeError`.
- Bindings are cached with weak references: closing a window makes it
  collectable; calling through a stale binding raises `ReferenceError`
  instead of failing silently. `signal.connect(w.task)` keeps a stable
  identity while the host lives (for normal hosts; a host that cannot be
  weak-referenced falls back to an uncached binding).

## Error handling

Handle errors inside the task with ordinary `try/except/finally` — it runs at
the await point, on the main thread:

```python
class FilesTab:
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

Anything you do not catch goes through the framework's uniform fallback,
in order:

1. **log with the original traceback** — `logger.error(str(e), exc_info=e)` on
   the `Orbitool` logger, so the log shows the worker's frames, not the
   resume frame;
2. **one dialog** — `showInfo(str(e))`, the single format used by the new
   path (a failing dialog is itself caught and logged; the task's state
   still unwinds correctly);
3. **busy release per mode** — default/`join` return their count, `light`
   releases nothing;
4. **the chain terminates** — no further task code runs (code in your
   `finally` has already run during unwinding).

Argument-binding failures (missing required parameter, conflicting
positional/keyword) and `background(42)`-style payload errors enter the same
fallback. There is no `except_node` in the new API.

## Abort semantics

- `MultiProcess.abort()` sets the aborted flag **first**, then requests
  completion — and **the first terminal notification wins**: whichever of
  abort and natural completion notifies first is kept, the other is
  suppressed. The completion notification fires **exactly once**, so the
  driver never completes a task twice.
- If abort takes effect **while the worker is running**, the worker's
  `exception(file)` rollback hook runs **exactly once** via `run()`'s
  `finally` (guarded by `_rolled_back`) — both in real multiprocessing mode
  and in the `NO_MULTIPROCESS` debug single-process mode. An abort arriving
  after natural completion does not roll back. Subclasses must override
  `exception()`: the base implementation raises `NotImplementedError`, which
  `run()`'s `finally` catches and logs.
- The abort surfaces as a worker exception (`RuntimeError("Aborted")`) on the
  normal result channel, so it reaches your await point / the standard error
  fallback like any other worker error.
- **Currently only `MultiProcess` workers are abortable**: the Abort button
  (`MainUiPy.abort_process`) acts only when `manager.running_thread` is a
  `MultiProcess`. Steps written as plain closures / `Thread` ignore it —
  button availability policy is tracked separately in the spec
  ("Further Notes").

## Rules: never touch widgets from a worker

The callable you pass to `background(...)` runs on a worker thread. Qt
widgets (and the widget tree under `self.ui.*`) are main-thread-only —
reading or writing them from a worker is undefined behavior (random crashes,
corrupted state). Capture plain values before the `await`, touch widgets
only in the main-thread segments:

```python
# ✗ wrong: the closure runs on a worker thread and calls into widgets
@ui_task
async def bad(self):
    await background(lambda: self.table.setRowCount(3), "updating")

# also ✗: reading widget state inside the closure is a cross-thread read
@ui_task
async def bad_too(self):
    rows = await background(lambda: self.table.rowCount(), "counting")

# ✓ correct: read inputs on the main thread, compute in the worker, update after
@ui_task
async def good(self):
    folder = self.folderEdit.text()            # main thread: read widget state
    rows = await background(lambda: count_rows(folder), "counting")  # pure computation
    self.table.setRowCount(rows)               # main thread: touch widgets
```

Inside a worker, `self.manager.tqdm(...)` progress reporting is fine (it only
emits a signal); anything that draws, reads, or mutates widgets is not.

## Migration table: `@state_node` → `@ui_task`

This is the table the per-file migration tickets follow (spec phase 2).
Migrate file by file; after each file run the manager tests
(`uv run --group dev pytest Orbitool/UI/manager/tests`) and smoke-test the
tab.

Regression tests a migration ticket adds are part of the default run and
live next to the migrated code: co-locate inside the migrated package when
that package is the whole batch (`Orbitool/UI/file_tab/test_file_tab_migration.py`),
otherwise pick one representative subpackage for the batch and add it to
`pytest.ini` `testpaths` (e.g. `Orbitool/UI/formulas/`). Do not drop them in
`Orbitool/UI/tests/` — that folder is the real-GUI/RAW suite excluded from
the default run.

| Old (`@state_node`) | New (`@ui_task`) |
|---|---|
| `@state_node` (default, `mode='w'`) | `@ui_task` |
| `@state_node(mode='x')` | `@ui_task(mode="join")` |
| `@state_node(mode='e')` or `@state_node(mode='n')` | `@ui_task(mode="light")` |
| `@state_node(mode='a')` | `@ui_task(mode="light")` — the counting rule takes over busy release |
| `withArgs=True` | delete — arguments are forwarded by signature |
| `def` + `yield closure, "msg"` | `async def` + `await background(closure, "msg")` |
| `yield worker_instance, "msg"` | `await background(worker_instance, "msg")` |
| `xxx.except_node(handler)` | delete — rewrite the handler as `try/except` or `finally` in the task body |
| `@state_node` method with **no** `yield` (a plain main-thread update, e.g. the `mode='e'`/`'n'`/`'a'` one-liners) | `@ui_task` + `async def` (no `await` inside) |

Notes:

- `yield closure` with no message → `await background(closure)` (default
  message `"processing"`); `ret = yield closure, "msg"` →
  `ret = await background(closure, "msg")`.
- A method with no `yield` still becomes `async def`: the task is handed to
  the shared send/throw driver, which requires a coroutine (or a legacy
  generator). A plain `def` under `@ui_task` fails at call time
  (`TypeError: task must be a generator or coroutine`), so a missed `async`
  is loud rather than silent.
- Residue check after migrating a file: `grep -E
  'state_node|except_node|withArgs'` must be empty. A leftover `\byield\b`
  is *not* a miss by itself — `@contextlib.contextmanager` helpers and
  nested helper generators (e.g. a local `iter_select()`) legitimately keep
  `yield`; only a `yield` left inside a former task body is an unmigrated
  task (and it would also fail the coroutine requirement above).
- Both `except_node` registration styles disappear: the decorator form on a
  same-named method (`@addThermoFile.except_node`) and the explicit call form
  (`addFormula.except_node(handler)`).
- Error-handler guidance: cleanup on success *and* failure → `finally`;
  recovery that suppresses the error (no framework dialog, task completes
  normally) → `except Exception:` without re-raising; cleanup while still
  wanting the framework dialog → `finally` (it runs during unwinding, just
  before the fallback).
- `mode='a'` sites (Formula panel) become `light`; this also fixes the old
  defect where an error during a busy period cleared *someone else's* busy —
  each task now only returns the count it took.
- No letter aliases: `mode='w'` etc. raise `ValueError` at decoration time,
  so a missed mapping fails loudly instead of silently misbehaving.

Before/after in full:

```python
# before — legacy style
@state_node(mode='x', withArgs=True)
def showResult(self, index):
    def func():
        return heavy(index)
    result = yield func, "computing"
    self.resultLabel.setText(result)

@showResult.except_node
def showResult(self):
    self.resultLabel.setText("failed")

# after — new style
@ui_task(mode="join")
async def showResult(self, index):
    try:
        result = await background(lambda: heavy(index), "computing")
    except Exception:                       # caught at the await point, main thread
        self.resultLabel.setText("failed")  # your recovery runs before the dialog
        raise                               # framework: log + dialog + release busy
    else:
        self.resultLabel.setText(result)    # resumed on the main thread
```

## Old and new styles coexist

- Both styles run in the **same driver** (`Driver` in
  `Orbitool/UI/manager/task.py`): it advances legacy generators (`yield`
  payload style) and coroutines (`await background(...)` style) through one
  send/throw protocol, so coexistence costs no second engine.
- The legacy `@state_node` code path — letters, `withArgs`, `except_node`,
  strong-reference binding cache, direct busy flag — is untouched and keeps
  its exact behavior while call sites migrate file by file.
- Shared busy is safe in both directions: busy = legacy flag **or** new
  count > 0, and `busy_signal` fires only when that effective state changes,
  so old and new tasks nesting or overlapping cannot release each other's
  busy early (pinned by the mixed-nesting tests).
- New or rewritten code uses `ui_task` only. Once all legacy call sites are
  gone (phase 3), the old mechanism — generator driver path, five letter
  modes, `except_node`, strong-reference binding cache — is deleted
  wholesale.

## Example → test map

Each example/claim above has executable twins in
`Orbitool/UI/manager/tests/` (default run: `uv run --group dev pytest`).
The `test_cookbook_*` twins are the doc's executable shadow — they overlap
deliberately with the broader behavior tests (e.g. `test_cookbook_slot_arguments`
↔ `test_signal_connect_truncates_and_disconnects_by_identity`); both columns
below are part of the contract:

| Doc example / claim | Test |
|---|---|
| Thread model: worker off main, resume + `finally` on main | `test_ui_task.py::test_finally_runs_on_main_thread_with_real_worker_thread` |
| Single step, busy edges, progress msg | `test_ui_task.py::test_cookbook_single_step` |
| Multi-step pipeline, segment order + thread identities | `test_ui_task.py::test_cookbook_multi_step_pipeline` |
| Falsy results arrive at the await point | `test_ui_task.py::test_falsy_worker_result_reaches_after_await` |
| `MultiProcess` instance passed to `background` | `test_ui_task.py::test_cookbook_multiprocess_instance` |
| Three payload forms (closure / closure+msg / worker) | `test_ui_task.py::test_background_accepts_three_payload_forms` |
| Non-callable payload rejected with a clear error | `test_ui_task.py::test_background_rejects_non_callable_payload` |
| `join` relay starts while busy, returns only its count | `test_ui_task.py::test_cookbook_join_relay` |
| default refuses while busy / `join` starts while busy | `test_busy_modes.py::test_default_refused_when_count_holds_busy`, `test_busy_modes.py::test_join_returns_only_the_count_it_took` |
| `light` never touches busy / busy signal | `test_ui_task.py::test_cookbook_light_slot` |
| Counting: nested tasks, out-of-order finishes | `test_busy_modes.py::test_nested_inner_finishes_first_busy_held_until_outer_finishes`, `test_busy_modes.py::test_nested_outer_finishes_first_busy_held_until_inner_finishes` |
| Old/new nesting shares busy correctly | `test_busy_modes.py::test_old_task_and_new_join_hold_busy_until_both_finish`, `test_new_default_refused_while_old_task_running`, `test_old_default_refused_while_new_task_running`, `test_light_during_old_task_leaves_busy_signal_untouched`, `test_join_error_keeps_busy_held_by_old_task` |
| Slot arguments: truncation / keywords / no `withArgs` | `test_ui_task.py::test_cookbook_slot_arguments`, `test_ui_task.py::test_slot_arguments_forwarded_by_signature`, `test_ui_task.py::test_new_api_rejects_with_args_switch` |
| Unbindable arguments → clear error through the fallback | `test_ui_task.py::test_unbindable_arguments_raise_clear_error_and_reset_busy` |
| `try/except/else/finally` at the await point, on main | `test_ui_task.py::test_cookbook_try_except_finally` |
| Uncaught → log with traceback → dialog → busy reset → chain stops | `test_ui_task.py::test_uncaught_worker_exception_logged_shown_and_busy_reset` |
| Recovery runs before the dialog (`except` + `raise`), count released | `test_ui_task.py::test_recover_before_dialog_then_release_count` |
| Letter modes rejected at decoration | `test_busy_modes.py::test_letter_mode_aliases_rejected_at_decoration` |
| Migrated form (`join` + forwarded args + `await background`) | `test_ui_task.py::test_cookbook_migrated_form` |
| Abort: flag first, exactly-once notification, rollback once | `test_multiprocess.py::test_abort_sets_flag_before_notifying`, `test_completion_then_abort_notifies_once`, `test_abort_then_completion_notifies_once`, `test_abort`, `test_abort_multiprocess_rollback` |
| Progress label unique across busy transitions | `test_progress_label.py::test_progress_label_stays_unique_across_busy_transitions` |
| Weak-reference binding, stale binding raises | `test_ui_task.py::test_ui_task_binding_cache_releases_host` |
