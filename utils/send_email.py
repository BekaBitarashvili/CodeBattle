from flask_mail import Message
from extensions import mail
from flask import render_template_string


VERIFY_TEMPLATE = """
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f1117;font-family:'Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:40px 20px">
  <tr><td align="center">
    <table width="560" cellpadding="0" cellspacing="0" style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:20px;overflow:hidden">
      <!-- Header -->
      <tr><td style="background:linear-gradient(135deg,#ff5722,#ff8c42);padding:32px 40px;text-align:center">
        <h1 style="margin:0;color:#fff;font-size:28px;font-weight:900;letter-spacing:-0.5px">🚀 CodeQuest</h1>
        <p style="margin:8px 0 0;color:rgba(255,255,255,0.85);font-size:14px">ქართული კოდინგის პლატფორმა</p>
      </td></tr>
      <!-- Body -->
      <tr><td style="padding:40px">
        <h2 style="color:#fff;font-size:22px;font-weight:800;margin:0 0 12px">გამარჯობა, {{ username }}! 👋</h2>
        <p style="color:#8b8fa8;font-size:15px;line-height:1.7;margin:0 0 28px">
          გმადლობთ CodeQuest-ზე რეგისტრაციისთვის! ანგარიშის გასააქტიურებლად გთხოვთ დაადასტუროთ თქვენი ელ-ფოსტის მისამართი.
        </p>
        <table cellpadding="0" cellspacing="0" style="margin:0 auto 28px">
          <tr><td style="background:#ff5722;border-radius:12px;text-align:center">
            <a href="{{ verify_url }}" style="display:inline-block;padding:16px 40px;color:#fff;text-decoration:none;font-size:16px;font-weight:800;letter-spacing:0.3px">
              ✅ ელ-ფოსტის დადასტურება
            </a>
          </td></tr>
        </table>
        <p style="color:#5a5d70;font-size:13px;line-height:1.6;margin:0">
          ეს ლინკი მოქმედია <strong style="color:#8b8fa8">1 საათის</strong> განმავლობაში.<br>
          თუ ეს თქვენ არ გახართ, უგულებელყავით ეს წერილი.
        </p>
      </td></tr>
      <!-- Footer -->
      <tr><td style="padding:20px 40px;border-top:1px solid #2a2d3a;text-align:center">
        <p style="color:#3a3d50;font-size:12px;margin:0">© 2026 CodeQuest · bekabitarashvili@gmail.com</p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>
"""

RESET_TEMPLATE = """
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f1117;font-family:'Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:40px 20px">
  <tr><td align="center">
    <table width="560" cellpadding="0" cellspacing="0" style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:20px;overflow:hidden">
      <tr><td style="background:linear-gradient(135deg,#ff5722,#ff8c42);padding:32px 40px;text-align:center">
        <h1 style="margin:0;color:#fff;font-size:28px;font-weight:900">🔐 CodeQuest</h1>
        <p style="margin:8px 0 0;color:rgba(255,255,255,0.85);font-size:14px">პაროლის აღდგენა</p>
      </td></tr>
      <tr><td style="padding:40px">
        <h2 style="color:#fff;font-size:22px;font-weight:800;margin:0 0 12px">გამარჯობა, {{ username }}! 🔑</h2>
        <p style="color:#8b8fa8;font-size:15px;line-height:1.7;margin:0 0 28px">
          მოვიდა პაროლის აღდგენის მოთხოვნა. ქვემოთ მოცემულ ღილაკზე დაჭერით შეძლებთ ახალი პაროლის დაყენებას.
        </p>
        <table cellpadding="0" cellspacing="0" style="margin:0 auto 28px">
          <tr><td style="background:#ff5722;border-radius:12px;text-align:center">
            <a href="{{ reset_url }}" style="display:inline-block;padding:16px 40px;color:#fff;text-decoration:none;font-size:16px;font-weight:800">
              🔓 პაროლის შეცვლა
            </a>
          </td></tr>
        </table>
        <p style="color:#5a5d70;font-size:13px;line-height:1.6;margin:0">
          ეს ლინკი მოქმედია <strong style="color:#8b8fa8">1 საათის</strong> განმავლობაში.<br>
          თუ ეს მოთხოვნა თქვენი არ არის, უგულებელყავით ეს წერილი — პაროლი არ შეიცვლება.
        </p>
      </td></tr>
      <tr><td style="padding:20px 40px;border-top:1px solid #2a2d3a;text-align:center">
        <p style="color:#3a3d50;font-size:12px;margin:0">© 2026 CodeQuest · bekabitarashvili@gmail.com</p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>
"""


def send_verification_email(user_email, username, verify_url):
    html = render_template_string(VERIFY_TEMPLATE, username=username, verify_url=verify_url)
    msg = Message(
        subject="✅ CodeMama — ელ-ფოსტის დადასტურება",
        recipients=[user_email],
        html=html
    )
    mail.send(msg)


def send_reset_email(user_email, username, reset_url):
    html = render_template_string(RESET_TEMPLATE, username=username, reset_url=reset_url)
    msg = Message(
        subject="🔐 CodeMama — პაროლის აღდგენა",
        recipients=[user_email],
        html=html
    )
    mail.send(msg)