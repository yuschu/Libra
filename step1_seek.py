with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update seekFrame
old_seekFrame = """    function seekFrame(frame) {
      if (isPlaying) playPause();
      const config = GRANULARITY_CONFIG[timeGranularity];
      const maxFrames = config.framesPerHour * 24 * 7;
      currentFrame = Math.max(0, Math.min(frame, maxFrames - 1));
      updateFrame(currentFrame);
    }"""

new_seekFrame = """    function seekFrame(frame) {
      if (isPlaying) playPause();
      const config = GRANULARITY_CONFIG[timeGranularity];
      const maxFrames = config.framesPerHour * 24 * 7;
      currentFrame = Math.max(0, Math.min(frame, maxFrames - 1));
      updateFrame(currentFrame);
    }"""

content = content.replace(old_seekFrame, new_seekFrame)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated seekFrame (already correct)")
