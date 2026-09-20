with open('web-screen/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_state = '''    // ============ STATE ============
    let globeChart = null;
    let roadMeta = [];
    let accidentsData = [];
    let vehicleTypesData = [];
    let trafficCache = new Map(); // key: - -> {flow, avg_speed, density}
    let currentFrame = 0;
    let isPlaying = false;
    let playTimer = null;
    let playbackSpeed = 1;
    let threeRenderer = null, threeScene = null, threeCamera = null, threeComposer = null, bloomPass = null;
    let orbitControls = null, globeMesh = null, wireframeMesh = null, glowMesh = null;
    let routeLineObjects = [], routeLines = [];
    let autoRotateGlobe = true, cameraFlying = false;
    let selectedRoadId = \
\;
    let timeRange = { start: null, end: null };
    let layers = { accidents: true, vehicleTypes: true, nonMotorized: false };
    let autoRotate = true;
    // Time granularity
    let timeGranularity = \h\; // \ms\, \s\, \min\, \h\
    const GRANULARITY_CONFIG = {
      ms: { step: 1, labelFormat: (d) => d.toISOString().slice(11, 23), stepMs: 1, framesPerHour: 3600000 },
      s:  { step: 1, labelFormat: (d) => d.toISOString().slice(11, 19), stepMs: 1000, framesPerHour: 3600 },
      min: { step: 1, labelFormat: (d) => d.toISOString().slice(11, 16), stepMs: 60000, framesPerHour: 60 },
      h:   { step: 1, labelFormat: (d) => d.toISOString().slice(11, 16), stepMs: 3600000, framesPerHour: 1 }
    };'''

new_state = '''    // ============ STATE ============
    let globeChart = null;
    let roadMeta = [];
    let accidentsData = [];
    let vehicleTypesData = [];
    let trafficCache = new Map(); // key: - -> {flow, avg_speed, density}
    let currentFrame = 0;
    let isPlaying = false;
    let playTimer = null;
    let playbackSpeed = 1;
    let threeRenderer = null, threeScene = null, threeCamera = null, threeComposer = null, bloomPass = null;
    let orbitControls = null, globeMesh = null, wireframeMesh = null, glowMesh = null;
    let routeLineObjects = [], routeLines = [];
    let autoRotateGlobe = true, cameraFlying = false;
    let selectedRoadId = \\;
    let timeRange = { start: null, end: null };
    let layers = { accidents: true, vehicleTypes: true, nonMotorized: false };
    let autoRotate = true;
    # Time granularity
    let timeGranularity = \h\; # \ms\, \s\, \min\, \h\
    const GRANULARITY_CONFIG = {
      ms: { step: 1, labelFormat: (d) => d.toISOString().slice(11, 23), stepMs: 1, framesPerHour: 3600000 },
      s:  { step: 1, labelFormat: (d) => d.toISOString().slice(11, 19), stepMs: 1000, framesPerHour: 3600 },
      min: { step: 1, labelFormat: (d) => d.toISOString().slice(11, 16), stepMs: 60000, framesPerHour: 60 },
      h:   { step: 1, labelFormat: (d) => d.toISOString().slice(11, 16), stepMs: 3600000, framesPerHour: 1 }
    };
    # Province data
    let provinceData = [];
    let provinceMeshes = [];'''

content = content.replace(old_state, new_state)

with open('web-screen/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added provinceData and provinceMeshes to STATE')
