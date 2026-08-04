def add(a, b):
    return a + b
 
def subtract(a, b):
    return a - b
 
def multiply(a, b):
    return a * b
 
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
 
def calculator():
    print("Simple Calculator")
    print("Operations: add, subtract, multiply, divide")
 
    while True:
        operation = input("\nEnter operation (or 'quit' to exit): ").strip().lower()
        if operation == "quit":
            print("Exiting calculator.")
            break
        if operation not in ("add", "subtract", "multiply", "divide"):
            print("Invalid operation. Try again.")
            continue
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue
 
        try:
            if operation == "add":
                result = add(a, b)
            elif operation == "subtract":
                result = subtract(a, b)
            elif operation == "multiply":
                result = multiply(a, b)
            elif operation == "divide":
                result = divide(a, b)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
 
if __name__ == "__main__":
    calculator()
 
