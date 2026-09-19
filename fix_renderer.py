with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("{ renderer: \"canvas\" }", "{ renderer: \"webgl\" }")

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed renderer to webgl")
