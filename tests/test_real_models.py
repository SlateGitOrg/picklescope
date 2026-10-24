"""False-positive check on pinned real models (skipped unless `make fetch-models` ran)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from picklescope import Severity, scan_file

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "eval" / "manifest.json").read_text())["models"]
CACHE = ROOT / ".cache" / "models"


@pytest.mark.parametrize("entry", MANIFEST, ids=lambda e: e["id"])
def test_real_model_has_no_medium_or_higher_findings(entry: dict[str, str]) -> None:
    path = CACHE / entry["id"]
    if not path.exists():
        pytest.skip("real models not downloaded (make fetch-models)")
    report = scan_file(path, hash_file=False)
    assert report.skipped_reason is None
    assert not report.findings_at_least(Severity.MEDIUM), [f.message for f in report.findings]
