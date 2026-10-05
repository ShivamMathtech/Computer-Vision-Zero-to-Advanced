# Shared utilities

Reusable code is packaged under `src/cvzero/` so imports work from any notebook after installation. This folder is an orientation marker, not a second implementation directory.

| Need | Module |
| --- | --- |
| Validate RGB, brightness, gains, crop, grayscale, histograms | `cvzero.images` |
| Seeded scenes and hand-checkable arrays | `cvzero.synthetic` |
| Bounded image loading and PNG/JSON output | `cvzero.io` |
| Recorded timing comparisons | `cvzero.benchmark` |
| Reproducible report generation | `cvzero.lab` |
| Runnable commands and input error handling | `cvzero.cli` |
