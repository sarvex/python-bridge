from typing import Dict, Any, List

def generate_metadata_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms raw scan data into a standardized metadata format (descriptor).
    """
    if item["type"] == "function":
        return {
            "componentType": "FunctionBlock",
            "name": item["name"],
            "docstring": item.get("docstring", ""),
            "arguments": item.get("args", []),
        }
    elif item["type"] == "class":
        # Each class might become a single block or multiple blocks for each method
        methods_meta = []
        for method in item.get("methods", []):
            methods_meta.append({
                "componentType": "MethodBlock",
                "className": item["name"],
                "methodName": method["name"],
                "docstring": method.get("docstring", ""),
                "arguments": method.get("args", []),
            })
        return {
            "componentType": "ClassBlock",
            "name": item["name"],
            "docstring": item.get("docstring", ""),
            "methods": methods_meta
        }
    return {}

def generate_full_metadata(scan_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts a list of scan items into a list of metadata descriptors.
    """
    metadata_list = []
    for item in scan_results:
        metadata_list.append(generate_metadata_item(item))
    return metadata_list
