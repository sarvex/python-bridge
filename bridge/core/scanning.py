import ast
import os
from typing import List, Dict, Any

def scan_python_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Scans a single Python file, extracting metadata about functions and classes.

    Returns:
        A list of dictionaries containing basic info (type, name, docstring, arguments).
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        # In case of syntax errors, we skip or return an empty list.
        return []

    result = []

    for node in ast.walk(tree):
        # Extract function definitions
        if isinstance(node, ast.FunctionDef):
            func_info = {
                "type": "function",
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "args": [arg.arg for arg in node.args.args],
            }
            result.append(func_info)

        # Extract class definitions
        elif isinstance(node, ast.ClassDef):
            class_info = {
                "type": "class",
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "methods": []
            }
            # Within the class, gather methods
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    method_info = {
                        "name": body_item.name,
                        "docstring": ast.get_docstring(body_item),
                        "args": [arg.arg for arg in body_item.args.args],
                    }
                    class_info["methods"].append(method_info)
            result.append(class_info)

    return result

def scan_directory(directory_path: str) -> List[Dict[str, Any]]:
    """
    Recursively scans a directory for Python files, aggregating metadata.
    """
    aggregated_results = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_results = scan_python_file(file_path)
                aggregated_results.extend(file_results)
    return aggregated_results
