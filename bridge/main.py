from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os

from bridge.core.scanning import scan_directory
from bridge.core.metadata import generate_full_metadata
from bridge.connectors.mobius import MobiusConnector

app = FastAPI(title="Bridge", version="0.1.0")

class ScanRequest(BaseModel):
    path: str
    mobius_url: str
    api_key: str = ""

@app.post("/scan-and-publish")
def scan_and_publish(req: ScanRequest) -> Dict[str, Any]:
    """
    Endpoint to scan a directory, generate metadata, and publish it to Mobius.
    """
    if not os.path.exists(req.path):
        raise HTTPException(status_code=400, detail="Invalid path or path does not exist")

    # 1. Scan directory
    scan_results = scan_directory(req.path)
    if not scan_results:
        return {"status": "No Python files or valid code found."}

    # 2. Generate metadata
    metadata = generate_full_metadata(scan_results)

    # 3. Publish to Mobius
    connector = MobiusConnector(base_url=req.mobius_url, api_key=req.api_key)
    success = connector.publish_metadata(metadata)

    if success:
        return {"status": "Published successfully", "itemsPublished": len(metadata)}
    else:
        raise HTTPException(status_code=500, detail="Failed to publish to Mobius.")
