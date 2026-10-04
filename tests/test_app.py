from app import app


def test_hello_world_returns_200():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Hello" in response.data


def test_checksum_endpoint_exists():
    with app.test_client() as client:
        response = client.get("/checksum?data=abc")
        assert response.status_code == 200


def test_html_input_is_escaped():
    with app.test_client() as client:
        response = client.get("/", query_string={"id": "<b>demo</b>"})
        assert response.status_code == 200
        assert b"<b>demo</b>" not in response.data
        assert b"&lt;b&gt;demo&lt;/b&gt;" in response.data


def test_checksum_uses_sha256():
    with app.test_client() as client:
        response = client.get("/checksum?data=abc")
        assert response.get_data(as_text=True) == (
            "ba7816bf8f01cfea414140de5dae2223"
            "b00361a396177a9cb410ff61f20015ad"
        )


def test_ping_rejects_non_ip_input():
    with app.test_client() as client:
        response = client.get(
            "/ping",
            query_string={"host": "not-an-ip"},
        )
        assert response.status_code == 400
        assert response.get_data(as_text=True) == "Invalid IP address"