#!/usr/bin/env python3

# 2026 (c) Micha Birklbauer
# https://github.com/michabirklbauer/

import pytest


def test1():
    from llm_judge._judge import __read_env
    import tempfile

    parsed_env = None
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete_on_close=False
    ) as f:
        f.write(
            """EXAMPLE_API_KEY="ABCDEFGH_=IJKLMNO"

            ANOTHER_EXAMPLE_API_KEY=ABCDEFGH_=IJKLMNOP"""
        )
        f.close()

        parsed_env = __read_env(f.name)
    assert parsed_env is not None
    assert len(parsed_env) == 2
    assert parsed_env["EXAMPLE_API_KEY"] == "ABCDEFGH_=IJKLMNO"
    assert parsed_env["ANOTHER_EXAMPLE_API_KEY"] == "ABCDEFGH_=IJKLMNOP"


def test2():
    from llm_judge._judge import __read_env
    import tempfile

    parsed_env = None
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete_on_close=False
    ) as f:
        f.write(
            """EXAMPLE_API_KEY="ABCDEFGH_=IJKLMNO"

            # this is a comment
            ANOTHER_EXAMPLE_API_KEY=ABCDEFGH_=IJKLMNOP"""
        )
        f.close()

        parsed_env = __read_env(f.name)
    assert parsed_env is not None
    assert len(parsed_env) == 2
    assert parsed_env["EXAMPLE_API_KEY"] == "ABCDEFGH_=IJKLMNO"
    assert parsed_env["ANOTHER_EXAMPLE_API_KEY"] == "ABCDEFGH_=IJKLMNOP"


def test3():
    from llm_judge._judge import __read_env

    with pytest.raises(OSError, match="'.custom_env' not found!"):
        _ = __read_env(".custom_env")


def test4():
    from llm_judge._judge import __read_env
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete_on_close=False
    ) as f:
        f.write(
            """EXAMPLE_API_KEY="ABCDEFGH_=IJKLMNO"
            INVALID_ENV_FMT VALUE
            # this is a comment
            ANOTHER_EXAMPLE_API_KEY=ABCDEFGH_=IJKLMNOP"""
        )
        f.close()

        with pytest.raises(RuntimeError, match="Invalid .env line \\[2\\]"):
            _ = __read_env(f.name)


def test5():
    from llm_judge._judge import __read_env
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete_on_close=False
    ) as f:
        f.write(
            """EXAMPLE_API_KEY="ABCDEFGH_=IJKLMNO"
            # this is a comment
            ANOTHER_EXAMPLE_API_KEY=ABCDEFGH_=IJKLMNOP
            ANOTHER_EXAMPLE_API_KEY=ABCDEFGH_=IJKLMNOP"""
        )
        f.close()

        with pytest.raises(RuntimeError, match="Found duplicate environment variable"):
            _ = __read_env(f.name)
