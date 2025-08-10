
def my_generator():
    print("1. Function starts - setting up resources")
    resource = "Database Connection"
    
    try:
        print("2. About to yield the resource")
        yield resource  # PAUSE HERE - give control back to caller
        print("5. Generator resumed after caller finished")
    finally:
        print("6. Finally block runs - cleaning up resources")
        print("7. Resource cleaned up!")

# Using the generator
print("=== Starting demo ===")

# Create the generator (doesn't run the function yet!)
gen = my_generator()

print("3. Generator created, now getting the resource...")

# This triggers the function to run until yield
resource = next(gen)
print(f"4. Got resource: {resource}")

print("   [Doing some work with the resource...]")
print("   [Work completed, now finishing...]")

# This triggers the rest of the function (finally block)
try:
    next(gen)  # This will raise StopIteration
except StopIteration:
    print("8. Generator finished")

print("=== Demo complete ===")

print("\n" + "="*50)
print("FASTAPI EQUIVALENT:")
print("="*50)

# This simulates what FastAPI does with dependencies
def simulate_fastapi():
    print("\n🌐 FastAPI request comes in...")
    
    # FastAPI calls the dependency
    db_gen = my_generator()
    
    # Get the resource (runs until yield)
    db = next(db_gen)
    
    print("🔧 API endpoint runs with the resource...")
    print(f"   Using: {db}")
    print("✅ API endpoint finished")
    
    # FastAPI cleans up (runs finally block)
    try:
        next(db_gen)
    except StopIteration:
        pass
    
    print("📤 Response sent to client")

simulate_fastapi()