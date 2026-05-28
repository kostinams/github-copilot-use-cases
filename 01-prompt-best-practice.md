# Prompt Best Practices

## 1. Be specific

**Vague:** `# Write some code for grades.py`

**Better:** `# Implement a function in grades.py to calculate the average grade`

**Even better:** `# Implement the function calculate_average_grade in grades.py that takes a list of grades as input and returns the average grade as a floating-point number`

## 2. Avoid ambiguity

Don't ask "what does this do" if "this" could be the current file, the last Copilot response, or a specific code block.
Instead, be specific:

`- What does the createUser function do?`

`- What does the code in your last response do?`

Ambiguity can also apply to libraries:

- If you are using an uncommon library, describe what the library does.
- If you want to use a specific library, set the import statements at the top of the file or specify what library you want to use.


## 3. Give GitHub Copilot an example or two ✍️

Use examples to help Copilot understand what you want. You can provide example input data, example outputs, and example implementations.

### Example: Providing input/output specifications

**Copilot Chat prompt:**

> Write a Go function that finds all dates in a string and returns them in an array. Dates can be formatted like:
> 
> * 05/02/24
> * 05/02/2024
> * 5/2/24
> * 5/2/2024
> * 05-02-24
> * 05-02-2024
> * 5-2-24
> * 5-2-2024
> 
> Example:
> findDates("I have a dentist appointment on 11/14/2023 and book club on 12-1-23")
> // Returns: ["11/14/2023", "12-1-23"]


**Tip:** Unit tests can also serve as examples. Before writing your function, you can use Copilot to write unit tests for the function. Then, you can ask Copilot to write a function described by those unit tests.

## 4. Reusable prompts
.github/prompts

## 5. Awesome Copilot

## 6. Custom chatmodes

## 7. Break complex tasks into simpler tasks
If you want Copilot to complete a complex or large task, break the task into multiple simple, small tasks.

For example, instead of asking Copilot to generate a word search puzzle, break the process down into smaller tasks, and ask Copilot to accomplish them one by one:

**Copilot Chat prompt:**

> - Write a function to generate a 10 by 10 grid of letters.
> - Write a function to find all words in a grid of letters, given a list of valid words.
> - Write a function that uses the previous functions to generate a 10 by 10 grid of letters that contains at least 10 words.
> - Update the previous function to print the grid of letters and 10 random words from the grid.

