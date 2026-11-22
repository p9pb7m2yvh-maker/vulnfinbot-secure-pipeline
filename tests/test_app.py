from app import create_app


def get_client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_ok():
    r = get_client().get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "healthy"}


def test_chat_ok():
    r = get_client().post("/api/chat", json={"message": "How can I manage my monthly budget?"})
    assert r.status_code == 200
    assert "response" in r.get_json()


def test_chat_empty_message():
    r = get_client().post("/api/chat", json={"message": "   "})
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_chat_missing_message():
    r = get_client().post("/api/chat", json={"text": "hello"})
    assert r.status_code == 400


def test_chat_invalid_json():
    r = get_client().post("/api/chat", data="{not json", content_type="application/json")
    assert r.status_code == 400
    # в ответе не должно быть трассировки стека
    assert "Traceback" not in r.get_data(as_text=True)


def test_chat_too_long_message():
    r = get_client().post("/api/chat", json={"message": "a" * 501})
    assert r.status_code == 400


def test_chat_wrong_input_types():
    client = get_client()
    for bad in (123, ["hi"], {"a": 1}, None, True):
        r = client.post("/api/chat", json={"message": bad})
        assert r.status_code == 400
    # сам JSON не объект
    assert client.post("/api/chat", json=["hi"]).status_code == 400


def test_unknown_route_json_error():
    r = get_client().get("/nope")
    assert r.status_code == 404
    assert r.get_json() == {"error": "Not found"}
