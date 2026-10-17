// stills.mjs <CompositionId> <t1,t2,...> <outDir> [scale]
// Render keyframe stills (seconds) of one Remotion composition through ONE bundle, far faster than N `remotion still` calls.
// Run from the project's video/ folder (needs src/index.ts and node_modules/@remotion/*). Copy this file under video/ if
// Node cannot resolve @remotion/bundler from here. Output: <outDir>/t<sec>.png (decimal point becomes underscore).
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';

const [id, times, outDir, scaleArg] = process.argv.slice(2);
if (!id || !times || !outDir) {
  console.error('usage: node stills.mjs <CompositionId> <t1,t2,...> <outDir> [scale=0.5]');
  process.exit(2);
}
const cwd = process.cwd();
const serveUrl = await bundle({entryPoint: path.join(cwd, 'src/index.ts'), webpackOverride: (c) => c});
const comp = await selectComposition({serveUrl, id});
for (const t of times.split(',').map(Number)) {
  await renderStill({
    composition: comp,
    serveUrl,
    frame: Math.round(t * comp.fps),
    output: path.join(outDir, `t${String(t).replace('.', '_')}.png`),
    scale: Number(scaleArg ?? 0.5),
  });
  console.log('done', t);
}
