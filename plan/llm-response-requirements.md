# LLM response requirements

For each requirement listed here, a determinstic function can be written to determine whether or not the requirement is satisfied. These test functions must not call the LLM API.

## General
- Every response from the LLM (gpt-4o-mini) returns strictly valid JSON

## Initial code generation
- The generated Python code has no syntax errors.
- If the user enters the name or phrase of an algorithm that tries to solve a problem in which no well-known solution exists, the LLM should not attempt to implement the algorithm.
    - Can be tested by asking the LLM to write code that solves the halting problem.

## Quiz mode

### Correct answers
- In quiz results (for every mode), there is an explanation for the correct responses (at least 25 characters).
- For the explanation of the correct answer, the explanation does not exceed 250 characters.

### Incorrect answers
- In quiz results (for every mode), for every incorrect response, there is an explanation for the incorrect answer the user selected (at least 30 characters).
- In quiz results (for every mode), no explanation of the incorrect response can exceed 500 characters.
- In quiz results (for every mode), for every incorrect response, there is an explanation for the correct answer that should've been selected (at least 30 characters).
- In quiz results (for every mode), no explanation of the correct response can exceed 500 characters.

### Quiz results after study mode only
- Within the same study session after two back-to-back quizzes, the app effectiveness score should be the roughly the same (difference is within 0.005 of the previous score). Back-to-back means after taking the first quiz, the user did not enter any additional content into the "What are you struggling with?" box before taking the quiz again.
- The app effectiveness score, is at least 0.8.
    - effectiveness = (((# of questions in study mode's quiz function whose topics are correctly classified) - (# of questions in study mode's quiz function whose topics are not about what was discussed in the current study mode session) * 0.1) / # of study-mode quiz questions)
    - effectiveness should not be listed as a percentage
    - the optimal effectiveness score is 1
        - if the effectiveness score does exceed 1, do not hide this fact
    - to make effectiveness possible to evaluate meaningfully, there should be 2 questions per topic discussed in study-mode session
