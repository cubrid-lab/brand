# Provenance

## Driver connector

The initial Driver connector was developed during a CUBRID Lab branding design session in October 2026.

Design constraints selected by the maintainer:

- geometry must remain recognizable in monochrome,
- color identifies implementation language,
- shape identifies repository role,
- Driver and ORM must have different silhouettes,
- Driver should express connection without copying a plug, chain, Poké Ball, language logo, or existing CUBRID logo,
- the mark must be reproducible from numeric geometry.

AI-assisted ideation was used during exploration. The first bootstrap PR mistakenly used a **different** polygon. This correction restores the exact selected **Connector Study / 02** construction and retains the earlier original SVG verbatim under `provenance/connector-study-02/driver-python.svg`. Numeric parameters live in `tokens/geometry.json`; the generator uses the original closed-form construction, and tests compare vertex coordinates to the retained source. Generated SVGs are outputs, not independent sources.

## Excluded concepts

Earlier promotional illustrations, mascot concepts, and generated posters are **not** source assets and are intentionally excluded from this repository.

## Review state

- Driver concept: design direction approved
- Driver geometry: restored from original Connector Study / 02 and checked against the retained reference
- Organization emblem / CUBRID Lab wordmark: pending (issue #3)
- ORM / MCP / Operator / Cookbook symbols: pending
- visual-asset redistribution license: pending
- trademark / legal clearance: pending
