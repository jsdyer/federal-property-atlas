# Federal Property Atlas

[Open Federal Property Atlas](https://coolcode.ca/federal-property-atlas/)

Locate federal parcels by community, custodian and legal interest. Inspect building area and follow a property into the federal heritage and contaminated-sites records.

<!-- coolcode:guide -->
Search Fisgard in British Columbia and open property 17454. The March 2026 heritage directory links this property to a national historic site, a classified federal heritage building and a heritage lighthouse.
<!-- /coolcode:guide -->

## Using the records

The unit is one DFRP parcel. Retain property and parcel numbers, including leading zeros. Building counts and floor areas come directly from the parcel summary. Buildings can have their own construction dates and condition fields. Exact DFRP-to-FCSI site IDs open the companion tool. The eight manually matched properties in the fixed March 2026 Parks Canada edition provide supplementary heritage context. Most rows in that register do not carry a DFRP property number. Do not infer a property’s legal heritage status from a missing match. Vacancy and disposal decisions are outside the directory.

Search, filter and download every matching record. Selecting a result exposes a shareable record URL. The local Natural Earth backdrop and zoomable point groups work from the deployed files. The optional street-map switch requests tiles from OpenStreetMap. Sources without coordinates still appear in the list and export.

## Sources and verification

- [Directory of Federal Real Property](https://open.canada.ca/data/en/dataset/08013e71-101a-457c-af76-c7b13a08ff64)
- [Parks Canada heritage designations (March 2026)](https://open.canada.ca/data/en/dataset/49d5ba7d-d860-40d9-9183-892979e4acbe)

Contains information licensed under the [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada). Province and state outlines derive from the [Natural Earth 1:50m admin-1 with lakes](https://www.naturalearthdata.com/) public-domain dataset. The bundled [Leaflet](https://leafletjs.com/) license is in web/vendor/LICENSE. The street layer contains © OpenStreetMap contributors.

The site derives dates and counts from each successfully retrieved edition. A weekly GitHub Actions job fetches and validates the source files, checks the app and commits the resulting snapshot. A failed refresh leaves the last working deployment available. The static build expands checked-in regional gzip files. No registration or API key is required.

Run `python scripts/refresh.py` to retrieve sources, `python -m unittest discover -s tests` and `node --test tests/*.test.mjs` for validation, and `python scripts/build.py` to build the site. For local preview run `python -m http.server --directory dist`.

<!-- schedule-reliability -->
## Schedule reliability

Public GitHub repositories can have scheduled workflows disabled after 60 days of inactivity. A separate weekly [schedule guard](.github/workflows/schedule-guard.yml) calls GitHub's enable-workflow API for an explicit list of refresh workflows and itself. It can restore workflows disabled for inactivity, preserves manually disabled workflows, and runs independently of collection failures.

This is an interim mitigation, not a scheduling guarantee: GitHub does not document active-workflow renewal as a permanent exemption, and scheduled runs can be delayed or dropped. A scheduler on our own Linux server is the planned independent trigger. The guard does not collect data, create dummy commits, or change source/check timestamps; successful collection and published data freshness still need monitoring.
<!-- /schedule-reliability -->
