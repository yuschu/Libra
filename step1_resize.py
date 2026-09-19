with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the end of initGlobe function and add helper functions after it
old_end = """    }
    }

    // ============ FRAME UPDATE ============"""

new_end = """    }
    }

    // ---- Window Resize ----
    function onWindowResize() {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      threeCamera.aspect = width / height;
      threeCamera.updateProjectionMatrix();
      
      threeRenderer.setSize(width, height);
      threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      
      threeComposer.setSize(width, height);
      bloomPass.setSize(width, height);
    }

    // ---- Globe Click Handler ----
    function onGlobeClick(event) {
      if (cameraFlying) return;
      
      const rect = canvas.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((event.clientX - rect.left) / rect.width) * 2 - 1,
        -((event.clientY - rect.top) / rect.height) * 2 + 1
      );
      
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, threeCamera);
      
      const routeObjects = Object.values(routeLineObjects);
      if (routeObjects.length === 0) return;
      
      const intersects = raycaster.intersectObjects(routeObjects, true);
      if (intersects.length > 0) {
        const roadId = intersects[0].object.userData.roadId;
        const road = roadMeta.find(r => r.road_id === roadId);
        if (!road) return;
        
        cameraFlying = true;
        autoRotateGlobe = false;
        
        // Animate camera to target
        const target = new THREE.Vector3(
          road.center_lon / 180 * Math.PI * 1.02,
          road.center_lat / 180 * Math.PI * 1.02,
          0
        );
        
        // Simple camera fly animation
        const startPos = threeCamera.position.clone();
        const startTarget = orbitControls.target.clone();
        const targetPos = new THREE.Vector3().copy(target).multiplyScalar(5000000);
        const targetTarget = new THREE.Vector3(0, 0, 0);
        
        const duration = 1500;
        const startTime = performance.now();
        
        function animateCamera(time) {
          const progress = Math.min((time - startTime) / 1500, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          
          threeCamera.position.lerpVectors(startPos, targetPos, eased);
          orbitControls.target.lerpVectors(startTarget, targetTarget, eased);
          orbitControls.update();
          
          if (progress < 1) {
            requestAnimationFrame(animateCamera);
          } else {
            cameraFlying = false;
            autoRotateGlobe = true;
          }
        }
        
        requestAnimationFrame(animateCamera);
        
        // Sync dropdown
        document.getElementById("roadSelect").value = roadId;
        selectedRoadId = roadId;
        updateFrame(currentFrame);
      }
    }

    // ============ FRAME UPDATE ============"""

content = content.replace(old_end, new_end)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added onWindowResize and onGlobeClick")
