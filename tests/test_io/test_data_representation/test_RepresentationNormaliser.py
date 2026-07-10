# test_RepresentationNormaliser.py
import pytest

from signnet.io.data_representation.RepresentationNormaliser import RepresentationNormaliser


class TestRepresentationNormaliser:
    """Ensures that interfaces cannot be instantiated directly."""
 
    def test_representation_normaliser_cannot_be_instantiated(self):
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            RepresentationNormaliser()  # type: ignore
 
    def test_subclass_without_implementation_cannot_be_instantiated(self):
        class IncompleteStrategy(RepresentationNormaliser):
            pass
 
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteStrategy()
