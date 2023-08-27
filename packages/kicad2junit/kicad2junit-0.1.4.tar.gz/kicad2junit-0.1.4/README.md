# kicad2junit

A utility to convert KiCad DRC/ERC reports to Junit reports for CI/CD checks.

# Usage

## DRC
```
usage: drc2junit [-h] [--project [PROJECT]] [--project-dir PROJECT_DIR] [--warn-error] [input] [output]

Convert KiCad DRC report to JUnit

positional arguments:
  input                 JSON DRC report
  output                JUnit XML output

options:
  -h, --help            show this help message and exit
  --project [PROJECT]   Kicad project file
  --project-dir PROJECT_DIR
                        Kicad project directory
  --warn-error          Treat warnings as errors
```

### Example
```sh
kicad-cli pcb drc /tmp/drc.json --format json
drc2junit /tmp/drc.json drc.junit.xml --project /path/to/project.kicad_pro
```

## ERC
```
usage: erc2junit [-h] [--project [PROJECT]] [--project-dir PROJECT_DIR] [--warn-error] [input] [output]

Convert KiCad ERC report to JUnit

positional arguments:
  input                 JSON ERC report
  output                JUnit XML output

options:
  -h, --help            show this help message and exit
  --project [PROJECT]   Kicad project file
  --project-dir PROJECT_DIR
                        Kicad project directory
  --warn-error          Treat warnings as errors
```

### Usage
```sh
kicad-cli sch erc /tmp/erc.json --format json
erc2junit /tmp/erc.json erc.junit.xml --project /path/to/project.kicad_pro
```

## Exit code
The exit code is set to 1 (Failure) if one or more errors are found (and warnings if `--warn-error` is used).

