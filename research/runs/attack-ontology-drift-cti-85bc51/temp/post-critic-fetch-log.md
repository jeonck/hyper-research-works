# Step 13 — gap fetch after the critics

The critics named five gaps. Three were closable from artefacts already on
disk and were closed without a fetch wave:

1. **MITRE's reporting-bias taxonomy and the Sightings Ecosystem telemetry.**
   Present in the vault and uncited by the draft; now cited in Section 7.6,
   where it qualifies our own long-tail refutation rather than supporting it.
2. **The survey that sets the novelty bar.** Present in the vault; now carries
   Section 10's statement of what an SCI-level contribution must demonstrate.
3. **MITRE's own version-orphaned Navigator sample layers.** The measurement
   was recomputed directly from the cloned repositories rather than re-fetched,
   and now appears disaggregated in Section 9.

Two gaps remain open and are recorded in `corpus-critic-gaps.json` rather than
papered over:

4. **The data-source and data-component ontology remodelled at v10**, which
   every detection coverage layer is built from. Measuring its drift is a new
   experiment, not a patch, and it is named as further work.
5. **Telemetry-derived prevalence.** The Sightings summary statistics are
   citable; the underlying event data is not public, so the long-tail question
   is stated as open on the telemetry distribution.

No fetch wave was dispatched: the egress proxy blocks every source host in this
environment, and both remaining gaps need data that no amount of fetching in
this session would reach.
