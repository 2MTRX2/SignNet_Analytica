# test_DatasetRegistry.py
import pytest
import os

from signnet.io.DatasetRegistry import DatasetRegistry, DatasetInfo

# =====================================================================
# 1. DATASET INFO TESTS (DTO)
# =====================================================================

def test_dataset_info_instantiation():
    # ACT
    info = DatasetInfo(
        name="Test Name",
        filename="test.csv",
        representation_type="Edge List",
        file_type="CSV",
        description="A short test description."
    )

    # ASSERT
    assert info.name == "Test Name"
    assert info.filename == "test.csv"
    assert info.representation_type == "Edge List"
    assert info.file_type == "CSV"
    assert info.description == "A short test description."


# =====================================================================
# 2. DATASET REGISTRY TESTS
# =====================================================================

def test_get_available_names():
    # ACT
    names = DatasetRegistry.get_available_names()

    # ASSERT
    expected_keys = [
        "Sampson Monks (Time 3)",
        "Gama Network of Alliances (positive) and Conflicts (negative)"
    ]
    assert names == expected_keys
    assert len(names) == 2


@pytest.mark.parametrize("lookup_key, expected_filename", [
    ("Sampson Monks (Time 3)", "sampson_signed_t3.csv"),
    ("Gama Network of Alliances (positive) and Conflicts (negative)", "highlandtribes.csv")
])
def test_get_info_success(lookup_key, expected_filename):
    # ACT
    info = DatasetRegistry.get_info(lookup_key)

    # ASSERT
    assert isinstance(info, DatasetInfo)
    assert info.filename == expected_filename


def test_get_info_raises_key_error():
    with pytest.raises(KeyError):
        DatasetRegistry.get_info("Non Existent Dataset")


def test_get_file_path(monkeypatch):
    # ARRANGE
    fake_data_dir = os.path.join("fake", "root", "data")
    monkeypatch.setattr(DatasetRegistry, "DATA_DIR", fake_data_dir)

    lookup_key = "Sampson Monks (Time 3)"
    
    # Erwarteter Pfad basierend auf unserem Fake-Verzeichnis und dem Filename aus der Registry
    expected_path = os.path.join(fake_data_dir, "sampson_signed_t3.csv")

    # ACT
    result_path = DatasetRegistry.get_file_path(lookup_key)

    # ASSERT
    assert result_path == expected_path
