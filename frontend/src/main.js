import * as THREE from "three"
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"
import { FlyControls } from "three/examples/jsm/controls/FlyControls.js"


console.log("THREE.js!")

const TARGET_SIZE = 2
const CAMERA_DISTANCE = 20

const SPACING = 4; // distance between models
const MODELS_PER_ROW = 5;


const scene = new THREE.Scene()

function addModelToScene(loader, uid, index) {
    console.log("uid:", uid)
    loader.load(`/static/assets/3d/${uid}/scene.gltf`, (gltf) => {
        const model = gltf.scene;

        // Compute bounding box
        const box = new THREE.Box3().setFromObject(model);
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        // Compute scale factor to make largest dimension == targetSize
        const scale = TARGET_SIZE / maxDim;
        model.scale.setScalar(scale);

        // Optionally reposition model so it sits on ground or centered
        const center = box.getCenter(new THREE.Vector3());
        model.position.x -= center.x * scale;
        model.position.y -= center.y * scale;
        model.position.z -= center.z * scale;

        const row = Math.floor(index / MODELS_PER_ROW);
        const col = index % MODELS_PER_ROW;
        model.position.set(col * SPACING, 0, row * SPACING);

        scene.add(model);
    }, undefined, (error) => {
        console.error(`Error loading model ${uid}:`, error);
    });
}

async function fetch3dModels() {

    const res = await fetch("/api/models", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    })

    const data = await res.json()


    const loader = new GLTFLoader();
    data.forEach((pathToModel, index) => {
        addModelToScene(loader, pathToModel, index)
    });

}



const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
camera.position.z = CAMERA_DISTANCE

const renderer = new THREE.WebGLRenderer()
const wrapper3d = document.getElementById("3d-renderer-wrapper");
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


scene.background = new THREE.Color(0xdddddd);


const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // smooth camera motion
controls.dampingFactor = 0.05;
controls.screenSpacePanning = false;
controls.minDistance = 1;
controls.maxDistance = 100;
controls.maxPolarAngle = Math.PI / 2; // prevent camera from going below ground




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

// const geometry = new THREE.BoxGeometry();
// const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
// const cube = new THREE.Mesh(geometry, material);
// scene.add(cube);

fetch3dModels()