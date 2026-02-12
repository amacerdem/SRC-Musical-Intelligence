"""Quick-start runner for MI-Beta pipeline."""
from __future__ import annotations
import sys
from pathlib import Path


def main():
    print("MI-Beta v0.1.0-beta -- Musical Intelligence Scaffold")
    print(f"  96 models across 9 cognitive units")
    print(f"  10 shared mechanisms")
    print(f"  5 cross-unit pathways")
    # Quick self-test
    try:
        from mi_beta.core.registry import ModelRegistry
        registry = ModelRegistry()
        registry.scan()
        models = registry.all_models()
        print(f"  Registry: {len(models)} models discovered")
    except Exception as e:
        print(f"  Registry scan failed: {e}")


if __name__ == "__main__":
    main()
