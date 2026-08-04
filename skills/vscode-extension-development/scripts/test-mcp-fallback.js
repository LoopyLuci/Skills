// Test for startHttpServer's EADDRINUSE port-fallback + resolved-port getter.
// Run: node scripts/test-mcp-fallback.js (from the extension project root).
const esbuild = require('esbuild');
const http = require('http');
const path = require('path');
const os = require('os');

async function main() {
  const outfile = path.join(os.tmpdir(), 'mcp-test-bundle.js');
  await esbuild.build({
    entryPoints: [path.join(__dirname, '..', 'src', 'mcp.ts')],
    bundle: true, platform: 'node', format: 'cjs', outfile, logLevel: 'silent',
  });
  const mod = require(outfile);
  const { MCPServer, startHttpServer } = mod;
  if (typeof startHttpServer !== 'function') throw new Error('startHttpServer not exported');

  const blocker = http.createServer((req, res) => res.end('blocker'));
  await new Promise((r) => blocker.listen(0, '127.0.0.1', r));
  const busyPort = blocker.address().port;

  const server = new MCPServer();
  const hs = startHttpServer(server, busyPort);
  await new Promise((r) => setTimeout(r, 200));
  const resolvedPort = hs.port;
  console.log(resolvedPort !== busyPort
    ? `PASS  port fallback: ${busyPort} -> ${resolvedPort}`
    : `FAIL  no fallback (still on ${busyPort})`);

  const res = await fetch(`http://127.0.0.1:${resolvedPort}/health`);
  const data = await res.json();
  console.log(data.status === 'ok'
    ? 'PASS  health endpoint responds after fallback'
    : 'FAIL  health endpoint did not respond ok');

  hs.close();
  await new Promise((r) => blocker.close(r));
}

main().catch((e) => { console.error(e); process.exit(1); });
