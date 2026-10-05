# Challenge — A batch image audit for a small design studio

A studio receives a folder of images from several devices. Before editing, it wants a local report describing which files can be used safely in an 8-bit RGB workflow. Build that report using only concepts from Chapter 01.

## Acceptance criteria

- Accept an input folder and a new output folder as configuration.
- Inspect common image files; report errors per file without pretending failed reads succeeded.
- Record dimensions, dtype, original mode if available, channel means and decoded array bytes.
- Create a contact sheet with filenames and explain any conversion of grayscale or alpha input.
- Preserve source files, avoid silent overwrites and include run parameters and environment versions.
- Demonstrate at least one valid RGB image, one grayscale image, one transparent image, one corrupt file and one missing path in a controlled test.
- Explain why neither a channel mean nor a histogram establishes that an image is “good.”

## Constraints

No model, cloud API, webcam or large external dataset. Generate small fixtures yourself. Do not hardcode a personal path. The tool should provide a useful failure message when no usable images exist.

## Submission

Provide code, a short README, a generated report, test evidence and a paragraph describing one unresolved limitation. No solution is supplied: decide the decomposition, data structures and report design yourself.
