"""Running queries against the flight database."""


def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    matches = []
    db_keys = db[0].keys()
    query_keys = query.keys()
    if not set(query_keys).issubset(db_keys):
        return {"query": query,
                "error" : "INVALID_QUERY",
                "matches" : "[]"
                }
    for item in list:
        for k in query_keys:
            if not (query_keys.get(k) is item.get(k)):
                break 
        matches.append(item) 

    return {
        "query": query,
        "matches" : matches
    }


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    results = []
    for q in queries:
        results.append(run_query(db, q))
    return results

