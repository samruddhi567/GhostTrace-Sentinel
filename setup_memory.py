import chromadb

# 1. Initialize the Persistent Client (Saves data to a folder)
client = chromadb.PersistentClient(path="./ghosttrace_db")

# 2. Create a 'Collection' (Think of it as a table for Rules)
collection = client.get_or_create_collection(name="business_rules")

# 3. Define the Business Rules for GhostTrace: Sentinel
# These rules are what the 'Judge' will check the code against
rules = [
    "The Payment button must be blue and labeled 'Pay Now'.",
    "Cardholder Name field must be a required text input.",
    "The Card Number field must mask digits for security (e.g., **** 1234).",
    "The Expiry Date must follow the format MM/YY.",
    "A checkbox for 'Save for future payments' must be present.",
    "Total balance must be displayed in black text, unless overdue (then red)."
]

# 4. Add rules to the database with unique IDs
collection.add(
    documents=rules,
    ids=[f"rule_{i}" for i in range(len(rules))]
)

print("✅ SUCCESS: Member 2 has initialized the Business Logic Memory.")
print(f"Stored {collection.count()} rules in ./ghosttrace_db")