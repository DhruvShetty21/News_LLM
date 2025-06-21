from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import json
import os

# 1. Load the template from the file
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(current_dir, "..", "prompts", "filter_prompt.txt")

with open(prompt_path, "r", encoding="utf-8") as f:
    template = f.read()

# 2. Create the prompt template
prompt = PromptTemplate(
    input_variables=["article"],
    template=template
)

# 3. Initialize LLM
llm = Ollama(model="mistral")

# 4. Create the chain
chain = prompt | llm

# 5. Define the classifier
import re

def classify_article(article_text):
    raw_response = chain.invoke({"article": article_text})
    print("\n🧠 Raw LLM Response:\n", raw_response)

    try:
        # Extract the first JSON-like object from the response
        json_match = re.search(r'\{.*?\}', raw_response, re.DOTALL)
        if json_match:
            cleaned = json_match.group()
            parsed = json.loads(cleaned)
            return parsed
        else:
            print("⚠️ No JSON found. Returning default.")
            return {}
    except Exception as e:
        print(f"⚠️ Error parsing JSON: {e}")
        return {}
