"""
Piston API integration for code execution.
https://github.com/engineer-man/piston

No API key needed. No registration. Completely free.
Supports Python, Java, JavaScript, C++ and 70+ languages.
"""
import requests

# Piston language runtime names
LANG_RUNTIME = {
    "python":     ("python",      "3.10.0"),
    "python3":    ("python",      "3.10.0"),
    "java":       ("java",        "15.0.2"),
    "javascript": ("javascript",  "18.15.0"),
    "js":         ("javascript",  "18.15.0"),
    "cpp":        ("c++",         "10.2.0"),
    "c++":        ("c++",         "10.2.0"),
}

PISTON_URL = "https://emkc.org/api/v2/piston/execute"


def _run(source_code: str, language: str, stdin: str, time_limit: float = 2.0) -> dict:
    """Execute code via Piston API. Returns normalized result dict."""
    runtime, version = LANG_RUNTIME.get(language.lower(), ("python", "3.10.0"))

    payload = {
        "language": runtime,
        "version":  version,
        "files": [{"content": source_code}],
        "stdin":    stdin,
        "run_timeout": int(time_limit * 1000),  # ms
    }

    try:
        r = requests.post(PISTON_URL, json=payload, timeout=15)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.Timeout:
        return {"status": "time_limit_exceeded", "stdout": "", "stderr": "Timeout", "runtime_ms": 0}
    except Exception as e:
        return {"status": "error", "stdout": "", "stderr": str(e), "runtime_ms": 0}

    run    = data.get("run",     {})
    compile_ = data.get("compile", {})

    # Compilation error (Java / C++)
    if compile_ and compile_.get("code", 0) != 0:
        return {
            "status":         "compilation_error",
            "stdout":         "",
            "stderr":         compile_.get("output", ""),
            "compile_output": compile_.get("output", ""),
            "runtime_ms":     0,
        }

    stdout   = (run.get("stdout") or "").strip()
    stderr   = (run.get("stderr") or "").strip()
    exit_code = run.get("code", 0)

    # TLE — Piston signals this via signal
    if run.get("signal") == "SIGKILL":
        return {"status": "time_limit_exceeded", "stdout": stdout, "stderr": stderr, "runtime_ms": 0}

    # Runtime error
    if exit_code != 0:
        return {"status": "runtime_error", "stdout": stdout, "stderr": stderr, "runtime_ms": 0}

    return {
        "status":         "accepted",
        "stdout":         stdout,
        "stderr":         stderr,
        "compile_output": "",
        "runtime_ms":     0,   # Piston doesn't return timing
    }


def judge_task(source_code: str, language: str, task) -> dict:
    """
    Run code against all test cases for a task.
    Returns: { ok, status, passed, total, runtime_ms, error_message, first_fail }
    """
    test_cases = task.get_test_cases()

    if not test_cases:
        result = _run(source_code, language, "", task.time_limit)
        ok = result["status"] == "accepted"
        return {
            "ok": ok, "status": result["status"],
            "passed": 1 if ok else 0, "total": 1,
            "runtime_ms": 0,
            "error_message": result.get("stderr") or result.get("compile_output", ""),
            "first_fail": None,
        }

    passed     = 0
    first_fail = None

    for i, tc in enumerate(test_cases):
        expected = tc.get("output", "").strip()
        stdin    = tc.get("input", "")

        result = _run(source_code, language, stdin, task.time_limit)

        # Compilation error — stop immediately
        if result["status"] == "compilation_error":
            return {
                "ok": False, "status": "compilation_error",
                "passed": 0, "total": len(test_cases),
                "runtime_ms": 0,
                "error_message": result.get("compile_output") or result.get("stderr", ""),
                "first_fail": None,
            }

        # TLE / Runtime error — stop immediately
        if result["status"] not in ("accepted",):
            return {
                "ok": False, "status": result["status"],
                "passed": passed, "total": len(test_cases),
                "runtime_ms": 0,
                "error_message": result.get("stderr", ""),
                "first_fail": {
                    "input":    stdin if not tc.get("hidden") else "🔒 დამალული ტესტი",
                    "expected": expected if not tc.get("hidden") else "🔒",
                    "got":      result["stdout"],
                    "test_num": i + 1,
                },
            }

        got = result["stdout"].strip()

        if got == expected:
            passed += 1
        else:
            # Wrong answer
            if not tc.get("hidden"):
                first_fail = {
                    "input":    stdin,
                    "expected": expected,
                    "got":      got,
                    "test_num": i + 1,
                }
            else:
                first_fail = {
                    "input":    "🔒 დამალული ტესტი",
                    "expected": "🔒",
                    "got":      got,
                    "test_num": i + 1,
                }
            return {
                "ok": False, "status": "wrong_answer",
                "passed": passed, "total": len(test_cases),
                "runtime_ms": 0,
                "error_message": "",
                "first_fail": first_fail,
            }

    # All tests passed
    return {
        "ok": True, "status": "accepted",
        "passed": passed, "total": len(test_cases),
        "runtime_ms": 0,
        "error_message": "",
        "first_fail": None,
    }