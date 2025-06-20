from markdown_it import MarkdownIt

def render_to_html(markdown_string, css_string=""):
    md = MarkdownIt()
    html_fragment = md.render(markdown_string)
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{css_string}
</style>
</head>
<body>
{html_fragment}
</body>
</html>"""
    return html