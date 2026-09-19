with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add Three.js state variables to STATE section
old_state = """    // ============ STATE ============
    let globeChart = null;
    let roadMeta = [];
    let accidentsData = [];
    let vehicleTypesData = [];
    let trafficCache = new Map(); // key: \${road_id}-\${dt} -> {flow, avg_speed, density}
    let currentFrame = 0;
    let isPlaying = false;
    let playTimer = null;
    let playbackSpeed = 1;
    let selectedRoadId = \"\";
    let timeRange = { start: null, end: null };
    let layers = { accidents: true, vehicleTypes: true, nonMotorized: false };"""

new_state = """    // ============ STATE ============
    let globeChart = null;
    let roadMeta = [];
    let accidentsData = [];
    let vehicleTypesData = [];
    let trafficCache = new Map(); // key: \${road_id}-\${dt} -> {flow, avg_speed, density}
    let currentFrame = 0;
    let isPlaying = false;
    let playTimer = null;
    let playbackSpeed = 1;
    let selectedRoadId = \"\";
    let timeRange = { start: null, end: null };
    let layers = { accidents: true, vehicleTypes: true, nonMotorized: false };
    // Three.js state
    let threeScene, threeCamera, threeRenderer, threeComposer, bloomPass, orbitControls;
    let globeMesh, wireframeMesh, glowMesh;
    let routeLines = {}, routeLineObjects = {};
    let autoRotateGlobe = true;
    let lastAutoRotateTime = 0;
    let cameraFlying = false;"""

content = content.replace(old_state, new_state)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added Three.js state variables to STATE section")
