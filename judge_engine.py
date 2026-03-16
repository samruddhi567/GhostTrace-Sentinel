import sys
import json
import os
import subprocess
from ollama import Client 

def get_staged_code():
    """Extracts Vector 3 (Code) from the Git staging area."""
    try:
        # IPC: Using Shell commands to get staged changes
        result = subprocess.check_output(['git', 'diff', '--cached'], stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except Exception:
        return None

def alignment_judge():
    # 1. INGESTION: Load Requirements (Vector 1) and Design (Vector 2)
    if not os.path.exists("current_context.json"):
        print("[ERROR] No Governance Context found. Please sync via Dashboard.")
        sys.exit(1)

    with open("current_context.json", "r") as f:
        context = json.load(f)
        requirement = context.get("requirement")
        design_spec = context.get("design_spec") # Corrected: Matches server.py key
        design_file = context.get("image_path")

    # 2. INTERCEPTION: Pull Vector 3 (The Code)
    code_to_check = get_staged_code()
    if not code_to_check:
        print("[SKIP] No code changes detected in staging area.")
        sys.exit(0)

    # 3. CROSS-VALIDATION: The Judicial Logic
    judicial_prompt = f"""
    You are the GhostTrace Sentinel. Audit for TRIPLE-POINT ALIGNMENT:
    
    VECTOR 1 (Business): "{requirement}"
    VECTOR 2 (Architectural Design): "{design_spec}"
    VECTOR 2 (Visual Reference): "{design_file}"
    VECTOR 3 (Developer's Code):
    ---
    {code_to_check}
    ---
    
    AUDIT TASK:
    Compare Vector 3 against Vector 1 and 2. Is there a semantic gap?
    
    RESPONSE FORMAT:
    If aligned, start with 'STATUS: SUCCESS'.
    If misaligned, start with 'STATUS: FAILED' and list the alignment gaps.
    """

    try:
        # Inference via Llama 3.2
        client = Client(host='http://127.0.0.1:11434')
        response = client.generate(model='llama3.2', prompt=judicial_prompt)
        verdict = response['response']

        # 4. SIGNAL TRANSMISSION (IPC)
        # We check for 'SUCCESS' to match the frontend logic
        if "STATUS: SUCCESS" in verdict.upper():
            print("\n✅ ALIGNMENT VERIFIED: Integrity check passed.")
            with open("latest_report.json", "w") as rf:
                json.dump({"status": "SUCCESS", "message": verdict}, rf)
            sys.exit(0) # Signal: ALLOW
        else:
            print("\n❌ ALIGNMENT FAILED: Commit Blocked.")
            with open("latest_report.json", "w") as rf:
                json.dump({"status": "FAILED", "message": verdict}, rf)
            sys.exit(1) # Signal: BLOCK

    except Exception as e:
        print(f"[SYSTEM ERROR] Engine Offline: {e}")
        sys.exit(1) 

if __name__ == "__main__":
    alignment_judge()