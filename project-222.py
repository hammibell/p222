import glob
import os
import sys
import time
import threading

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_list = []

def turn_to_right():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.21))
    time.sleep(5)
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.18, steer=0.25))
    time.sleep(1)
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.34))
    time.sleep(4)


def check_traffic_lights():
    threading.Timer(0.1, check_traffic_lights).start()
    traffic_light = dropped_vehicle.get_traffic_light()

    if dropped_vehicle.is_at_traffic_light():
        print(traffic_light.get_state())

        # write code for if condition
        if traffic_light.get_state() == carla.TrafficLightState.Red:
            red_time = traffic_light.get_red_time()
            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
            time.sleep(1)
            # Change the traffic light color from red to yellow
        if traffic_light.get_state() == carla.TrafficLightState.Yellow:
            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
            time.sleep(1)
            dropped_vehicle.set_light_state(carla.VehicleLightState(carla.VehicleLightState.Brake | carla.VehicleLightState.LeftBlinker | carla.VehicleLightState.LowBeam))
            
            # write code here to turn car to right
            dropped_vehicle.apply_control(throttle = 0.3, steer = 0.2)
            dropped_vehicle.apply_control(throttle = 0.1, steer = 0.15)
            dropped_vehicle.apply_control(throttle = 0.34)

            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
            time.sleep(10)
            print("Car stopped. Well Done!")

        else:
            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
            time.sleep(10)



    else:
        dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.51))


try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter('model3')[0]
    spawn_point = (world.get_map().get_spawn_points()[20])
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    # car_control()
    check_traffic_lights()
    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')
