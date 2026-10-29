from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import secrets
import string

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Password Forge | Secure Generator</title>
<style>

:root {
  color-scheme: dark;
  --bg: #171412;
  --panel: #211B17;
  --line: #49382E;
  --text: #F1E7D8;
  --muted: #A99B8D;
  --accent: #D9A77C;
  --accent-hover: #E8BC95;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  padding: 48px 20px;
  background:
    radial-gradient(ellipse at 50% 0%, #38291F 0%, transparent 52%),
    var(--bg);
  color: var(--text);
  font: 15px/1.7 -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
}

main {
  max-width: 540px;
  margin: 0 auto;
}

header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 36px;
}

.logo {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  background: var(--accent);
  color: var(--bg);
  border-radius: 14px;
  font-size: 25px;
}

h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 650;
  letter-spacing: -0.8px;
}

header p {
  margin: 2px 0 0;
  color: var(--muted);
  font-size: 13px;
}

.card {
  background: rgba(33, 27, 23, 0.94);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 24px 70px #0004;
}

.label {
  color: #D6C6B5;
  font-size: 12px;
  font-weight: 650;
  letter-spacing: 0.7px;
}

.output {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding: 16px;
  background: #171412;
  border: 1px solid var(--line);
  border-radius: 12px;
}

#password {
  min-width: 0;
  flex: 1;
  overflow-wrap: anywhere;
  font: 15px/1.8 "SFMono-Regular", Consolas, monospace;
  color: var(--text);
}

button {
  cursor: pointer;
  border: 0;
  border-radius: 10px;
  font: inherit;
  font-weight: 600;
  transition: background 180ms ease, transform 180ms ease;
}

button:active {
  transform: scale(0.98);
}

button:focus-visible,
input:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 4px;
}

button:hover {
  filter: brightness(1.08);
}

.copy {
  flex-shrink: 0;
  background: #33271F;
  color: var(--text);
  padding: 10px 13px;
}

.section {
  margin-top: 28px;
}

.length-head,
.strength-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

#length-value {
  color: var(--accent);
  font-weight: 700;
  font-size: 21px;
}

input[type="range"] {
  width: 100%;
  accent-color: var(--accent);
  margin: 22px 0 8px;
  cursor: pointer;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  color: var(--muted);
  font-size: 12px;
}

.options {
  display: grid;
  gap: 9px;
  margin-top: 14px;
}

.option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 13px 15px;
  background: #171412;
  border: 1px solid #382B22;
  border-radius: 11px;
  transition: border-color 180ms ease;
}

.option:hover {
  border-color: var(--accent);
}

.option small {
  display: block;
  color: var(--muted);
  font-size: 12px;
  margin-top: 2px;
}

input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
}

.meter {
  display: flex;
  gap: 5px;
  margin-top: 13px;
}

.meter span {
  height: 4px;
  flex: 1;
  background: #49382E;
  border-radius: 10px;
}

.meter span.on {
  background: var(--accent);
}

#strength {
  color: var(--accent);
  font-size: 13px;
  font-weight: 650;
}

.generate {
  width: 100%;
  padding: 15px;
  margin-top: 28px;
  background: var(--accent);
  color: #211710;
  font-size: 14px;
  letter-spacing: 0.1px;
}

.generate:hover {
  background: var(--accent-hover);
}

.generate:disabled {
  opacity: 0.65;
  cursor: wait;
}

#message {
  min-height: 22px;
  color: var(--muted);
  font-size: 12px;
  margin-top: 13px;
}

footer {
  text-align: center;
  color: var(--muted);
  font-size: 11px;
  margin-top: 22px;
  letter-spacing: 0.4px;
}

@media (max-width: 480px) {
  body {
    padding: 24px 14px;
  }

  .card {
    padding: 20px;
  }

  h1 {
    font-size: 22px;
  }

  .output {
    padding: 12px;
  }
}
</style>
</head>
<body>
<main>
  <header>
    <div class="logo">♢</div>
    <div><h1>Password Forge</h1><p>Your security, your rules.</p></div>
  </header>
  <section class="card">
    <div class="label">YOUR PASSWORD</div>
    <div class="output">
      <div id="password" aria-live="polite">Click generate to begin</div>
      <button class="copy" id="copy" type="button">Copy</button>
    </div>

    <div class="section">
      <div class="length-head">
        <label class="label" for="length">Password length</label>
        <span id="length-value">20</span>
      </div>
      <input id="length" type="range" min="4" max="64" value="20">
      <div class="range-labels"><span>4 characters</span><span>64 characters</span></div>
    </div>

    <div class="section">
      <div class="label">CHARACTER SETTINGS</div>
      <div class="options">
        <label class="option"><span>Lowercase letters<small>a, b, c ...</small></span><input type="checkbox" id="lower" checked></label>
        <label class="option"><span>Uppercase letters<small>A, B, C ...</small></span><input type="checkbox" id="upper" checked></label>
        <label class="option"><span>Numbers<small>0, 1, 2 ...</small></span><input type="checkbox" id="numbers" checked></label>
        <label class="option"><span>Symbols<small>!, @, #, $ ...</small></span><input type="checkbox" id="symbols" checked></label>
      </div>
    </div>

    <div class="section">
      <div class="strength-head"><span class="label">Password strength</span><span id="strength">Ready</span></div>
      <div class="meter"><span></span><span></span><span></span><span></span></div>
    </div>

    <button class="generate" id="generate" type="button">↻ &nbsp; Generate password</button>
    <div id="message" role="status">Passwords are generated securely on this server.</div>
  </section>
  <footer>♧ &nbsp; Built for privacy. No password history is stored.</footer>
