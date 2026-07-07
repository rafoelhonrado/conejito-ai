"""
llm.py

Loads the local GGUF model using llama.cpp.
"""

import os

from dotenv import load_dotenv
from llama_cpp import Llama

# ============================================================
# Load .env
# ============================================================

load_dotenv()

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/Qwen2.5-3B-Instruct-Q4_K_M.gguf"
)

# ============================================================
# Verify model exists
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"\nModel not found:\n\n{MODEL_PATH}\n"
    )

# ============================================================
# Load model
# ============================================================

print("\nLoading model...")
print(MODEL_PATH)

llm = Llama(
    model_path=MODEL_PATH,

    # Context
    n_ctx=4096,

    # CPU Threads
    n_threads=os.cpu_count(),

    # GPU
    n_gpu_layers=0,

    # Performance
    n_batch=512,

    # Sampling
    temperature=0.0,
    top_p=0.95,

    # Faster
    verbose=False
)

print("Model loaded successfully.\n")


# ============================================================
# Chat Function
# ============================================================

def chat(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 512,
):
    """
    Send a prompt to the local LLM.

    Returns the assistant text.
    """

    response = llm.create_chat_completion(

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],

        max_tokens=max_tokens,

        temperature=0,

        response_format={
            "type": "json_object"
        }

    )

    return response["choices"][0]["message"]["content"]


# ============================================================
# Interactive Test
# ============================================================

if __name__ == "__main__":

    while True:

        question = input("> ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = chat(
            "You are a helpful assistant.",
            question
        )

        print()
        print(answer)
        print()
