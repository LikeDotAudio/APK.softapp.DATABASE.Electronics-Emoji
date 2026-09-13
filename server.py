# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
"""server.py — the local HTTP door to the Electronics Emoji symbol set.

Serves this folder on PORT and opens a browser at index.html. It owns nothing
but that: no build, no render, no state. renderPNG.py makes the PNGs.

HTTP IS NOT OPTIONAL. index.html and gallery.htm import symbols/index.js as an
ES module, and browsers refuse module imports under the file:// scheme. Opening
either page by double-clicking it shows an EMPTY GRID AND NO ERROR, which is the
mistake this file exists to prevent -- and the one a reader will otherwise make
twice, because nothing about the blank page says the transport was the problem.

Two doors, and index.html is the wrong one for most visitors: it is the Unicode
proposal, laid out for letter paper. gallery.htm is the symbol lookup.

Must not bind beyond localhost. A taken PORT is not a fault -- an incumbent
serving this same symbols/ tree IS this server, so its URL is the answer.
"""

import errno
import http.server
import os
import urllib.request
import webbrowser

PORT = 8080
BIND = "127.0.0.1"
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# The identity probe reads this, because a static file server has no /api/health
# to ask. Serving the same bytes at the same path is the strongest statement a
# plain file server can make about which tree it is standing on.
IDENTITY = "symbols/index.js"

class Handler(http.server.SimpleHTTPRequestHandler):
    index_pages = ("index.html", "index.htm")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def probe_incumbent(bind, port, timeout=1.5):
    """Ask whoever holds the port whether they are serving THIS symbols/ tree.

    Returns True when the bytes at IDENTITY match the ones on disk here.
    Never raises: this runs on the failure path of a bind, and a launcher that
    dies while explaining why it could not launch has explained nothing.
    """
    try:
        with open(os.path.join(DIRECTORY, IDENTITY), "rb") as handle:
            mine = handle.read(4096)
    except OSError:
        return False
    try:
        with urllib.request.urlopen(f"http://{bind}:{port}/{IDENTITY}",
                                    timeout=timeout) as answer:
            return answer.read(4096) == mine
    except Exception:
        return False


# A SECOND SERVER DEFERS TO THE FIRST RATHER THAN KILLING IT. Until 2026-09-05
# this ran `fuser -k 8080/tcp` on every start, which does not ask what it is
# killing -- 8080 is the most contended port on a developer's bench, and the
# thing holding it was as likely to be somebody's dev server as a stale copy of
# this one. Deferring is the same outcome when the incumbent is us, and not a
# silent execution when it is not.
def _defer_to_incumbent(bind, port, url, err):
    """The port was taken. Decide whether that satisfied the request.

    Returns the process exit code: 0 when this same symbol set already answers
    there, and 1 when something else holds the port -- the only case that is a
    fault, and the case the old kill_port() used to resolve with a signal.
    """
    if not probe_incumbent(bind, port):
        print(f"⛔ Port {port} on {bind} is held by something that is not the "
              f"Electronics Emoji server.")
        print(f"   {err}")
        print(f"   Free it, or edit PORT in this file to {port + 1}.")
        return 1
    print(f"⚡ The Electronics Emoji server is already serving — {url}")
    print(f"   It is serving this same {IDENTITY}. Nothing to do.")
    webbrowser.open(url)
    return 0


def run():
    url = f"http://localhost:{PORT}/index.html"
    # Without this a restart inside the TIME_WAIT window fails on a port nothing
    # is listening on, which reads as another server still running and sends a
    # person hunting a process that is gone. It is also what makes EADDRINUSE
    # below MEAN something: with the socket reused, the only way left to get it
    # is a live listener, so the probe that follows one is asking a real process.
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    try:
        # ThreadingHTTPServer serves the ES module files concurrently instead of
        # one-at-a-time, which speeds up initial load over HTTP/1.1.
        httpd = http.server.ThreadingHTTPServer((BIND, PORT), Handler)
    except OSError as err:
        if err.errno != errno.EADDRINUSE:
            raise
        return _defer_to_incumbent(BIND, PORT, url, err)

    with httpd:
        webbrowser.open(url)
        print(f"Server started at {url}")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
