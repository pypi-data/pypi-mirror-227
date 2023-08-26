# kicad2junit

A utility to convert KiCad DRC/ERC reports to Junit reports for CI/CD checks.

# Usage

## DRC
```
kicad-cli pcb drc /tmp/drc.json --format json
drc2junit <path/to/drc.json> [path/to/output.xml]
```

## ERC
```
kicad-cli sch erc /tmp/erc.json --format json
erc2junit /tmp/erc.json [path/to/output.xml]
```