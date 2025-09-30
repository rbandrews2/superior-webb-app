def button_email(title: str, intro: str, button_text: str, button_href: str, footer: str = "") -> str:
return f"""
<div style=\"font-family:system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; line-height:1.5; color:#0f172a\">
<h2 style=\"margin:0 0 8px\">{title}</h2>
<p style=\"margin:0 0 16px; color:#334155\">{intro}</p>
<p>
<a href=\"{button_href}\" style=\"
display:inline-block; padding:12px 18px; border-radius:10px;
background:#10b981; color:#fff; text-decoration:none; font-weight:600;\">
{button_text}
</a>
</p>
<p style=\"margin:16px 0 0; color:#64748b\">{footer}</p>
</div>
"""