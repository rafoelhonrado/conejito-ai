from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="models/Qwen2.5-3B-Instruct-Q4_K_M.gguf",
    temperature=0,
    max_tokens=64,
    n_ctx=4096,
)

print(llm.invoke("Say hello"))