# Todo

来源：`AverageScans` 崩溃调查。根因是混合扫描列表里存在 FT profile 为空的扫描，交给
`AverageScans` 即崩溃。

> 完成一项就直接删掉，不留归档——本文件只记录未完成的事项。

以下按 待办 / 待评估 / 数据侧 归类。

## 待办

### 1. `MassOptions` 容差单位错 10⁶ 倍（优先级最高）
- [ ] 改 `thermo.py` 的 `Extensions.AverageScans(self.rawfile, average_list,
      MassOptions(rtol, ToleranceUnits.ppm))`（活动那处 + 上面注释掉的那处）。
- 事实：UI 是 ppm 框（`FileUiPy.py:255` 写入 `rtol = 框值 * 1e-6`，默认 1.0 ppm），
  模型存的是**比率**（`file_tab.py:13-14` 默认 `1e-6`），全仓其它消费者也按比率用
  （如 `models/spectrum/_average.pyx:29` `atol = rtol*np.sqrt(mass1/200)*mass1`）；
  只有这一处把它标成 `ToleranceUnits.ppm` → 实际是 **1e-6 ppm ≈ 1e-12 相对容差**，
  比用户意图紧 10⁶ 倍。
- 官方例程（`RawFileReaderExample.py` / `Program.cs`）是
  `Extensions.DefaultMassOptions(rawFile)` + `options.Tolerance = 5.0` + `ToleranceUnits.ppm`；
  实测 `DefaultMassOptions(raw)` 给出的是 `Tolerance=0.5, ToleranceUnits=amu`。
- `MassOptions` 的构造实测只有 `()`、`(Double, ToleranceUnits, Int32 precision)`、
  `(IMassOptionsAccess)` —— **没有** 2 参数版本，第三参数名是 `precision`。
- ⚠️ **改它会改变结果**（分段数据的平均谱会变），需在提交说明里写清楚；
  并且要决定用 `rtol * 1e6` 还是改成 `DefaultMassOptions`。
- 关联小问题：file tab 的 ppm 框**只写不读**（其它 tab 都有 `*1e6` 回显），
  已有工作区里框内显示值可能与 `info.rtol` 不一致。

### 2. 非 Thermo 路径 `reader` 未绑定
- [ ] `models/file/file.py` 的 `get_spectrum_from_info`：`if origin == PATH_TYPE.THERMO.value:`
      之外没有任何分支，`reader` 永远未赋值 → 调用处 `UnboundLocalError`
      （`PATH_TYPE` 只有 `THERMO` / `HDF5`）。
- 建议：对不支持的 origin 抛一个明确的错误，而不是靠未绑定变量炸。

### 3. 空窗口返回时丢弃 `last_reader`
- [ ] `get_spectrum_from_info` 在 `ret is None` 时返回 `None, None`，调用方于是把 reader 丢掉，
      下一个同文件的窗口**重新打开** .RAW（每个 reader 约 11 MB 工作集，实测）。
- 现状：已经把 reader 显式 `close()`（不再等 GC），但"反复重开"仍在。
- 建议（**需拍板**）：返回 `None, LastReader(path=self.path, reader=reader)` 让调用方继续复用，
      代价是这个 reader 会一直开着（11 MB）直到路径变化。哪种更划算取决于实际文件大小与数量。

### 4. 日志轮转不删旧文件
- [ ] `Orbitool/logger.py:13` 的 `TimedRotatingFileHandler(LOG_PATH, when="midnight")`
      **没设 `backupCount`**（默认 0 = 保留全部）→ 轮转出来的 `log.txt.<date>` 永不删除。
- 建议：给一个上限（例如 `backupCount=7`）。

### 5. 每窗口一行 DEBUG 日志要不要长期留（**需拍板**）
- [ ] `thermo.py` 每次 `AverageScans` 成功后一行 `AverageScans ok …`（诊断期加的）。
- 量级：默认「每 2h5m」约 5 行/夜；「每 N 张谱」与窗口数同阶（2 万次扫描 / N=10 → 约 2 千行、约 200 KB / 次 denoise）。
- 选项：① 长期保留；② 只在异常时打（如 `distinct > 1` 或 `ScansCombined != requested`）；
      ③ 挂到 `setting.debug` 下（已有 `NO_MULTIPROCESS` / `thread_block_gui` 两个先例）。

## 待评估（证据不足，先记着）

- [ ] `to_spectrum_filter` 只取 `GetMassRange(0)`（**只有第 0 段**）→ 分段扫描的
      filter 签名看不见段数/后续段。本轮崩溃**已排除**与此有关，但对分段数据是否正确仍待评估。
- [ ] `thermo.py` 的 `_getFirstFilterInRawNumRange(start, stop, filter)` **忽略 `start`/`stop`**，
      只回答"这个文件里有没有任何匹配的 filter"，因此拿它当"窗口非空"的守卫是无效的
      （掩盖空窗口信号，是诊断障碍）。
- [ ] `checkAverageEmpty` 全仓无调用者（死代码）。
- [ ] 损坏缓存目前是 **per reader 实例**；多文件工作区里 reader 每个窗口重建（实测 `call#` 恒为 1），
      所以损坏文件每个受影响窗口都要重学一次（约 +250 ms）。提升为按路径的会话级可省掉 ——
      但会引入 reader 之外的状态，**已决定暂不做**。

## 数据侧（不是代码问题）

- [ ] 那批 `Z:\FileRequests\其无能名的文件收集20261006\Neg_sample_*.raw`（233 个）建议抽查或重导：
      已确认 `Neg_sample_20220605062321.raw` 里 87 条扫描中有 2 条完全没有 profile 数据、
      1 条被截断（7363 点 vs 正常 2.5–5.7 万）。程序现在不会再崩，但数据本身的损伤修不了。

## 零散待办

- 校准时 detail 的 next ion 和双击 ion 跳转
- 文件找不到时给出提示！
- 校准参数导出