</main>
<script>
const $ = id => document.getElementById(id);
let currentPassword = "";

$("length").addEventListener("input", () => {
  $("length-value").textContent = $("length").value;
});
["lower","upper","numbers","symbols"].forEach(id => {
  $(id).addEventListener("change", updateStrength);
});
function updateStrength() {
  const count = ["lower","upper","numbers","symbols"]
    .filter(id => $(id).checked).length;
  const len = Number($("length").value);
  let score = len >= 16 && count >= 3 ? 4 :
              len >= 12 && count >= 3 ? 3 :
              len >= 8 && count >= 2 ? 2 : 1;
  $("strength").textContent =
    ["","Weak","Moderate","Strong","Very strong"][score];
  document.querySelectorAll(".meter span").forEach((el,i) => {
    el.classList.toggle("on",i < score);
  });
}
$("generate").addEventListener("click", async () => {
  const options = {
    length:Number($("length").value),
    lowercase:$("lower").checked,
    uppercase:$("upper").checked,
    numbers:$("numbers").checked,
    symbols:$("symbols").checked
  };
  if (!Object.values(options).slice(1).some(Boolean)) {
    $("message").textContent = "Select at least one character type.";
    return;
  }
  $("generate").disabled = true;
  $("message").textContent = "Generating securely...";
  try {
    const response = await fetch("/generate", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(options)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Generation failed.");
    currentPassword = data.password;
    $("password").textContent = currentPassword;
    $("message").textContent = "Secure password generated.";
    $("copy").textContent = "Copy";
    updateStrength();
  } catch (error) {
    $("message").textContent = error.message;
  } finally {
    $("generate").disabled = false;
  }
});
$("copy").addEventListener("click", async () => {
  if (!currentPassword) {
    $("message").textContent = "Generate a password first.";
    return;
  }
  try {
    await navigator.clipboard.writeText(currentPassword);
    $("copy").textContent = "Copied!";
    $("message").textContent = "Copied to clipboard.";
  } catch {
    $("message").textContent = "Clipboard unavailable. Select and copy the password.";
  }
});
updateStrength();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def send_data(self, status, content, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_GET(self):
        if self.path != "/":
            self.send_data(404, "Not found", "text/plain; charset=utf-8")
            return

        self.send_data(200, HTML, "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/generate":
            self.send_data(404, "Not found", "text/plain; charset=utf-8")
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 4096:
                raise ValueError("Invalid request size")

            options = json.loads(self.rfile.read(size))
            length = options.get("length", 20)

            if type(length) is not int or not 4 <= length <= 64:
                raise ValueError("Invalid password length")

            groups = []
            if options.get("lowercase") is True:
                groups.append(string.ascii_lowercase)
            if options.get("uppercase") is True:
                groups.append(string.ascii_uppercase)
            if options.get("numbers") is True:
                groups.append(string.digits)
            if options.get("symbols") is True:
                groups.append("!@#$%^&*()-_=+[]{}?")

            if not groups:
                raise ValueError("Select a character type")
            if len(groups) > length:
                raise ValueError("Password length is too short")

            alphabet = "".join(groups)
            password = [secrets.choice(group) for group in groups]
            password.extend(
                secrets.choice(alphabet)
                for _ in range(length - len(password))
            )
            secrets.SystemRandom().shuffle(password)

            self.send_data(
                200,
                json.dumps({"password": "".join(password)}),
                "application/json; charset=utf-8"
            )

        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_data(
                400,
                json.dumps({"error": "Invalid password settings."}),
                "application/json; charset=utf-8"
            )

        except Exception:
            self.send_data(500, json.dumps({
                "error": "Could not generate a password. Please try again."
            }), "application/json; charset=utf-8")

    def log_message(self, format, *args):
        # Avoid logging request details.
        pass


import os
from http.server import ThreadingHTTPServer

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Password Forge is running on port {port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
