from cache import create_cache_key,CACHE_DIR,save_cache,load_cache

key1 = create_cache_key(
    prompt="Explain SQL injection",
    model="gemini-3.1-flash-lite",
    settings={"temperature": 0.2}
)

key2 = create_cache_key(
    prompt="Explain SQL injection",
    model="gemini-3.1-flash-lite",
    settings={"temperature": 0.2}
)


key3 = create_cache_key(
    prompt="Explain SQL injection",
    model="different-model",
    settings={"temperature": 0.2}
)

'''save_cache(
    key1,
    prompt="Explain SQL injection",
    model="gemini-3.1-flash-lite",
    settings={"temperature": 0.2},
    response="Hello World"
)'''

print(load_cache("6fd467eb2709a9da1820b764fa514f4e49dacea3b03d62c58a0202bd9c0e93d8"))
