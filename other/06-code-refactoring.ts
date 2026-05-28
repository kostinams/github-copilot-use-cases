// The code below is a simple function that compares three numbers 
// and returns the sum of the positive ones.

/**
 * Calculates the sum of positive numbers from the provided inputs.
 * 
 * This function validates input by only summing numbers greater than zero,
 * protecting against potential issues with negative values or zero.
 * 
 * @param a - The first number to evaluate
 * @param b - The second number to evaluate
 * @param c - The third number to evaluate
 * @returns The sum of all positive numbers, or 0 if none are positive
 */
function sumPositiveNumbers(a: number, b: number, c: number): number {
    return [a, b, c]
        .filter(num => num > 0)
        .reduce((sum, num) => sum + num, 0);
}

// Prompt in Ask: Refactor the code to make it more readable and effective.