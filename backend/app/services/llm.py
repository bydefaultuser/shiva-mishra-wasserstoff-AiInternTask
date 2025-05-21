import os
from groq import Groq
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Initialize Groq client using environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

if not GROQ_API_KEY:
    logger.error("❌ GROQ_API_KEY is not set. Please set it in your environment.")
    raise ValueError("GROQ_API_KEY is not set. Please set the GROQ_API_KEY environment variable.")

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    logger.error(f"❌ Failed to initialize Groq client: {e}")
    raise

def generate_structured_answer(
    question: str,
    docs: List[Dict],
    style: str = "detailed",
    include_sources: bool = True,
    length: str = "long"
) -> str:
    """
    Accepts a user question and retrieved document chunks with metadata.
    Returns a structured LLM response with document-level answers and thematic synthesis in Markdown format.
    """
    formatted_chunks = ""
    for i, doc in enumerate(docs):
        doc_id = f"DOC{i + 1:03}"
        content = doc["content"].replace("\n", " ").strip()
        citation = doc["citation"]
        formatted_chunks += f"{doc_id}:\n{content}\nCitation: {citation}\n\n"

    prompt_instructions = ""
    if style == "detailed":
        prompt_instructions += "Provide a detailed and comprehensive answer.\n"
    elif style == "concise":
        prompt_instructions += "Provide a concise and to-the-point answer.\n"

    if include_sources:
        prompt_instructions += "Make sure to explicitly cite the document IDs (DOC001, etc.) when referring to information from specific documents in the themes.\n"
    else:
        prompt_instructions += "You do not need to explicitly cite document IDs in the themes.\n"

    if length == "long":
        prompt_instructions += "The answer can be of considerable length to be thorough.\n"
    elif length == "short":
        prompt_instructions += "Keep the answer brief.\n"

    prompt = f"""
You are an expert legal/technical summarizer. Do the following:

1. Extract a short answer from each document below. Mention the citation in parentheses.
2. Then, synthesize a few high-level themes, group the answers under these themes, and cite the documents using the 'DOCXXX' IDs where relevant.
3. Your output should follow **strictly this format**:

### Documents:
{formatted_chunks}

### Output Format:

📄 Document-Level Answers:
[DOC001]: [Extracted Answer] ([Citation])
[DOC002]: [Extracted Answer] ([Citation])
...

💬 Synthesized Themes:

**Theme 1 – [Theme Title]**
[Summary of this theme. Mention DOC001, DOC004 as support.]

**Theme 2 – [Another Theme]**
...

{prompt_instructions}

Write clearly and concisely.
"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        raise