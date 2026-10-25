# Organization mark usage

The three-color cube in [`dist/organization/mark.svg`](../dist/organization/mark.svg)
is the CUBRID Lab organization emblem. It has no repository-role glyph and is
distinct from the Driver, ORM, and Operator icons.

## Candidate evaluation and role-symbol distinction

Three distinct organization mark candidates share the 24×24, 60°/120° isometric
construction grammar in [`tokens/geometry.json`](../tokens/geometry.json) and
[`tokens/organization.json`](../tokens/organization.json):

| Candidate | File | Construction and study palette | Status and rationale |
| --- | --- | --- | --- |
| Candidate A — Three-color solid cube | [`dist/organization/mark.svg`](../dist/organization/mark.svg) | Solid `top`, `left`, and `right` faces using `#006BDA`, `#00A36F`, and `#E60039` with open seams and no role glyph | **Selected emblem**, approved for the organization avatar and profile only (status: `emblem` in [`tokens/organization.json`](../tokens/organization.json)). Multi-hue faces immediately distinguish the organization from single-token repository icons and stay legible at 16 px. |
| Candidate B — Monochrome slate cube | [`studies/organization/candidate-monochrome-cube.svg`](../studies/organization/candidate-monochrome-cube.svg) | Solid `top`, `left`, and `right` faces in tonal slate/navy (`#284679`, `#071B43`, `#6B7280`) without a role glyph | **Study only.** Evaluates single-family tonal contrast, but at 16–24 px its silhouette reads too close to a Neutral-token repository cube. |
| Candidate C — Open hexagonal frame | [`studies/organization/candidate-hex-frame.svg`](../studies/organization/candidate-hex-frame.svg) | Three-color isometric perimeter ring (`inset_scale = 0.52`) with a hollow center rhombus | **Study only.** Distinct open-center container silhouette, but thinner strokes lose visual weight at 16 px avatar size compared with Candidate A. |

These colors are internal CUBRID Lab design/study tokens, not official CUBRID
brand colors.

Resemblance checks against the Driver and ORM role symbols (`AGENTS.md` rules 1
and 11):

- **Driver role (`src/driver.svg`)**: Replaces the left and right vertical cube
  faces with two open horizontal chevron layers (`M 2 10.1 ...` and
  `M 2 14.3 ...`) under the top rhombus, in a single language color
  (`currentColor`). All three organization candidates retain the three
  isometric cube face zones (`top`, `left`, `right`) and never use stacked
  horizontal chevrons.
- **ORM role (`src/orm.svg`)**: A single language color with the left face as a
  front plate and two bent layers (top strip plus right-face strip) beside it,
  with no full top or right face. All three organization candidates keep the
  complete top and right faces, use no internal role glyph, and never split a
  face into lateral layers.

## Approval scope

