from src.split import split_transcript


def test_split_transcript_basic() -> None:
    prepared, qa = split_transcript("Prepared remarks. We are pleased with growth. Question and answer session. Analysts asked about margins.")
    assert "Prepared remarks." in prepared
    assert "Question and answer session." not in prepared
    assert "Question and answer session." in qa


if __name__ == "__main__":
    test_split_transcript_basic()
    print("split test passed")
