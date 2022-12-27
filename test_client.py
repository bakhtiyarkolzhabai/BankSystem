from client import Client


def test_client_create():
    client = Client.from_names(name="John")
    assert isinstance(client, Client)
    assert client.name == "John"
