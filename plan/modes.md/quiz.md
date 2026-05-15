This file describes the quiz mode of Algo Buddy.

When the user enters quiz mode, the LLM (gpt-4o-mini) will be prompted for 10 random questions about the algorithm. 5 questions are multiple choice, and the other 5 are short-response (at most 50 characters per response). At least one of these questions must ask the user for the time complexity of the algorithm (which should be a short-response question). Every other question can be about details of the algorithm's time complexity, the algorithm's common use cases, the algorithm's implementation code, or notable properties about the algorithm (e.g. greedy approach or naive approach is used).

When the user presses "Done", the quiz is evaluated for correctness, and incorrect answers get an explanation.
