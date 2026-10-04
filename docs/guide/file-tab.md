# Files Tab

Import RAW files and average them into the spectra the rest of the pipeline
works on.

![Files tab](img/file-tab.png)

## Import

- **Import file(s)** (`Alt + I`) or drag files onto the window.
- **Import folder** (`Alt + F`), with the **Subdirectory** checkbox to recurse.
- ![Drag and drop files](img/dragdrop-files.gif)
- ![Drag and drop a folder](img/dragdrop-folder.gif)
- Choose the **polarity** (positive or negative) of your spectra.
- **Remove selected** (`Del`) drops the selected files from the table.

## Filter and pick

- **Spectrum filters** narrow which spectra are shown: add a row with `+`,
  remove it with `-`, then **refresh filter**. Each row is a
  property / operator / value condition.
- **Show spectra for** — **Selected file(s)** (`Alt + S`) or **All file(s)**
  (`Return`) — populates the [Spectra List](dockers.md) with the matching
  spectra. **All if no peak selected** style behaviour applies here too.

## Average

![Custom average period](img/custom-average-period.gif)

The **Average** group defines how spectra are binned:

- **every … period(s)** — average by collection-time window. The duration field
  accepts values like `1000s`, `10m5s`, `1h`, `2h5m`.
- **every … spectra** — average by scan number. Only scans whose charge matches
  the selected polarity are counted, so a 40-scan window covering 20 positive
  and 20 negative spectra still averages just the 20 positive ones.
- **custom** — adjust a single period's borders, or change all periods at once.
  You can export the periods as a CSV, edit it, and import it back. (Generating
  periods by number is marked "coming soon".)

The **Use time range** box limits the source window: set **from**/**to**,
tick **auto**, or **adjust to selected files**.

These buttons configure the averaging; they do **not** start a calculation. The
actual averaging runs when spectra are added.

## Shortcuts

| Key | Action |
| --- | --- |
| `Alt + I` | Import file(s) |
| `Alt + F` | Import folder |
| `Del` | Remove selected file(s) / delete a filter row |
| `Alt + S` | Show spectra for selected file(s) |
| `Return` | Show spectra for all file(s) |
