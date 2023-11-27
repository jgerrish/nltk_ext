import pytest
from _pytest.fixtures import FixtureFunctionMarker
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.generator_pipeline import GeneratorPipeline
from nltk_ext.pipelines.recorder import Recorder


class TestRecorder:
    """
    Test the recorder pipeline module
    """

    @pytest.fixture
    def setup(self) -> None:
        self.d1 = Document(
            {"id": "1", "body": "This is a test."},
        )

    def test_process(self, setup: FixtureFunctionMarker) -> None:
        recorder = Recorder([])
        pipeline = GeneratorPipeline([recorder])
        words = pipeline.process(self.d1.words())
        word_list = list(words)
        assert len(word_list) == 5
        assert word_list[0] == "this"
        assert word_list[1] == "is"
        assert word_list[2] == "a"
        assert word_list[3] == "test"
        assert word_list[4] == "."

        word_list = recorder.get_data()
        # print word_list
        assert word_list[0] == "this"
        assert word_list[1] == "is"
        assert word_list[2] == "a"
        assert word_list[3] == "test"
        assert word_list[4] == "."
