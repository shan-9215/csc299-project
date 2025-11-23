# Summary of My Development Process

This project was my final assignment for CSC299, where I built a terminal-based Personal Knowledge Management System (PKMS) and task manager that also uses AI agents. The system can store tasks and notes, search through them, and use the OpenAI API to summarize tasks and generate daily plans. This summary explains, in detail, how I developed the project, the prototypes I created, how I used different kinds of AI coding assistance, and what worked or didn’t work during the process.

---

## Prototypes and Early Experiments

Before writing the final version, I built multiple prototypes (tasks1–tasks5). This helped me explore ideas without getting stuck on details too early.

### tasks1
The first prototype was a simple JSON task storage system. It taught me how to load and save state and how a CLI workflow feels. This stage helped me understand the basics of storing tasks.

### tasks2
Here I expanded on the idea by adding PKMS-style notes. The structure was still rough, but it made me realize I needed better module organization.

### tasks3
In this prototype I learned to use `uv`, a real Python package layout, and pytest. I created tests for JSON operations and ID handling. This helped shape the testing approach in the final project.

### tasks4
This prototype focused only on the OpenAI Chat Completions API. I tested summarizing text with an AI model, which later became the "AI summarizer" used in the `add-task` command of the final version.

### tasks5
This version used GitHub’s spec-kit. I reviewed the structure of a generated task manager, which helped me understand how to design clean command modules for my final build.

These prototypes acted as planning experiments that showed me what worked and what needed to improve.

---

## Building the Final Version

After gathering ideas from my prototypes, I designed a clean and modular structure for the final version under the `final/` directory:

- `__init__.py` – REPL loop  
- `commands.py` – task, note, search, and AI commands  
- `storage.py` – JSON load/save  
- `models.py` – data structures  
- `ai_agent.py` – OpenAI summarizer and planning functions  
- `tests/` – pytest suite

I added a `reset-state` command with confirmation to make demos easier. The REPL interface was designed to be simple, readable, and easy to extend.

---

## How I Used AI Coding Assistants

I used two main AI tools: **ChatGPT** and **GitHub Copilot (Agent Mode)**.

### ChatGPT (direct chat)
I used ChatGPT for:
- Breaking the project into steps  
- Understanding the assignment  
- Planning file structure  
- Debugging JSON issues  
- Writing prompts for Copilot  
- Designing REPL commands  
- Clearing up errors caused by outdated API examples  

ChatGPT also helped me stay aligned with the grading rubric.

### GitHub Copilot (Agent Mode)
I used Copilot Agent to:
- Generate code inside specific files  
- Implement command functions  
- Fix repetitive patterns  
- Create pytest files  
- Write README sections  
- Help with OpenAI integration  

Short, specific prompts worked best. Vague prompts caused Copilot to generate incorrect or outdated code, especially for the OpenAI API.

### Other AI Tools
I used AI briefly to prototype API calls and test ideas in isolation.

---

## What Worked Well

- Building multiple prototypes before the final version  
- Keeping the project modular  
- Writing and using tests early  
- Letting ChatGPT handle planning and explanation tasks  
- Using Copilot to fill in structured code  
- Integrating AI summarization and planning  
- Creating a responsive REPL interface  

---

## What Didn’t Work (False Starts)

- Copilot sometimes generated outdated OpenAI code (`openai.error`), which I had to fix  
- Generating entire files at once caused disorganized code  
- Some prototypes were messy due to unclear structure  
- AI occasionally generated overly complex solutions  
- I had to reorganize my architecture after realizing a cleaner REPL was needed  

These problems helped me understand how to use AI coding assistants responsibly and when to take control manually.

---

## Conclusion

This project taught me how to plan software, build prototypes, write tests, and integrate AI agents into real applications. I learned how to use AI coding assistants effectively while still understanding and managing the code myself. The final system is modular, tested, and complete. It reflects everything I learned across the course and demonstrates how planning, testing, and AI-assisted development can work together to create a full software project.