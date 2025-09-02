# solaris-observe

A friendly, modular starting point for **telescope observations** in Python.

This repository gives you:

- a **CLI** to run observation schedules and simple tracking  
- a clean **library** you can extend step-by-step  
- a **simulator** so you can develop and test without hardware  
- a place to keep your **legacy** scripts while you migrate

It’s designed for contributors who are **not expert programmers**: each module
has a clear purpose, small interfaces, and examples below.

---

## Quick start

### 1) Install (recommended: Poetry)

```bash
poetry install
```

### 2) Run the CLI

```bash
poetry run solaris-observe --help
poetry run solaris-observe schedule path/to/file.lis --site TG --driver sim
poetry run solaris-observe track Sun --duration 300 --site TG
```

> The current CLI is a **skeleton**: it prints what it would do.  
> As you implement modules, the same commands will start doing real work.

### 3) Run tests

```bash
pytest -q
```

---

## Repository layout (what lives where, and why)

```
solaris-observe/
├─ pyproject.toml          # package + CLI entrypoint (Poetry)
├─ README.md               # you are here
├─ solaris_observe/        # the library (importable code)
│  ├─ cli/                 # CLI only: parse args, call library code
│  ├─ core/                # algorithms & data (no hardware here)
│  ├─ drivers/             # hardware adapters (or simulator)
│  ├─ runner/              # high-level "do the thing" orchestrators
│  ├─ config/              # config files and schemas (if any)
│  ├─ io/                  # logging/trace helpers (no telescope IO)
│  └─ utils/               # small helpers (time, units, etc.)
├─ legacy/                 # your old scripts live here, unchanged
└─ tests/                  # unit + integration tests
```

### Mental model

- **CLI** = a thin shell: translate user flags → call functions.
- **core** = pure logic (patterns, parsing, coordinates). Easy to test.
- **drivers** = talk to the **real telescope** (or to a simulator).
- **runner** = glue: take a plan from `core`, call a `driver` safely.
- **io** = logs and traces (for debugging and “golden” comparisons).
- **legacy** = keep the old code for reference while you migrate.

This separation keeps the “hard parts” (algorithms) independent from
hardware and the command line. It makes testing and refactoring much safer.

---

## How to extend each module

### `solaris_observe/cli/`
- Purpose: **only** parse arguments and call library functions.

### `solaris_observe/core/`
- Pure logic, no sockets.  
- Implement schedule parser, coordinate conversions, scan patterns, tracking.

### `solaris_observe/drivers/`
- Hardware adapters or simulators.  
- Keep all UDP/socket logic here.

### `solaris_observe/runner/`
- Orchestration: read schedule, call drivers, handle timing.  
- Where you implement actual scan/track loops.

### `solaris_observe/config/`
- Example YAML configs for site and driver parameters.

### `solaris_observe/io/`
- Logging and trace utilities.

### `solaris_observe/utils/`
- Small helpers, like virtual time.

### `legacy/`
- Keep the old scripts, unchanged, for reference.

### `tests/`
- `unit/`: fast tests for `core/`.  
- `integration/`: run runners with the simulator.  
- `golden/`: save driver traces for comparison.

---

## Development workflow (step-by-step)

1. Implement schedule parser (`core/schedule.py`).  
2. Implement serpentine scan pattern (`core/patterns.py`).  
3. Implement RA/Dec ↔ Alt/Az (`core/coords.py`).  
4. Wire a runner (`runner/schedule_runner.py`) using `sim_motor`.  
5. Port UDP motor driver (`drivers/udp_motor.py`).  
6. Extend the CLI to call runners.  
7. Add tracking support (`core/tracker.py` + `runner/track_runner.py`).

---

## CLI examples

```bash
solaris-observe schedule data/Sun_20250530_120000.lis --site TG --driver sim
solaris-observe schedule data/Sun_20250530_120000.lis --site TG --driver udp
solaris-observe track Sun --duration 600 --site TG
solaris-observe track Sun --duration 300 --site TG   --offset-ra 0.25d --offset-dec -0.10d
```

---

## Roadmap

- [ ] Implement `.lis` parser.  
- [ ] Add coordinate conversions.  
- [ ] Wire schedule runner to simulator.  
- [ ] Port UDP driver commands.  
- [ ] Add tracking.  
- [ ] Logging and traces.  
- [ ] Golden tests vs legacy.

---

## Coding style

- English comments/docstrings.  
- Small functions, one purpose.  
- Configurable constants (no hard-coded numbers).  
- Line length: 88 chars.  
- Add type hints.  
- Logs: one line per action with time + key params.
