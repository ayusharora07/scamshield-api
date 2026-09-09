from unittest.mock import MagicMock
import pytest


def test_email_check(client, mocker):
    mocker.patch(
        "app.api.analyze.get_assessment",
        return_value={
            "label": "spam",
            "score": 90,
            "certainty": "high",
            "reason": "Suspicious request",
        },
    )
    response = client.post(
        "/email",
        json={
            "sender": "fraud420@gmail.com",
            "body": "Looking for Loans? Give your Bank Crendentials and get it within an hour",
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert "label" in result
    assert "score" in result
    assert "certainty" in result
    assert "reason" in result


def test_audio_check(client, mocker):
    mocker.patch("app.api.analyze.audio_transcript", return_value="Sample audio text")
    mocker.patch(
        "app.api.analyze.get_assessment",
        return_value={
            "label": "safe",
            "score": 10,
            "certainty": "high",
            "reason": "No threat",
        },
    )
    with open("tests/test_audio.m4a", "rb") as audio:
        response = client.post("/audio", files={"file": audio})
    assert response.status_code == 200
    result = response.json()
    assert "label" in result
    assert "score" in result
    assert "certainty" in result
    assert "reason" in result


@pytest.fixture
def audio_bytes():
    with open("tests/test_audio.m4a", "rb") as audio:
        yield audio.read()


def test1(client, audio_bytes, mocker):
    mocker.patch("app.api.analyze.audio_transcript", return_value="Sample audio text")

    mock_assessment = MagicMock()
    mock_assessment.model_dump.return_value = {
        "label": "spam",
        "score": 80,
        "certainty": "high",
        "reason": "Phishing detection",
    }
    mocker.patch("app.api.analyze.get_assessment", return_value=mock_assessment)

    with client.websocket_connect("/ws") as websocket:
        websocket.send_bytes(audio_bytes)
        result = websocket.receive_json()
        assert "label" in result
        assert "score" in result
        assert "certainty" in result
        assert "reason" in result
