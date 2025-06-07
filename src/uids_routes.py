from flask import Blueprint, jsonify
import os
from flasgger import swag_from


uids_bp = Blueprint("uids", __name__)


import os

model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "static", "assets", "3d"))


MODEL_INFO = {
    "ArduinoUNO_43cebeb50dc14ab490b553f0a0077eb9": {
        "name": "Arduino UNO",
        "description": "A microcontroller board based on the ATmega328P.",
        "embedded_context": "Arduino boards are widely used in embedded systems and prototyping for tasks like sensor interfacing, motor control, and IoT applications."
    },
    "AUVDevice_a504bfe01f9e474d8d771a5c4124c825": {
        "name": "Autonomous Underwater Vehicle (AUV)",
        "description": "A robotic device designed to operate underwater without direct human control.",
        "embedded_context": "AUVs rely on embedded systems for navigation, sensor integration, sonar processing, and mission control in marine exploration."
    },
    "CCTVCamera_281b2b84260447e49ab4a6b34bf78697": {
        "name": "CCTV Camera",
        "description": "A closed-circuit television camera used for surveillance.",
        "embedded_context": "Modern CCTV cameras use embedded processors for image capture, motion detection, video encoding, and network streaming."
    },
    "DHT22TemperatureSensorModule_c46a658784034c679e4907bbddad0093": {
        "name": "DHT22 Temperature and Humidity Sensor",
        "description": "A digital sensor that measures temperature and humidity.",
        "embedded_context": "Often used with microcontrollers like Arduino or ESP32, the DHT22 enables environmental monitoring in smart homes, weather stations, and IoT devices."
    },
    "FlyingDrone_2ecfb55304a043a2a86353f70cc1cf92": {
        "name": "Flying Drone",
        "description": "A quadcopter aerial drone used for surveillance, photography, or transport.",
        "embedded_context": "Drones use embedded systems for flight stabilization, GPS navigation, camera control, wireless communication, and autonomous flight behavior."
    },
    "IndustrialRobot_e5e6703e7788417e9761eb4dc516de5a": {
        "name": "Industrial Robot Arm",
        "description": "A multi-jointed robotic arm used in manufacturing automation.",
        "embedded_context": "Industrial robots rely on real-time embedded systems for motor control, feedback sensing, task scheduling, and safety protocols."
    },
    "TrafficLight_7b86bedf64c04e15a0e01a84d29ea93d": {
        "name": "Traffic Light",
        "description": "Traffic lights control traffic flow by signaling when vehicles and pedestrians must stop or go.",
        "embedded_context": "Demonstrates real-world use of embedded systems in smart city applications, traffic flow optimization, and real-time sensor feedback integration."
    },
    "Truck_72caf995b6064890b7bc62371cc79f36": {
        "name": "A Truck",
        "description": "A standard cargo truck used for transporting goods over roads.",
        "embedded_context": "Modern trucks include embedded systems for engine control, safety features like ABS, and onboard diagnostics."
    }
}


@uids_bp.route("/models", methods=["GET"])
@swag_from({
    "responses": {
        "200": {
            "description": "JSON array of strings of 3D model uids",
            "examples": {
                "application/json": {
                    "response": ["ID_1", "ID_2", "ID_3", "ID_4"]
                }
            }
        },
    } 
})
def get_model_list():
    """
    Get a list of available 3D model UIDs from SketchFab.
    ___ 
    """
    list_of_models = [
        d for d in os.listdir(model_dir)
        if os.path.isdir(os.path.join(model_dir, d))
    ]

    res = {
        "models": list_of_models,
        "metadata": MODEL_INFO
    }

    return jsonify(res)