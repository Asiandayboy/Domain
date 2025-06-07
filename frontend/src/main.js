import * as THREE from "three"
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"



const TARGET_SIZE = 2
const CAMERA_DISTANCE = 4


let NUM_OF_3D_MODELS = null
let modelIndex = 0;
let MODEL_ASSETS
let MODEL_METADATA
let currentModel = null

const scene = new THREE.Scene()
const loader = new GLTFLoader();


async function fetch3dModels() {
    const res = await fetch("/api/models", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    })

    const data = await res.json()

    MODEL_ASSETS = data.models
    MODEL_METADATA = data.metadata
    NUM_OF_3D_MODELS = MODEL_ASSETS.length

    connectThreejsWrapperButtons()

    // load first model on startup
    loadModelIntoScene(modelIndex)
}

function removeCurrentModelFromScene() {
    if (currentModel) {
        scene.remove(currentModel);
        currentModel.traverse((child) => {
            if (child.geometry) child.geometry.dispose();
            if (child.material) {
                if (Array.isArray(child.material)) {
                    child.material.forEach((m) => m.dispose());
                } else {
                    child.material.dispose();
                }
            }
        });
    }
}

function loadModelIntoScene(modelIndex) {
    const uid = MODEL_ASSETS[modelIndex]
    const info = MODEL_METADATA[uid]
    const modelNameElement = document.getElementById("model-name")
    const modelDescElement = document.getElementById("model-desc")
    const counterElement = document.getElementById("counter")

    loader.load(`/static/assets/3d/${uid}/scene.gltf`, (glft) => {
        removeCurrentModelFromScene()
        currentModel = glft.scene

        // Compute bounding box
        const box = new THREE.Box3().setFromObject(currentModel);
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        // Compute scale factor to make largest dimension == targetSize
        const scale = TARGET_SIZE / maxDim;
        currentModel.scale.setScalar(scale);

        // Reposition model so it sits on ground centered
        const center = box.getCenter(new THREE.Vector3());
        currentModel.position.x -= center.x * scale;
        currentModel.position.y -= center.y * scale;
        currentModel.position.z -= center.z * scale;

        // currentModel.position.set(0, -0.25, 0);

        scene.add(currentModel)
        // console.log(uid)

        modelNameElement.innerHTML = info.name
        modelDescElement.innerHTML = info.description
        counterElement.innerHTML = `${modelIndex+1}/${NUM_OF_3D_MODELS}`
    }, undefined, (error) => {
        console.error(`Error loading model ${uid}:`, error)
    })
}


function prevModel() {
    modelIndex = (modelIndex - 1 + NUM_OF_3D_MODELS) % NUM_OF_3D_MODELS
    loadModelIntoScene(modelIndex)
    // console.log("prev model: index =", modelIndex)
}

function nextModel() {
    modelIndex = (modelIndex + 1) % NUM_OF_3D_MODELS
    loadModelIntoScene(modelIndex)
    // console.log("next model: index =", modelIndex)
}

function connectThreejsWrapperButtons() {
    const prevBtn = document.getElementById("prev")
    const nextBtn = document.getElementById("next")

    prevBtn.onclick = () => {
        prevModel()
    }

    nextBtn.onclick = () => {
        nextModel()
    }
}

async function askAI() {
    const prompt = document.getElementById("prompt").value

    if (prompt.trim() == "") { return }

    const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            prompt: prompt,
            model_id: MODEL_ASSETS[modelIndex]
        })
    })

    const data = await res.json()


    const responseElement = document.getElementById("response")
    responseElement.innerHTML = data.response
    responseElement.style.display = "block" 
}

document.getElementById("ai-submit-btn").onclick = askAI


const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000)
camera.position.z = CAMERA_DISTANCE

const renderer = new THREE.WebGLRenderer()
const wrapper3d = document.getElementById("3d-renderer");
const width = wrapper3d.clientWidth;
const height = wrapper3d.clientHeight;

renderer.setSize(width, height);
renderer.setPixelRatio(window.devicePixelRatio);
wrapper3d.appendChild(renderer.domElement)



const light = new THREE.DirectionalLight(0xffffff, 1)
light.position.set(1,1,1)
scene.add(light)

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // white light, half intensity
scene.add(ambientLight);

const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
hemiLight.position.set(0, 20, 0);
scene.add(hemiLight);


scene.background = new THREE.Color(0xF3F3F7);


const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // smooth camera motion
controls.dampingFactor = 0.05;
controls.screenSpacePanning = false;
controls.minDistance = 1;
controls.maxDistance = 100;
controls.maxPolarAngle = Math.PI;




// const controls = new FlyControls(camera, renderer.domElement);
// const clock = new THREE.Clock()

// controls.movementSpeed = 10;
// controls.rollSpeed = Math.PI / 2;
// controls.dragToLook = true;  // true means you have to hold mouse to look around
// controls.autoForward = false;


window.addEventListener("resize", () => {
    const width = wrapper3d.clientWidth
    const height = wrapper3d.clientHeight

    camera.aspect = width/height
    camera.updateProjectionMatrix()
    renderer.setSize(width, height)
})


function animate() {
    requestAnimationFrame(animate)

    // const delta = clock.getDelta()
    controls.update()

    renderer.render(scene, camera)
}

animate()
fetch3dModels()
