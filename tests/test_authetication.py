import pytest


def test_auth():
    assert True

def test_sample_fail():
    assert False

def test_sample_fail2():
    assert 1 / 0 

def test_skipped_runtime():
    pytest.skip("Skipping this test at runtime")
