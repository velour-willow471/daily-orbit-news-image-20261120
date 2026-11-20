// The Daily Orbit — entrypoint for the news-image-20261120 competition.
//
// The artwork itself lives in entry.png next to this file (rendered by
// draw.py). This program's only job at grading time is to deliver those
// exact bytes to the output location, untouched, so the picture the
// judge sees is the picture that was committed.
//
// Destination: $MAKEFUN_OUTPUT_DIR/entry.png, falling back to
// /output/entry.png when the variable is not set (the grader's layout).
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the folder this file sits in, then locate the bundled image.
const here = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(here, "entry.png");

// Figure out where the image has to land.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const targetImage = join(outputDir, "entry.png");

// Make sure the destination folder exists, then copy byte for byte.
mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, targetImage);
