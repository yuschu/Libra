with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update playPause to use granularity config
old_playPause = """    function playPause() {
      isPlaying = !isPlaying;
      const btn = document.getElementById("btnPlayPause");
      btn.textContent = isPlaying ? "⏸" : "▶";
      
      if (isPlaying) {
        const config = GRANULARITY_CONFIG[timeGranularity];
        const maxFrames = config.framesPerHour * 24 * 7; // 7 days
        playTimer = setInterval(() => {
          currentFrame = (currentFrame + 1) % maxFrames;
          updateFrame(currentFrame);
        }, 500 / playbackSpeed);
      } else {
        clearInterval(playTimer);
      }
    }"""

new_playPause = """    function playPause() {
      isPlaying = !isPlaying;
      const btn = document.getElementById("btnPlayPause");
      btn.textContent = isPlaying ? "⏸" : "▶";
      
      if (isPlaying) {
        const config = GRANULARITY_CONFIG[timeGranularity];
        const maxFrames = config.framesPerHour * 24 * 7;
        playTimer = setInterval(() => {
          currentFrame = (currentFrame + 1) % maxFrames;
          updateFrame(currentFrame);
        }, 500 / playbackSpeed);
      } else {
        clearInterval(playTimer);
      }
    }"""

content = content.replace(old_playPause, new_playPause)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated playPause (already correct)")
