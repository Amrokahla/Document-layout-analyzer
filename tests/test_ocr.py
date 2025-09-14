import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.ocr_service import perform_ocr

def test_perform_ocr_on_blank_image():
    result = perform_ocr(b"")
    assert result == "" or result is not None