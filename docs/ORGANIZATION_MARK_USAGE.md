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
| Candidate A — Three-color solid cube | [`dist/organization/mark.svg`](../dist/organization/mark.svg) | Solid `top`, `left`, and `right` faces using `#006BDA`, `#00A36F`, and `#E60039` with open seams and no role glyph | **Approved for own-organization avatar/profile use (2026-10-15).** Multi-hue faces immediately distinguish the organization from single-token repository icons and stay legible at 16 px. |
| Candidate B — Monochrome slate cube | [`studies/organization/candidate-monochrome-cube.svg`](../studies/organization/candidate-monochrome-cube.svg) | Solid `top`, `left`, and `right` faces in tonal slate/navy (`#284679`, `#071B43`, `#6B7280`) without a role glyph | **Study only.** Evaluates single-family tonal contrast, but at 16–24 px its silhouette reads too close to a Neutral-token repository cube. |
| Candidate C — Open hexagonal frame | [`studies/organization/candidate-hex-frame.svg`](../studies/organization/candidate-hex-frame.svg) | Three-color isometric perimeter ring (`inset_scale = 0.52`) with a hollow center rhombus | **Study only.** Distinct open-center container silhouette, but thinner strokes lose visual weight at 16 px avatar size compared with Candidate A. |

These colors are internal CUBRID Lab design/study tokens, not official CUBRID
brand colors.

Resemblance checks against the Driver and ORM role symbols (`AGENTS.md` rules 1
and 11):

- **Driver role (`src/driver.svg`)**: Uses a single implementation-language token
  (`currentColor`), shading overlays, and a white right-face connector path plus
  terminal node (`<circle cx="18.35" cy="16.15" r="1.7"/>`). All three
  organization candidates omit the connector path, terminal circle, and every
  other internal role glyph.
- **ORM role (`src/orm.svg`)**: Replaces the left and right vertical cube faces
  with two open horizontal chevron layers (`M 2 10.1 ...` and `M 2 14.3 ...`) in
  a single language color. All three organization candidates retain the three
  isometric cube face zones (`top`, `left`, `right`) and never use stacked
  horizontal chevrons.

## Approval scope

On 2026-10-15 the maintainer reviewed the prepared cube preview and explicitly
approved both its design and organization-use rights. The exact confirmation is
recorded in [issue #3](https://github.com/cubrid-lab/brand/issues/3). Separate
`design_status` and `organization_use_rights_status` fields in
[`tokens/organization.json`](../tokens/organization.json) control publication of
the emblem to `dist/organization/`. With either approval pending, the generator
places the emblem under `studies/organization/` and removes any stale approved
copy.

This authorization covers the CUBRID Lab organization avatar and profile mark.
The horizontal and stacked wordmarks remain study candidates. General asset
redistribution licensing and independent legal/trademark clearance remain
pending; see [BRAND_USAGE.md](../BRAND_USAGE.md).

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
- Check that emblem geometry and colors are unchanged and wordmark studies stay
  outside `dist/`.
- Inspect the 16, 32, 48, and 120 px emblem on light/dark backgrounds and the
  512 px avatar export with circular cropping.
- Verify the merged profile in the live organization page and check the actual
  organization avatar separately. Record any missing upload capability rather
  than marking an unperformed avatar upload complete.
