# test_CentralityMeasure.py
import pytest
from typing import Any

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure, ParameterSpec
from signnet.models.SignedNetwork import SignedNetwork


# =====================================================================
# 1. PARAMETER SPEC TESTS
# =====================================================================

def test_parameter_spec_initialization_defaults():
    # ARRANGE & ACT
    spec = ParameterSpec(
        name="delta",
        label="factor",
        type="float",
        default=0.25
    )

    # ASSERT
    assert spec.name == "delta"
    assert spec.label == "factor"
    assert spec.type == "float"
    assert spec.default == 0.25
    assert spec.min_value is None
    assert spec.max_value is None
    assert spec.step is None


def test_parameter_spec_initialization_full():
    # ARRANGE & ACT
    spec = ParameterSpec(
        name="iterations",
        label="iter",
        type="int",
        default=10,
        min_value=1,
        max_value=100,
        step=1
    )

    # ASSERT
    assert spec.min_value == 1
    assert spec.max_value == 100
    assert spec.step == 1


# =====================================================================
# 2. ABSTRACT BASE CLASS TESTS (The Contract)
# =====================================================================

def test_cannot_instantiate_abstract_base_class():
    # ARRANGE, ACT & ASSERT
    # Check if python blocks the intantiation of an abstract base class
    with pytest.raises(TypeError, match="Can't instantiate abstract class CentralityMeasure"):
        CentralityMeasure()


def test_subclass_must_implement_abstract_methods():
    # ARRANGE
    # Building an inheriting class which implements no compute
    class IncompleteMeasure(CentralityMeasure):
        @property
        def name(self) -> str:
            return "Incomplete"

    # ACT & ASSERT
    with pytest.raises(TypeError, match="with abstract method"):
        IncompleteMeasure()


def test_successful_subclass_instantiation():
    # ARRANGE
    # A correct implementation of an inheriting class
    class DummyMeasure(CentralityMeasure):
        @property
        def name(self) -> str:
            return "Dummy"
        
        def compute(self, network: SignedNetwork):
            return {"node_1": 1.0}

    # ACT
    instance = DummyMeasure()

    # ASSERT
    assert instance.name == "Dummy"
    assert instance.PARAMETERS == []  
