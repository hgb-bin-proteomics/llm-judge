#!/usr/bin/env python3

# 2026 (c) Micha Birklbauer
# https://github.com/michabirklbauer/

import pytest


def test1():
    from llm_judge import TranslationErrorAccuracy

    te = TranslationErrorAccuracy(
        error_type="accuracy",
        error_subtype="addition",
        error_severity="critical",
        error_index_start=0,
        error_index_end=0,
        description="description",
        location="location",
    )
    assert te.error_subtype == "addition"


def test2():
    from llm_judge import TranslationErrorAccuracy
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _ = TranslationErrorAccuracy(
            error_type="style",
            error_subtype="addition",
            error_severity="critical",
            error_index_start=0,
            error_index_end=0,
            description="description",
            location="location",
        )


def test3():
    from llm_judge import TranslationErrorAccuracy
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _ = TranslationErrorAccuracy(
            error_type="accuracy",
            error_subtype="grammar",
            error_severity="critical",
            error_index_start=0,
            error_index_end=0,
            description="description",
            location="location",
        )


def test4():
    from llm_judge import QualityEstimation

    qe = QualityEstimation(
        source="source",
        machine_translation="machine_translation",
        quality_estimation_value=0.0,
        errors=list(),
    )
    assert qe.quality_estimation_value == pytest.approx(0.0)


def test5():
    from llm_judge import QualityEstimation

    qe = QualityEstimation(
        source="source",
        machine_translation="machine_translation",
        quality_estimation_value=1.0,
        errors=list(),
    )
    assert qe.quality_estimation_value == pytest.approx(1.0)


def test6():
    from llm_judge import QualityEstimation, TranslationError, TranslationErrorAccuracy

    te = TranslationErrorAccuracy(
        error_type="accuracy",
        error_subtype="addition",
        error_severity="critical",
        error_index_start=0,
        error_index_end=0,
        description="description",
        location="location",
    )
    qe = QualityEstimation(
        source="source",
        machine_translation="machine_translation",
        quality_estimation_value=0.8,
        errors=[te],
    )
    assert isinstance(qe.errors[0], TranslationError)
    assert isinstance(qe.errors[0], TranslationErrorAccuracy)


def test7():
    from llm_judge import QualityEstimation
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _ = QualityEstimation(
            source="source",
            machine_translation="machine_translation",
            quality_estimation_value=float("nan"),
            errors=list(),
        )
