# Logging

Where records go, what a record says, and when to emit one. **Format** and
**when** are two separate rules.

## Where records go

`Orbitool/logger.py` builds the `Orbitool` logger: a `TimedRotatingFileHandler`
writing `log.txt` next to the executable (`paths.py`, `LOG_PATH`, midnight
rotation) plus a stdout handler. Emit through the `logger` wrapper —
`logger.i(TAG, content)` (and `d` / `w` / `error` / `exception` / `critical`) —
which prepends `[TAG] `. Tests never write this `log.txt` (`conftest.py`; see
[development.md](development.md)).

## Format

One shape for every record, user action or internal step alike:

```
[TAG] func_name() key=value ...
```

`TAG` is the emitting file's stem or the owning class. `content` is the function
name plus the key values at that point — the parameters that matter or the
result. Don't dump long data; log a count. Exceptions keep their traceback
(`logger.error(msg, exc_info=e)`).

## When

Emit a record on an obvious active user operation, or at a key moment in the
work. No central hook and no helper — call `logger.i` at the handler.

This convention is documented rather than asserted; there is no test for it.
