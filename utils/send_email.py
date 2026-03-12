"""
Email sending via Gmail SMTP.
Config (set in .env or Render environment):
  MAIL_USERNAME = c0d3mama@gmail.com
  MAIL_PASSWORD = xxxx xxxx xxxx xxxx  (Gmail App Password)
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app


def _send(to_email: str, subject: str, html: str) -> tuple[bool, str]:
    gmail_user = current_app.config.get("MAIL_USERNAME", "")
    gmail_pass = current_app.config.get("MAIL_PASSWORD", "")

    if not gmail_user or not gmail_pass:
        print(f"\n[EMAIL - DEV MODE]\nTo: {to_email}\nSubject: {subject}\n")
        # HTML-იდან ლინკი ამოვიღოთ
        import re
        links = re.findall(r'href="(http[^"]+)"', html)
        for link in links:
            print(f"LINK: {link}")
        print()
        return True, ""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"CodeMama <{gmail_user}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(html, "html", "utf-8"))

    # Try SSL (port 465) first, fallback to STARTTLS (port 587)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(gmail_user, gmail_pass)
            smtp.sendmail(gmail_user, to_email, msg.as_string())
        return True, ""
    except Exception as e1:
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(gmail_user, gmail_pass)
                smtp.sendmail(gmail_user, to_email, msg.as_string())
            return True, ""
        except Exception as e2:
            print(f"[MAIL ERROR] SSL: {e1} | TLS: {e2}")
            return False, str(e2)


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
          ქვემოთ ღილაკზე დაჭერით შეძლებთ ახალი პაროლის დაყენებას:
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