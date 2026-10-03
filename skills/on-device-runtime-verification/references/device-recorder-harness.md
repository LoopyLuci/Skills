# Pointing a phone at a recorder you control

Recipes for observing what a mobile app actually sends, and for reading the
answer back. The strongest available check, because the assertion is on the wire
format rather than on storage.

## Reaching the host from a physical handset

A handset cannot see the host's `127.0.0.1`. `10.0.2.2` is the *emulator*
loopback and does not work on hardware - relying on it is the most common reason
a "the request never arrived" investigation goes nowhere.

```python
import subprocess
ADB = r"C:\Users\Server\AppData\Local\Android\Sdk\platform-tools\adb.exe"
subprocess.run([ADB, "reverse", f"tcp:{port}", f"tcp:{port}"], timeout=60)
```

After `adb reverse` the app addresses the host as `127.0.0.1:<port>`, with no
change needed to any hardcoded default.

## The recorder

```python
import http.server, json, socketserver, threading

received: list[dict] = []

class Stub(http.server.BaseHTTPRequestHandler):
    def _send(self, obj):
        out = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        received.append(json.loads(body))
        self._send({"choices": [{"message": {"role": "assistant", "content": "ok"}}]})

    def do_GET(self):
        self._send({"models": [{"id": "llama3.2", "name": "llama3.2"}]})

    def log_message(self, *a): pass

srv = socketserver.TCPServer(("127.0.0.1", 0), Stub)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
```

## Reading the reply

Handler responses come back on logcat, not in the `am broadcast` result:

```python
def control(**extras):
    subprocess.run([ADB, "logcat", "-c"], timeout=60)
    args = []
    for k, v in extras.items():
        args += ["--es", k, str(v)]
    subprocess.run(
        [ADB, "shell", "am", "broadcast", "-a", ACTION, "-n", COMPONENT, *args],
        timeout=120,
    )
    time.sleep(1.5)
    log = subprocess.run([ADB, "logcat", "-d"], capture_output=True, text=True,
                         timeout=120).stdout
    body = ""
    for line in log.splitlines():
        if TAG not in line or "onReceive" in line:
            continue
        text = line.split(f"{TAG}:", 1)[-1].strip()
        if "->" in text:      # the reply line, not a trace logged after it
            body = text
    return body
```

## Silence means "did not run"

When no request arrives, log the resolved endpoint and model at the call site
before changing anything else. A silent coroutine, a failed context cast, and a
swallowed exception look identical from outside. Force-stop and relaunch between
runs: an installed-but-not-restarted APK keeps the old code alive and makes a
correct fix look ineffective.

## Screenshots

`adb shell screencap -p /sdcard/x.png` then `adb pull`. Worth capturing when the
claim is visual (a control disabled and labelled), because one frame shows the
working and the disabled control side by side. Derive the tap target from a first
capture rather than guessing the bottom-bar position.

## Making a Kotlin store testable without Robolectric

If a store only reads and writes files, take the directory as its **primary**
constructor parameter and add a `companion object` factory for the Android entry
point. A `Context` parameter with a default does not compile, and a secondary
constructor taking `Context` collides with the primary one. Robolectric for two
JSON files is a poor trade; `TemporaryFolder` on a plain JVM covers the same ground.

## Provider wire shapes worth asserting separately

- OpenAI-compatible: the token cap is `max_tokens` at the top level.
- Ollama: `max_tokens` is ignored; the cap is `options.num_predict`. Sending the
  OpenAI shape leaves the setting inert on this path with no error at all.

Assert whichever shape the target under test actually reads, or the check passes
against the wrong runtime.