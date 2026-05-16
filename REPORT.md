# Project report

Possibly elaborate on eval metrics.
Also elaborate on why a single LLM prompt cannot be used to service the whole website.

Initial website was developed by prompting Kiro to "implement the website described in plan/start.md".

## Course corrections

Previously, the eval metric was whether or not the LLM would classify common properties about the algorithm correctly (in particular, time/space complexity and approach). This is not a good metric to evaluate
the AI assistant's accuracy because the app is working with common, well-known, and well-studied algorithms. Because of this, the LLM will get these correct with 99% accuracy or higher all the time without much prompting (a short one-shot prompt would do).

Due to this, the eval metric is now based on the "study mode" function of this website (Algo Buddy). To summarize the new metric:
```
effectiveness = (# of questions in study mode's quiz function whose topics are correctly classified / # of topics about the algorithm discussed in study mode before hitting the quiz button)
```
\* single question per topic

This is a better metric because it more closely measures whether or not the AI assistant is doing its job correctly to help the user memorize information about the algorithm.

## What and why

The app is an AI assistant that helps you prepare for technical interviews by helping you learn common algorithms. The app's target audience are people hunting for jobs in Computer Science where sufficient recall of algorithmic choices are important.

The difficult part about getting the AI right is verifying that the code generated for a particular algorithm is correct and helpful. This requires manual analysis, and writing test cases for every common algorithm is infeasible in a week.

## Iterations

### V1: Initial website
The initial website was built by first writing a plan (under the plan directory, which initially included 'start.md', 'modes/quiz.md', and 'study.md'), and instructing the Kiro CLI coding assistant to implement the website described in the plan files.

The initial website (with the quiz and study modes) works as expected, even if there were a few UI/UX issues.

## AI Disclosure

My AI coding assistant, Kiro, was used to implement the website listed in the plan files (in the 'plan' directory) as well as implement the eval metric.

### Moments Kiro failed
- When trying to implement the eval metric, Kiro tried to implement the effectiveness metric as a measure of how well the user memorized information. This was corrected by interrupting Kiro and telling it "Please make it clear that 'study effectiveness' refers to how well the app is helping the user learn.'"
