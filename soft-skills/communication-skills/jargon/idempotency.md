# Idempotency

Provenance: AI-drafted
Credits: roadmap.sh, OpenAPI Initiative, Sebastián Ramírez (FastAPI docs)

Related: [concepts/apis-rest-graphql-grpc.md](../../../concepts/apis-rest-graphql-grpc.md), [builds/fastapi-crud.md](../../../builds/fastapi-crud.md)

Repeating the operation yields the same result as doing it once. A POST that
dedupes by client-generated key is idempotent; a plain "charge the card" POST
is not. Why it matters: networks retry. The system that assumes "sent once =
received once" is the system that double-charges.
