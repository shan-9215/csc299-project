from openai import OpenAI
import os

def summarize(client: OpenAI, text: str) -> str:
    """Send a paragraph to ChatGPT and get a short summary back."""
    messages = [
        {"role": "system", "content": "Summarize each task into a short, clear phrase (max 10 words)."},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
    )
    return response.choices[0].message.content.strip()

def main():
    paragraphs = [
        "Refactor the user authentication system to support multi-factor login. Test all components and deploy before the upcoming sprint review.",
        "Prepare the apartment for guests: clean the living room and kitchen, change sheets, and restock the bathroom essentials by Friday evening."
    ]

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set your OPENAI_API_KEY environment variable.")
        return

    client = OpenAI(api_key=api_key)
    print("\nSummaries:\n")

    for i, p in enumerate(paragraphs, 1):
        summary = summarize(client, p)
        print(f"{i}. {summary}")

if __name__ == "__main__":
    main()
