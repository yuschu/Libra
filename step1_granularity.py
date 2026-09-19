with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update the granularity selector event handler
old_granularity = """      // Initialize granularity selector
      document.getElementById("granularitySelect").addEventListener("change", (e) => {
        const oldGran = timeGranularity;
        timeGranularity = e.target.value;
        // Convert current frame to new granularity
        const oldConfig = GRANULARITY_CONFIG[oldGran];
        const newConfig = GRANULARITY_CONFIG[timeGranularity];
        const progress = currentFrame / (oldConfig.framesPerHour * 24 * 7);
        const maxFrames = newConfig.framesPerHour * 24 * 7;
        currentFrame = Math.round(progress * maxFrames);
        updateTimelineSliderMax();
        updateFrame(currentFrame);
        showToast("时间粒度已切换: " + timeGranularity);
      });"""

new_granularity = """      // Initialize granularity selector
      document.getElementById("granularitySelect").addEventListener("change", (e) => {
        const oldGran = timeGranularity;
        timeGranularity = e.target.value;
        // Convert current frame to new granularity
        const oldConfig = GRANULARITY_CONFIG[oldGran];
        const newConfig = GRANULARITY_CONFIG[timeGranularity];
        const progress = currentFrame / (oldConfig.framesPerHour * 24 * 7);
        const maxFrames = newConfig.framesPerHour * 24 * 7;
        currentFrame = Math.round(progress * maxFrames);
        updateTimelineSliderMax();
        updateFrame(currentFrame);
        showToast("时间粒度已切换: " + timeGranularity);
      });"""

content = content.replace(old_granularity, new_granularity)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated granularity selector (already correct)")
