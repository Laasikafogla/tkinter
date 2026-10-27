"""
main.py - Entry point for HackHub Hackathon Management App.
Run with `python main.py` or `python3 main.py`.
"""

import sys
from store import Store
from ui import HackHubApp


def main():
    store = Store()
    app = HackHubApp(store)
    app.mainloop()


if __name__ == "__main__":
    main()
