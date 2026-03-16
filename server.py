from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os, json, shutil, uvicorn

app = FastAPI()

# Fix for "Server Offline" errors & Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_ui():
    """Serves the Governance Dashboard."""
    return FileResponse("index.html")

@app.post("/api/sync")
async def sync_governance_vectors(
    requirements: str = Form(...), 
    design_spec: str = Form(...), # New: Added explicit Design Pattern Vector
    design_image: UploadFile = File(...)
):
    """
    TRIPLE-VECTOR SYNC:
    Saves the Requirement and Design Specs to act as the 
    'Ground Truth' for the Judge Engine.
    """
    # 1. Save the Visual Design Vector
    img_path = f"active_design{os.path.splitext(design_image.filename)[1]}"
    with open(img_path, "wb") as buffer:
        shutil.copyfileobj(design_image.file, buffer)
    
    # 2. Create the Shared Memory (Context) for IPC
    context_data = {
        "requirement": requirements,  # Vector 1
        "design_spec": design_spec,    # Vector 2
        "image_path": img_path
    }
    
    with open("current_context.json", "w") as f:
        json.dump(context_data, f, indent=4)
        
    return {"status": "GOVERNANCE VECTORS SYNCED", "context": context_data}

@app.get("/api/report")
async def get_alignment_report():
    """Fetches the latest verdict from the Judicial Engine."""
    if os.path.exists("latest_report.json"):
        with open("latest_report.json", "r") as f:
            return json.load(f)
    return {"status": "AWAITING COMMIT", "message": "Sentinel is standing by..."}

if __name__ == "__main__":
    print("🚀 GhostTrace Sentinel Command Center Running on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)