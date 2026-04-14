import argparse
import threading
import time
import webbrowser

from web_interface import start_web_server


def main():
    parser = argparse.ArgumentParser(
        description="Launch the local DIFF web configuration interface."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind.")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind.")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the browser automatically.",
    )
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}"

    print("=" * 64)
    print("DIFF web configuration")
    print("Local dashboard only - configuration workspace")
    print(f"URL: {url}")
    print("=" * 64)

    if not args.no_browser:
        def _open_browser():
            time.sleep(1.0)
            webbrowser.open(url)

        threading.Thread(target=_open_browser, daemon=True).start()

    start_web_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
