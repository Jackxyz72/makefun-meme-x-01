// gta6-meme-x-01 entry program.
//
// The entry itself is a post on X; all this repository has to hand over at
// grade time is POST.json, the little file that names that post. So the
// program does exactly one thing: it takes POST.json from the bot directory
// and places a copy in the output directory, byte for byte. Success is
// silent. Anything that goes wrong is reported by name and ends the run
// with exit code 1.

import { copyFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

// Where things live. The grader points the two environment variables at
// its own mounts; the fallbacks are the mounts' usual places, so a plain
// local run behaves the same way.
const BOT_DIR_VAR = "MAKEFUN_BOT_DIR";
const OUTPUT_DIR_VAR = "MAKEFUN_OUTPUT_DIR";
const BOT_DIR_FALLBACK = "/bot";
const OUTPUT_DIR_FALLBACK = "/output";
const WANTED_FILE = "POST.json";

// A directory setting counts only when it holds real text; an unset or
// blank variable falls back to the default mount point.
function pickDirectory(varName: string, fallback: string): string {
  const raw = process.env[varName];
  if (raw === undefined) {
    return fallback;
  }
  const trimmed = raw.trim();
  return trimmed === "" ? fallback : trimmed;
}

// One place for every failure: say plainly what broke, then stop.
function giveUp(complaint: string): never {
  console.error("memex entry failed: " + complaint);
  process.exit(1);
}

function sayWhat(err: unknown): string {
  if (err instanceof Error) {
    return err.message;
  }
  return String(err);
}

// The whole job, in order: work out both directories, make sure the output
// side exists, then carry the file across. Each step names itself in its
// failure message so a broken run says where it broke.
async function carryPostFileAcross(): Promise<void> {
  const botDir = pickDirectory(BOT_DIR_VAR, BOT_DIR_FALLBACK);
  const outputDir = pickDirectory(OUTPUT_DIR_VAR, OUTPUT_DIR_FALLBACK);
  const fromPath = join(botDir, WANTED_FILE);
  const toPath = join(outputDir, WANTED_FILE);

  try {
    await mkdir(outputDir, { recursive: true });
  } catch (err) {
    giveUp("cannot prepare output directory " + outputDir + " (" + sayWhat(err) + ")");
  }

  try {
    await copyFile(fromPath, toPath);
  } catch (err) {
    giveUp("cannot copy " + fromPath + " to " + toPath + " (" + sayWhat(err) + ")");
  }
}

// Kick it off. A rejection that somehow escapes the steps above still has
// to end as a named failure, never as a silent crash dump.
carryPostFileAcross().then(
  () => {
    // Done: the copy is in place and there is nothing to announce.
  },
  (err: unknown) => {
    giveUp("unexpected problem (" + sayWhat(err) + ")");
  },
);
