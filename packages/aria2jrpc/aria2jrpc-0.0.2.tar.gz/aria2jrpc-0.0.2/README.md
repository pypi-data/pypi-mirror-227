# Aria2jrpc

A wrapper around [Aria2 JSON-RPC](https://aria2.github.io/manual/en/html/aria2c.html#rpc-interface)

## Example usage

```python
from aria2jrpc import Aria2JRPC
aria2_client = Aria2JRPC("http://127.0.0.1:6800", secret="your-secure-secret")
gid = aria2_client.add_uri("http://example.com/file.zip")
aria2_client.pause(gid)
```