The maintainer explicitly approved both the emblem's design and its
organization-use rights; the decision is recorded in
[PROVENANCE.md](../PROVENANCE.md#review-state) and
[issue #3](https://github.com/cubrid-lab/brand/issues/3). Separate
`design_status` and `organization_use_rights_status` fields in
[`tokens/organization.json`](../tokens/organization.json) control publication of
the emblem to `dist/organization/`. With either approval pending, the generator
places the emblem under `studies/organization/` and removes any stale approved
copy. Those fields are the authoritative current status.

This authorization covers the CUBRID Lab organization avatar and profile mark.
The wordmark lockups have their own, separate approval (below). No visual-asset
license is offered, and independent legal/trademark clearance is pending; see
[BRAND_USAGE.md](../BRAND_USAGE.md).

## Wordmark lockups

The lockups combine the unchanged emblem with the `CUBRID Lab` wordmark and the
tagline “Open Source for a More Connected World”. Each layout has a variant for
light backgrounds and one for dark backgrounds:

| Layout | Light backgrounds | Dark backgrounds | View box | Minimum display width |
| --- | --- | --- | --- | --- |
| Horizontal | [`lockup-horizontal.svg`](../dist/organization/lockup-horizontal.svg) | [`lockup-horizontal-dark.svg`](../dist/organization/lockup-horizontal-dark.svg) | 300 × 64 | 240 px |
| Stacked | [`lockup-stacked.svg`](../dist/organization/lockup-stacked.svg) | [`lockup-stacked-dark.svg`](../dist/organization/lockup-stacked-dark.svg) | 200 × 154 | 200 px |

### Approval scope

The maintainer approved the horizontal and stacked lockup design, with the
tagline, as-is on light backgrounds, and asked for dark-background variants with
light text and an unchanged emblem. The current status is `wordmarks` in
[`tokens/organization.json`](../tokens/organization.json); the reviewed renders
and revision are recorded in [PROVENANCE.md](../PROVENANCE.md#review-state) and
[issue #3](https://github.com/cubrid-lab/brand/issues/3).

The approval covers the design and CUBRID Lab's own organization use. Its
`design_status` and `organization_use_rights_status` fields route the lockups:
with both approved the generator writes all four to `dist/organization/`; with
either pending it writes them to `studies/organization/` as studies and removes
the stale copies. It is not a license and not a legal or trademark clearance,
and it does not change the emblem approval or the repository icon decisions.

Own organization use means showing an unmodified lockup, by a commit-pinned
`raw.githubusercontent.com` URL, on surfaces CUBRID Lab controls: the
organization profile, READMEs of repositories owned by the `cubrid-lab`
organization, and CUBRID Lab documentation and community sites. As with the
repository icons in [BRAND_USAGE.md](../BRAND_USAGE.md#repository-icon-use),
copying the SVG into another repository or package, modifying, recoloring,
cropping or rasterizing it, and any use outside CUBRID Lab are not permitted.
Never place a lockup next to an official CUBRID logo or wordmark, and never use
a lockup or a role icon as the avatar.

### Choosing a variant

- Use the light variant (navy text) on white or light backgrounds and the dark
  variant (light text) on dark backgrounds such as GitHub's dark theme
  (`#0D1117`). Never place a variant on the other background: its text drops
  to about 1.1:1 contrast (see the
  [review sheet](studies/wordmark-lockups.md)).
- Where the page follows the viewer's color scheme, as on GitHub, serve both
  with `<picture>`.
- Below the minimum display width the tagline is not legible, so leave the
  lockup out. The emblem alone is approved only as the organization avatar and
  profile mark; do not substitute it for an undersized lockup anywhere else.
- The text is drawn with the `Arial, Helvetica, sans-serif` system fonts, so
  letterforms vary slightly by platform. Do not convert the text to outlines or
  add a font; change the generator if a different treatment is needed.

GitHub README example (replace `<commit>` with the merged revision that holds
the files):

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cubrid-lab/brand/<commit>/dist/organization/lockup-horizontal-dark.svg">
  <img src="https://raw.githubusercontent.com/cubrid-lab/brand/<commit>/dist/organization/lockup-horizontal.svg" width="300" alt="CUBRID Lab: Open Source for a More Connected World">
</picture>
```

The `<img>` fallback is the light variant; a viewer without a color-scheme
preference sees it. Text contrast for both variants is recorded in the
[wordmark lockup review](studies/wordmark-lockups.md).

## GitHub organization profile

Use the approved emblem at 120 px, centered above the existing `CUBRID Lab`
heading in `cubrid-lab/.github/profile/README.md`. Link the image to this brand
repository and provide alt text identifying the organization mark. Pin the image
URL to the final merged commit containing `dist/organization/mark.svg`.

Preserve the existing profile text, project links, and independence/trademark
notices. Record the integration PR and immutable asset revision in issue #3.

## GitHub avatar

The avatar uses the emblem alone. The SVG's square view box fits the prepared
512 × 512 transparent PNG and circular cropping; do not use a wordmark lockup or
repository-role icon as the avatar.

The standard-library brand build generates the canonical SVG. An existing
CairoSVG installation can export the upload file without changing the build's
dependencies:

```bash
python3 - <<'PY'
import cairosvg

cairosvg.svg2png(
    url="dist/organization/mark.svg",
    write_to="/tmp/cubrid-lab-organization-avatar-512.png",
    output_width=512,
    output_height=512,
)
PY
```

GitHub documents avatar upload in the organization's authenticated
[profile settings](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile#changing-your-organizations-profile-picture).
The documented [REST organization update](https://docs.github.com/en/rest/orgs/orgs#update-an-organization)
does not accept an avatar image.
Changing the profile README or preparing a PNG does not update the avatar.

## Verification

- Run the brand build and tests, including withheld/revoked approval routing and
  stale-output cleanup.
- Check that emblem geometry and colors are unchanged, that the lockups follow
  their own approval statuses, and that each dark lockup differs from its light
  one only in the text colors, with at least 4.5:1 text contrast on its
  background.
- Inspect the lockups at their display widths on light and dark backgrounds
  with `scripts/lockup_previews.py`.
- Inspect the 16, 32, 48, and 120 px emblem on light/dark backgrounds and the
  512 px avatar export with circular cropping.
- Verify the merged profile in the live organization page and check the actual
  organization avatar separately. Record any missing upload capability rather
  than marking an unperformed avatar upload complete.
