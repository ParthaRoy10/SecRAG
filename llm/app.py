from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv  
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from cache import create_cache_key,load_cache,save_cache



load_dotenv("./.env")

MODEL_NAME = "gemini-3.1-flash-lite"

GENERATION_SETTINGS = {
    "temperature": 0.2
}

model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    max_retries=2,
    temperature=GENERATION_SETTINGS["temperature"]
)

message = ChatPromptTemplate.from_messages([
        ("system" , "You are a cyber security expert."),
        ("human" , "Describe the {topic}.")
])

parser = StrOutputParser()

chain = message | model | parser

def generate(topic) -> str :

    prompt = (
        "System: You are a cyber security expert.\n"
        f"Human: Describe the {topic}."
    )
    cache_key = create_cache_key(
        prompt=prompt,
        model=MODEL_NAME,
        settings=GENERATION_SETTINGS
    )

    cache = load_cache(cache_key=cache_key)

    if cache is None:
        print("Cache Miss Requesting to gemini")

        response = chain.invoke({"topic": topic})

        
        save_cache(
            cache_key=cache_key,
            prompt=prompt,
            model=MODEL_NAME,
            response=response,
            settings=GENERATION_SETTINGS
        )

    else :
        print("Cache HIT")
        response = cache

    return response


print(generate("sql injection"))
