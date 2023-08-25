import pytest

from chemchef.engine.indexing.keyword_similarity import parse_assistant_message, \
    SimilarityTestResponseParsingError, TargetCandidatesTuple, construct_user_message, SynonymsHyponymsHypernymsTuple, \
    construct_assistant_message


def test_parse_assistant_message() -> None:
    message = """Synonyms: sport\nHyponyms: football, rugby\nHypernyms:"""

    result = parse_assistant_message(message)
    assert result.synonyms == {"sport"}
    assert result.hyponyms == {"football", "rugby"}
    assert result.hypernyms == set()


def test_parse_assistant_message_with_extra_whitespace() -> None:
    message = """Synonyms: sport \n Hyponyms: football,  rugby\nHypernyms: \n"""

    result = parse_assistant_message(message)
    assert result.synonyms == {"sport"}
    assert result.hyponyms == {"football", "rugby"}
    assert result.hypernyms == set()


def test_parse_assistant_message_with_wrong_line_headers() -> None:
    message = """Synonyms: sport\nWRONG: football, rugby\nHypernyms:"""

    with pytest.raises(SimilarityTestResponseParsingError):
        parse_assistant_message(message)


def test_parse_assistant_message_with_wrong_number_of_lines() -> None:
    message = """Synonyms: sport\nHyponyms: football, rugby\nHypernyms:foo\nExtra line"""

    with pytest.raises(SimilarityTestResponseParsingError):
        parse_assistant_message(message)


def test_construct_user_message() -> None:
    target_candidate_tuple = TargetCandidatesTuple(target="foo", candidates=["bar", "aaa"])
    message = construct_user_message(target_candidate_tuple)
    assert message == "Target: foo\nCandidates: bar, aaa"


def test_construct_assistant_message() -> None:
    result_tuple = SynonymsHyponymsHypernymsTuple(
        synonyms={"foo"}, hyponyms=set(), hypernyms={"bar", "aaa"}
    )
    message = construct_assistant_message(result_tuple)
    assert (message == "Synonyms: foo\nHyponyms: \nHypernyms: bar, aaa"
        or message == "Synonyms: foo\nHyponyms: \nHypernyms: aaa, bar")
