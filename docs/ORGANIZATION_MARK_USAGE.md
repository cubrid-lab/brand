# Organization mark usage

The three-color cube in [`dist/organization/mark.svg`](../dist/organization/mark.svg)
is the CUBRID Lab organization emblem. It has no repository-role glyph and is
distinct from the Driver, ORM, and Operator icons.

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
