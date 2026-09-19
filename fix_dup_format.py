with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the second formatTimeForGranularity and remove the duplicate block
idx2 = 16473
next_func = content.find("\n    function ", idx2 + 50)
if next_func == -1:
    next_func = content.find("\n    // ==========", idx2 + 50)

print(f"Second formatTimeForGranularity starts at: {idx2}")
print(f"Next function starts at: {next_func}")

if next_func != -1:
    print("--- DUPLICATE BLOCK ---")
    print(content[idx2:next_func])
    print("--- END ---")
    
    # Remove the duplicate block
    content = content[:idx2] + content[next_func:]
    
    with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Removed duplicate formatTimeForGranularity block")
