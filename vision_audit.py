import ollama
import os

# 1. SETUP: Path to your sketch image
# Use r"" to prevent Windows backslash errors
IMAGE_PATH = r"C:\Users\samru\Desktop\GhostTrace\ui_sketch.png"

def run_vision_audit(image_path):
    # 2. FILE CHECK: Ensure the image is actually there
    if not os.path.exists(image_path):
        print(f"❌ ERROR: File not found at {image_path}")
        return

    print(f"🔍 GhostTrace: Sentinel - Starting Vision Audit...")
    print(f"🖼️ Analyzing: {os.path.basename(image_path)}")

    # 3. PROMPT: Instructing the AI on Business Logic extraction
    prompt = """
    Identify all UI components in this payment checkout sketch. 
    Return a clean JSON array of objects. 
    Each object must have:
    - 'type': (e.g., button, input_field, header)
    - 'label': (the text visible on or near the component)
    """

    try:
        # 4. EXECUTION: Using Moondream for low-memory efficiency
        response = ollama.chat(
            model='moondream',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }]
        )
        
        # 5. OUTPUT: Display the extracted logic
        print("\n✅ ANALYSIS COMPLETE")
        print("--- EXTRACTED DESIGN SCHEMA ---")
        print(response['message']['content'])
        
    except Exception as e:
        print(f"⚠️ SYSTEM ERROR: {str(e)}")

if __name__ == "__main__":
    run_vision_audit(IMAGE_PATH)