"""
Email sending via Resend API.
https://resend.com — free 3000 emails/month, no SMTP ports needed.

Config (set in environment variables on Render):
  RESEND_API_KEY = re_xxxxxxxxxxxx
  MAIL_FROM      = onboarding@resend.dev   (ან შენი დომენი)
  MAIL_FROM_NAME = CodeMama
"""
import json
import urllib.request
import urllib.error
import requests as _requests
from flask import current_app


def _send(to_email: str, subject: str, html: str) -> tuple[bool, str]:
    api_key   = current_app.config.get("RESEND_API_KEY", "")
    from_addr = current_app.config.get("MAIL_FROM", "onboarding@resend.dev")
    from_name = current_app.config.get("MAIL_FROM_NAME", "CodeMama")

    if not api_key:
        print(f"\n[EMAIL - DEV MODE]\nTo: {to_email}\nSubject: {subject}\n(Set RESEND_API_KEY to send real emails)\n")
        return True, ""

    try:
        r = _requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type":  "application/json",
            },
            json={
                "from":    f"{from_name} <{from_addr}>",
                "to":      [to_email],
                "subject": subject,
                "html":    html,
            },
            timeout=10
        )
        if r.status_code in (200, 201):
            return True, ""
        print(f"[RESEND ERROR] {r.status_code}: {r.text}")
        return False, f"Resend {r.status_code}: {r.text}"
    except Exception as e:
        print(f"[RESEND ERROR] {e}")
        return False, str(e)


# ── HTML TEMPLATES ────────────────────────────────────────

_VERIFY_HTML = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f1117;font-family:'Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:40px 20px">
  <tr><td align="center">
    <table width="560" cellpadding="0" cellspacing="0"
           style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:20px;overflow:hidden">
      <tr><td style="background:linear-gradient(135deg,#ff5722,#ff8c42);padding:32px 40px;text-align:center">
        <h1 style="margin:0;color:#fff;font-size:26px;font-weight:900">🚀 CodeMama</h1>
        <p style="margin:6px 0 0;color:rgba(255,255,255,0.85);font-size:13px">ქართული კოდინგის პლატფორმა</p>
      </td></tr>
      <tr><td style="padding:36px 40px">
        <h2 style="color:#fff;font-size:20px;font-weight:800;margin:0 0 10px">გამარჯობა, {username}! 👋</h2>
        <p style="color:#8b8fa8;font-size:14px;line-height:1.7;margin:0 0 24px">
          გმადლობთ CodeMama-ზე რეგისტრაციისთვის!<br>
          ანგარიშის გასააქტიურებლად დაადასტურეთ ელ-ფოსტა:
        </p>
        <table cellpadding="0" cellspacing="0" style="margin:0 auto 24px">
          <tr><td style="background:#ff5722;border-radius:12px;text-align:center">
            <a href="{verify_url}"
               style="display:inline-block;padding:15px 38px;color:#fff;text-decoration:none;font-size:15px;font-weight:800">
              ✅ ელ-ფოსტის დადასტურება
            </a>
          </td></tr>
        </table>
        <p style="color:#5a5d70;font-size:12px;line-height:1.6;margin:0">
          ლინკი მოქმედია <strong style="color:#8b8fa8">1 საათის</strong> განმავლობაში.<br>
          თუ ეს თქვენ არ გახართ, უგულებელყავით ეს წერილი.
        </p>
      </td></tr>
      <tr><td style="padding:18px 40px;border-top:1px solid #2a2d3a;text-align:center">
        <p style="color:#3a3d50;font-size:11px;margin:0">© 2025 CodeMama</p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>"""

_RESET_HTML = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f1117;font-family:'Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:40px 20px">
  <tr><td align="center">
    <table width="560" cellpadding="0" cellspacing="0"
           style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:20px;overflow:hidden">
      <tr><td style="background:linear-gradient(135deg,#ff5722,#ff8c42);padding:32px 40px;text-align:center">
        <h1 style="margin:0;color:#fff;font-size:26px;font-weight:900">🔐 CodeMama</h1>
        <p style="margin:6px 0 0;color:rgba(255,255,255,0.85);font-size:13px">პაროლის აღდგენა</p>
      </td></tr>
      <tr><td style="padding:36px 40px">
        <h2 style="color:#fff;font-size:20px;font-weight:800;margin:0 0 10px">გამარჯობა, {username}! 🔑</h2>
        <p style="color:#8b8fa8;font-size:14px;line-height:1.7;margin:0 0 24px">
          მოვიდა პაროლის აღდგენის მოთხოვნა.<br>
          ქვემოთ მოცემულ ღილაკზე დაჭერით შეძლებთ ახალი პაროლის დაყენებას:
        </p>
        <table cellpadding="0" cellspacing="0" style="margin:0 auto 24px">
          <tr><td style="background:#ff5722;border-radius:12px;text-align:center">
            <a href="{reset_url}"
               style="display:inline-block;padding:15px 38px;color:#fff;text-decoration:none;font-size:15px;font-weight:800">
              🔓 პაროლის შეცვლა
            </a>
          </td></tr>
        </table>
        <p style="color:#5a5d70;font-size:12px;line-height:1.6;margin:0">
          ლინკი მოქმედია <strong style="color:#8b8fa8">1 საათის</strong> განმავლობაში.<br>
          თუ ეს მოთხოვნა თქვენი არ არის, უგულებელყავით — პაროლი არ შეიცვლება.
        </p>
      </td></tr>
      <tr><td style="padding:18px 40px;border-top:1px solid #2a2d3a;text-align:center">
        <p style="color:#3a3d50;font-size:11px;margin:0">© 2025 CodeMama</p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>"""


def send_verification_email(to_email: str, username: str, verify_url: str) -> tuple[bool, str]:
    html = _VERIFY_HTML.replace("{username}", username).replace("{verify_url}", verify_url)
    return _send(to_email, "✅ CodeMama — ელ-ფოსტის დადასტურება", html)


def send_reset_email(to_email: str, username: str, reset_url: str) -> tuple[bool, str]:
    html = _RESET_HTML.replace("{username}", username).replace("{reset_url}", reset_url)
    return _send(to_email, "🔐 CodeMama — პაროლის აღდგენა", html)