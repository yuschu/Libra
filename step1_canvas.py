with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the globe panel div - keep the same id but it will be a canvas
old_globe_div = """      <!-- Globe Panel -->
      <div class="globe-panel">
        <div id="globe"></div>
      </div>"""

new_globe_div = """      <!-- Globe Panel -->
      <div class="globe-panel">
        <canvas id="globe"></canvas>
      </div>"""

content = content.replace(old_globe_div, new_globe_div)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced globe div with canvas")
