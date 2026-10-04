# FAQ

## Cannot open Orbitool

Possible reasons and fixes, in any order:

- Use Windows.
- Install `.NET Framework` **≥ 4.7.2**
  ([download](https://dotnet.microsoft.com/en-us/download/dotnet-framework)).
- Avoid non-ASCII characters in the Orbitool path.
- If Orbitool creates `log.txt` but shows no window, your antivirus is probably
  scanning it — wait; subsequent launches will be fast.

If that doesn't help, check `log.txt` (next to `Orbitool.exe`) and send it to the
maintainers listed in the [README](../../readme.md).

## Why do exported times have no time zone?

The time zone is not recorded in the RAW file. Note the time zone when you take
measurements.

## How do I skip or narrow denoising?

Press **skip** on the [Noise tab](noise.md) to denoise nothing, or set global
noise and LOD to `-1` to denoise only specific mass points.

## Does average-by-scan-number count both polarities?

No. Averaging filters scans by the selected charge, so only scans matching the
polarity are averaged. See [Files tab](file-tab.md#average).
