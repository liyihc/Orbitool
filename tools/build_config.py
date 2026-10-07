from dataclasses import asdict, dataclass, fields
import json
from pathlib import Path

CONFIG_PATH = Path("build-config.json")


@dataclass
class Config:
    not_compile_once: bool = False
    compile: bool = True
    test: bool = True
    build: bool = True
    zip_file: bool = True
    upx_dir: str = ""
    mingw_dir: str = ""


def load_config():
    """Tolerant read: missing/broken file -> (default config, False).

    Unknown keys (e.g. from older configs) are dropped, known keys are kept.
    Does not create or modify the file.
    """
    try:
        data = json.loads(CONFIG_PATH.read_text())
        known = {f.name for f in fields(Config)}
        config = Config(**{k: v for k, v in data.items() if k in known})
        return config, True
    except FileNotFoundError:
        return Config(), False
    except Exception:
        return Config(), False


def save_config(config: Config):
    CONFIG_PATH.write_text(json.dumps(asdict(config), indent=4))


def read_config():
    """build.py semantics: (config file already existed, config).

    Always (re)writes the file, applying the `not_compile_once` one-shot
    flag: when compile+not_compile_once, the persisted flag is reset to
    False and the returned config has compile disabled for this run only.
    """
    config, exists = load_config()
    not_compile_once = config.not_compile_once
    if config.compile and not_compile_once:
        config.not_compile_once = False
    save_config(config)
    if config.compile and not_compile_once:
        config.compile = False

    return exists, config
