// News-image entry (make.fun, news-image-20261123): the program ships the
// infographic drawn by draw.py from Monday 23 November 2026 reporting and
// writes it to the grader's output directory as entry.png.
// Node 22, standard library only. No network, no secrets, no input files
// beyond entry.png beside this file.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const image = readFileSync(new URL("./entry.png", import.meta.url));
writeFileSync(join(outDir, "entry.png"), image);
