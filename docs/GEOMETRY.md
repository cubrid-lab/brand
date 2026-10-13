# Driver geometry — accepted Connector Study / 02

The original user-approved prototype is retained verbatim at
`provenance/connector-study-02/driver-python.svg`. The prior bootstrap accidentally
substituted a different path shape; this change restores the original contour.

The Driver mark comprises two congruent polygons in a 24 × 24 viewBox.

Let `s = sqrt(3)`, `g = 1.5`, and `d = g / s`. Polygon A vertices are:

1. `(6, 12 - 4s)`
2. `(2, 12)`
3. `(6, 12 + 4s)`
4. `(12 - d, 12 + 4s)`
5. `(10 - d, 12 + 2s)`
6. `(14 - d, 12 - 2s)`
7. `(12 - d, 12 - 4s)`

Polygon B is derived by rotating A by 180° about `(12,12)`; equivalently,
`(x,y) → (24-x,24-y)`.

The outer silhouette is 20u × 8√3u, with edge directions 0°, 60°, and 120°.
The channel has perpendicular mitered width 1.5u. The original imported B path
contains one redundant collinear vertex; the generator removes it without changing
the outline. Tests compare regenerated coordinates with the retained original.

Colors identify implementation language. Python/Go/Rust colors are carried over
from Study / 02. TypeScript is a separately proposed project token; no language
logos are embedded. The Driver shape is **not** the organization-wide logo.

## Status

Design direction approved; review of brand naming, non-infringement and graphics
redistribution licensing remains pending. Do not deploy organization-level identity
from a Driver-specific symbol.
