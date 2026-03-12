"""
Code Judge using Judge0 CE public API.
Docs: https://ce.judge0.com
No API key required for basic usage.
"""
import time
import base64
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Judge0 CE language IDs
LANGUAGE_IDS = {
    "python":     71,   # Python 3.8.1
    "javascript": 63,   # JavaScript (Node.js 12.14.0)
    "cpp":        54,   # C++ (GCC 9.2.0)
    "java":       62,   # Java (OpenJDK 13.0.1)
}

JUDGE0_URL = "https://ce.judge0.com"


def _b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def _decode(s) -> str:
    if not s:
        return ""
    try:
        return base64.b64decode(s).decode("utf-8", errors="replace").strip()
    except Exception:
        return str(s).strip()


def _run(source_code: str, language: str, stdin: str, time_limit: float = 2.0) -> dict:
    """
    Submit to Judge0, poll until done, return normalized result dict.
    """
    lang_id = LANGUAGE_IDS.get(language.lower(), 71)

    payload = {
        "source_code":     _b64(source_code),
        "language_id":     lang_id,
        "stdin":           _b64(stdin),
        "cpu_time_limit":  time_limit,
        "wall_time_limit": time_limit + 2,
        "base64_encoded":  True,
    }

    headers = {"Content-Type": "application/json"}

    # ── Submit ────────────────────────────────────
    try:
        r = requests.post(
            f"{JUDGE0_URL}/submissions?base64_encoded=true&wait=false",
            json=payload,
            headers=headers,
            timeout=15,
            verify=False,
        )
        r.raise_for_status()
        token = r.json().get("token")
        if not token:
            return _err("No token from Judge0")
    except Exception as e:
        return _err(str(e))

    # ── Poll ──────────────────────────────────────
    for _ in range(20):
        time.sleep(0.8)
        try:
            poll = requests.get(
                f"{JUDGE0_URL}/submissions/{token}?base64_encoded=true",
                headers=headers,
                timeout=10,
                verify=False,
            )
            poll.raise_for_status()
            data = poll.json()
        except Exception as e:
            return _err(str(e))

        status_id = data.get("status", {}).get("id", 0)

        # Still processing (1=In Queue, 2=Processing)
        if status_id in (1, 2):
            continue

        stdout          = _decode(data.get("stdout"))
        stderr          = _decode(data.get("stderr"))
        compile_output  = _decode(data.get("compile_output"))
        time_used       = data.get("time")
        runtime_ms      = int(float(time_used) * 1000) if time_used else 0

        # 3 = Accepted
        if status_id == 3:
            return {"status": "accepted", "stdout": stdout, "stderr": stderr,
                    "compile_output": "", "runtime_ms": runtime_ms}

        # 4 = Wrong Answer (Judge0 only gets this if expected_output was sent)
        if status_id == 4:
            return {"status": "accepted", "stdout": stdout, "stderr": stderr,
                    "compile_output": "", "runtime_ms": runtime_ms}

        # 5 = Time Limit Exceeded
        if status_id == 5:
            return {"status": "time_limit_exceeded", "stdout": stdout,
                    "stderr": stderr, "compile_output": "", "runtime_ms": runtime_ms}

        # 6 = Compilation Error
        if status_id == 6:
            return {"status": "compilation_error", "stdout": "",
                    "stderr": compile_output or stderr,
                    "compile_output": compile_output, "runtime_ms": 0}

        # 7-12 = Runtime errors
        if 7 <= status_id <= 12:
            return {"status": "runtime_error", "stdout": stdout,
                    "stderr": stderr or compile_output,
                    "compile_output": "", "runtime_ms": runtime_ms}

        # Other
        return {"status": "error", "stdout": stdout, "stderr": stderr,
                "compile_output": "", "runtime_ms": runtime_ms}

    return _err("Polling timeout — Judge0 did not respond in time")


def _err(msg: str) -> dict:
    return {"status": "error", "stdout": "", "stderr": msg,
            "compile_output": "", "runtime_ms": 0}


def judge_task(source_code: str, language: str, task) -> dict:
    """
    Run source_code against all test cases of task.
    Returns:
      ok, status, passed, total, runtime_ms, error_message, first_fail
    """
    test_cases = task.get_test_cases()
    if not test_cases:
        return {
            "ok": False, "status": "error",
            "passed": 0, "total": 0,
            "runtime_ms": 0,
            "error_message": "ამოცანას test case-ები არ აქვს.",
            "first_fail": None,
        }

    passed     = 0
    total      = len(test_cases)
    first_fail = None
    max_ms     = 0

    for i, tc in enumerate(test_cases, 1):
        stdin    = tc.get("input", "")
        expected = tc.get("output", "").strip()
        hidden   = tc.get("hidden", False)

        result = _run(source_code, language, stdin, task.time_limit or 2.0)
        max_ms = max(max_ms, result.get("runtime_ms", 0))

        status = result["status"]

        if status == "compilation_error":
            err = result.get("compile_output") or result.get("stderr", "")
            return {
                "ok": False, "status": "compilation_error",
                "passed": 0, "total": total,
                "runtime_ms": 0,
                "error_message": err[:500],
                "first_fail": None,
            }

        if status in ("error", "runtime_error"):
            err = result.get("stderr", "") or result.get("compile_output", "")
            if not first_fail:
                first_fail = {
                    "test_num": i,
                    "input":    "🔒" if hidden else stdin,
                    "expected": "🔒" if hidden else expected,
                    "got":      result["stdout"] or "",
                }
            return {
                "ok": False, "status": status,
                "passed": passed, "total": total,
                "runtime_ms": max_ms,
                "error_message": err[:500],
                "first_fail": first_fail,
            }

        if status == "time_limit_exceeded":
            if not first_fail:
                first_fail = {
                    "test_num": i,
                    "input":    "🔒" if hidden else stdin,
                    "expected": "🔒" if hidden else expected,
                    "got":      "⏱ Time Limit Exceeded",
                }
            return {
                "ok": False, "status": "time_limit_exceeded",
                "passed": passed, "total": total,
                "runtime_ms": max_ms,
                "error_message": "კოდი ძალიან ნელა სრულდება.",
                "first_fail": first_fail,
            }

        # Compare output
        got = result["stdout"].strip()
        if got == expected:
            passed += 1
        else:
            if not first_fail:
                first_fail = {
                    "test_num": i,
                    "input":    "🔒" if hidden else stdin,
                    "expected": "🔒" if hidden else expected,
                    "got":      got,
                }

    if passed == total:
        return {
            "ok": True, "status": "accepted",
            "passed": passed, "total": total,
            "runtime_ms": max_ms,
            "error_message": "",
            "first_fail": None,
        }
    else:
        return {
            "ok": False, "status": "wrong_answer",
            "passed": passed, "total": total,
            "runtime_ms": max_ms,
            "error_message": "",
            "first_fail": first_fail,
        }