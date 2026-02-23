"""
Python Executor Tool
Safely executes agent-generated Python/Matplotlib chart code in the venv.
Used exclusively by the Visual Designer Agent to render infographic PNGs.
"""
import os
import sys
import subprocess
import tempfile
from typing import Type
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class PythonExecutorInput(BaseModel):
    code: str = Field(
        description=(
            "Complete, runnable Python code that generates a matplotlib chart and saves it "
            "as a PNG file. Must include all imports. Must call plt.savefig() with the "
            "exact output path and plt.close() at the end. "
            "The code must print the output file path as its last stdout line."
        )
    )


class PythonExecutorTool(BaseTool):
    name: str = "Execute Chart Code"
    description: str = (
        "Executes Python/Matplotlib chart generation code and returns the result. "
        "Use this to render infographic PNG files from the chart code you write. "
        "The code MUST save the chart to a file and print the output path. "
        "Returns stdout output (including the saved file path) or error message."
    )
    args_schema: Type[BaseModel] = PythonExecutorInput

    def _run(self, code: str) -> str:
        # Write code to a temp file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            # Use the same venv Python so all packages are available
            python_exe = sys.executable

            result = subprocess.run(
                [python_exe, tmp_path],
                capture_output=True,
                text=True,
                timeout=60,
                env={**os.environ, "MPLBACKEND": "Agg"},  # Force non-interactive backend
            )

            if result.returncode != 0:
                return (
                    f"[CHART ERROR] Code execution failed.\n"
                    f"STDERR:\n{result.stderr[-2000:]}\n"
                    f"STDOUT:\n{result.stdout[-500:]}\n\n"
                    "Fix the code and try again."
                )

            stdout = result.stdout.strip()
            if not stdout:
                return "[CHART ERROR] Code ran but produced no output. Did you forget to print the output path?"

            return f"[CHART SUCCESS]\n{stdout}"

        except subprocess.TimeoutExpired:
            return "[CHART ERROR] Code timed out after 60 seconds. Simplify the chart."
        except Exception as e:
            return f"[CHART ERROR] Unexpected error: {str(e)}"
        finally:
            Path(tmp_path).unlink(missing_ok=True)
