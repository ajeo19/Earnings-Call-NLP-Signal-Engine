import pandas as pd


def test_split_transcript_basic() -> None:
    from src.split import split_transcript

    prepared, qa = split_transcript("Prepared remarks. Question and answer session.")
    assert "Prepared remarks." in prepared
    assert "Question and answer session." not in prepared
    assert "Question and answer session." in qa


if __name__ == "__main__":
    test_split_transcript_basic()
    print("split test passed")
