from backend.services.llm_service import LLMService


def test_llm_generation():
    service = LLMService()

    response = service.generate(
        "Explain overfitting in machine learning in one sentence."
    )

    assert isinstance(response, str)
    assert len(response.strip()) > 0