from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "frontend" / "app.py"


def test_chat_screen_shows_welcome_and_interactive_suggestions():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=10)

    assert not app.exception
    assert any("Temukan jawaban" in item.value for item in app.title)
    assert any("Ketik pertanyaan" in item.placeholder for item in app.chat_input)
    labels = [button.label for button in app.button]
    assert any("beasiswa" in label.lower() for label in labels)
    assert any("cuti" in label.lower() for label in labels)


def test_suggested_question_returns_answer_with_document_sources():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=10)
    app.button[0].click().run(timeout=10)

    assert not app.exception
    messages = app.session_state["messages"]
    assert [message["role"] for message in messages] == ["user", "assistant"]
    assert messages[1]["sources"][0]["source"] == "01_Pedoman_Akademik_2026.pdf"


def test_user_and_assistant_bubbles_have_opposite_alignment():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=10)
    css = "\\n".join(item.value for item in app.markdown if item.value.startswith("<style>"))

    assert '[data-testid="stChatMessage"]:has([aria-label="Chat message from user"])' in css
    assert "flex-direction:row-reverse" in css.replace(" ", "")
    assert "margin:0 !important" in css
    assert '[aria-label="Chat message from assistant"]' in css
