# Changelog

All notable changes to Orbitool are documented in this file. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [2.6.0]

### Changed

- Documentation is now kept in the repository: the user manual lives under
  `docs/guide/` and developer/build docs under `docs/dev/`. The external Notion
  links have been removed.

### Fixed

- Averaging no longer kills the denoise read when a `.RAW` contains a scan whose FT
  profile is empty (a damaged or interrupted acquisition). The .NET averager throws
  `IndexOutOfRangeException` on such a scan without naming it, so the unusable scans
  are now detected on the first failure and left out of that window, which is averaged
  again instead of aborting the whole file. A read reports the scans it had to repair
  to whoever started it, so every denoise, skip or show-average read lists the files it
  found damaged in one dialog (as well as in `log.txt`) and forgets them with that read;
  nothing is repaired silently. Such a scan looks normal otherwise — its TIC and every
  trailer field match the healthy scans.
- A raw file reader now releases its file handle through an explicit `File.close()`,
  which `__del__` calls without ever raising, and which the spectrum read path calls
  as soon as a reader is superseded or yields no spectrum. The previous `__del__`
  called `Dispose()` unguarded and raised `TypeError: 'MethodObject' object is not
  callable` whenever it ran during interpreter shutdown.

## [2.5.4]

- First tracked release. Changes before this version were not recorded in the
  repository; the current version lives in `Orbitool/version.py`.
