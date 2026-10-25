# Wordmark lockup light/dark review (issue #3)

Date: 2026-10-25. Renderer: librsvg (`rsvg-convert`), composited with Pillow. The
text uses the lockups' system font stack (`Arial, Helvetica, sans-serif`); this
sheet was rendered where it resolves to Liberation Sans, so other systems will
show slightly different letterforms. No font file is bundled.

## Review sheet

[`wordmark-lockups/contact-sheet.png`](wordmark-lockups/contact-sheet.png) shows
the four generated lockups in `dist/organization/` at actual display widths
(horizontal 150, 240 and 300 px; stacked 100, 120 and 200 px; the view box
width is 1x) on the light (`#FFFFFF`) and dark (`#0D1117`) review backgrounds.
Cells marked **mismatch** show a variant on the background it is not meant
for, which is the problem the dark variants solve.

Regenerate it, and the table below, with
`python scripts/lockup_previews.py docs/studies/wordmark-lockups/contact-sheet.png`
(optional; needs `rsvg-convert` and Pillow; not used by the build or CI).

## Text contrast

WCAG 2 contrast ratio of each text color on each review background. The colors
come from `wordmarks.variants` in
[`tokens/organization.json`](../../tokens/organization.json);
`tests/test_brand.py` requires at least 4.5:1 for both text lines of every
variant on its own background.

| Variant | Text | Color | On light `#FFFFFF` | On dark `#0D1117` |
| --- | --- | --- | --- | --- |
| light | title | `#071B43` | 16.84 | 1.12 |
| light | tagline | `#284679` | 9.37 | 2.02 |
| dark | title | `#F0F6FC` | 1.09 | 17.39 |
| dark | tagline | `#A8C1E8` | 1.83 | 10.33 |

The light variant's navy title measures 1.12:1 on `#0D1117`, which is why it
nearly disappears on a dark page. The dark variant keeps the same emblem,
layout, font stack and tagline and changes only the two text colors: a near
white title and a light tint of the tagline's navy hue. WCAG 1.4.3 exempts
logotypes; 4.5:1 is used as a review yardstick, not a conformance claim.

## Observations

- The emblem colors are unchanged and read on both backgrounds.
- The tagline's font size is 2.8% of the horizontal width and 3.65% of the
  stacked width. At 150 px (horizontal) and 100 or 120 px (stacked) it is
  under 5 px and not legible; at 240 px horizontal and 200 px stacked it is
  about 7 px. The usage guide therefore sets those minimum display widths for
  the full lockup and says to omit a lockup that would be smaller. The emblem
  alone is approved only as the organization avatar and profile mark, so it is
  not a general substitute for an undersized lockup.
