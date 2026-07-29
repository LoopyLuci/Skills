# dnspython API Patterns for DNS Proxy/Filter Applications

Discovered and validated while building the Sentinel AdBlocker & Firewall.

## RDATA Construction (the big gotcha)

`dns.rdtypes.IN.*` submodules are **lazy-loaded** — they don't exist until explicitly imported:

```python
import dns.rdtypes.IN.A       # provides A rdata
import dns.rdtypes.IN.AAAA    # provides AAAA rdata
```

Constructor signature is `(rdclass, rdtype, address)` — THREE positional args:

```python
# ✅ Correct
dns.rdtypes.IN.A.A(dns.rdataclass.IN, dns.rdatatype.A, "0.0.0.0")
dns.rdtypes.IN.AAAA.AAAA(dns.rdataclass.IN, dns.rdatatype.AAAA, "::")

# ❌ Wrong — will raise: A.__init__() missing 1 required positional argument: 'address'
dns.rdtypes.IN.A.A(0, "0.0.0.0")
```

The wrong form causes a silent failure (timeout from the client's perspective) because the `DnsProtocol.datagram_received` exception handler catches the error and sends nothing back.

## Building a Blocking DNS Response

```python
response = dns.message.make_response(request)     # copies ID + sets QR flag
rrset = dns.rrset.RRset(
    question.name,           # dns.name.Name
    dns.rdataclass.IN,        # 1
    dns.rdatatype.A,          # 1
    60                        # TTL in seconds
)
rrset.add(dns.rdtypes.IN.A.A(dns.rdataclass.IN, dns.rdatatype.A, "0.0.0.0"))
response.answer.append(rrset)
response_wire = response.to_wire()
```

For IPv6 blocking, use `dns.rdtypes.IN.AAAA.AAAA(...)` with address `"::"`.

## Parsing DNS Queries from Wire Format

```python
request = dns.message.from_wire(data)
question = request.question[0]
qname = str(question.name).rstrip(".")      # "doubleclick.net"
qtype = dns.rdatatype.to_text(question.rdtype)  # "A", "AAAA", etc.
```

The trailing dot on `question.name` MUST be stripped before blocklist lookup.

## Sending DNS Queries to Upstream

Three approaches:

### Async (preferred for proxy patterns):
```python
import dns.asyncresolver
resolver = dns.asyncresolver.Resolver()
resolver.nameservers = ["1.1.1.1"]
resolver.port = 53
resolver.timeout = 5.0
resolver.lifetime = 5.0

answer = await resolver.resolve(qname, question.rdtype)
# answer[0] → first IP, answer.response → full dns.message.Message
for rrset in answer.response.answer:
    response.answer.append(rrset)
```

### Sync (for testing/verification):
```python
import dns.resolver
resolver = dns.resolver.Resolver()
resolver.nameservers = ["127.0.0.1"]
resolver.port = 5300
resolver.timeout = 3
answer = resolver.resolve("google.com", "A")
```

## Creating a DNS Query Programmatically

```python
query = dns.message.make_query("doubleclick.net", dns.rdatatype.A)
wire = query.to_wire()
```

## Exception Handling for DNS Operations

| Exception | Meaning |
|-----------|---------|
| `dns.exception.Timeout` | Upstream took too long |
| `dns.resolver.NoAnswer` | Upstream responded with no answer section |
| `dns.resolver.NXDOMAIN` | Domain does not exist |
| `dns.name.EmptyLabel` | Malformed domain name |

Only `Timeout` and `NoAnswer` should be silently swallowed in a proxy context; NXDOMAIN should still return a proper NXDOMAIN response to the client.

## Async UDP Server Pattern

```python
class DnsProtocol(asyncio.DatagramProtocol):
    def __init__(self, proxy):
        self._proxy = proxy
        self._transport = None

    def connection_made(self, transport):
        self._transport = transport

    def datagram_received(self, data, addr):
        asyncio.ensure_future(self._handle(data, addr))

    async def _handle(self, data, addr):
        try:
            response = await self._proxy.handle_query(data, addr)
            if response and self._transport:
                self._transport.sendto(response, addr)
        except Exception as e:
            logger.error("Error handling DNS query: %s", e)

    def error_received(self, exc):
        logger.error("DNS protocol error: %s", exc)

# Start:
transport, protocol = await loop.create_datagram_endpoint(
    lambda: DnsProtocol(proxy),
    local_addr=(bind_host, bind_port),
)
```
