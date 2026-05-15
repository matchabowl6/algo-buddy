You are to generate an AI assistant named 'Algo Buddy' that helps you prepare for technical interviews by helping you learn common algorithms. This is a website that can run locally, but calls the OpenAI API to perform the LLM work.

The LLM used is OpenAI's gpt-4o-mini, and the website makes calls to the OpenAI API using gpt-4o-mini to process user responses entered in Algo Buddy.

On the home page, the user enters the name of a common algorithm. The LLM then generates code for the algorithm with comments.

The code generated should be strictly valid Python code, but the Python code should be understandable by someone fairly new to Python. For example, instead of a list comprehension over a 2D array, use nested for loops.

IMPORTANT: The response of the OpenAI API call should never hallucinate answers. If the user asks the LLM (gpt) about a very niche algorithm used by less than 3 people around the world, or if the user asks for an algorithm that solves a problem nobody has solved before, the LLM should not try to implement the algorithm. Instead, the LLM should say "I don't know how to implement this, but I can help you with a more common algorithm".

After code generation there are two actions the user can perform. Each action is a mode. The first is a study mode, and the second is a quiz mode. See the modes directory (located in the same directory as this Markdown file) for details about each mode.

When implementing the website's source code, do not edit any of the Markdown files, and do not edit .gitattributes and .gitignore. Ignore and do not edit report.md.
