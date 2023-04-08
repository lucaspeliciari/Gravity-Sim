from math import pi

from functions import *
from vars import universe_boundary


def update_acceleration(bodies):  # accel in m/s²  
    for body in bodies:
        force_summation_x = 0
        force_summation_y = 0
        force_summation_z = 0
        if body.influenced_by_gravity:
            for other_body in body.circle_of_influence:
                if other_body.has_gravity:
                    gravitational_forces = get_g_forces(body, other_body, METERS)
                    gravitational_force_x = gravitational_forces[0]
                    gravitational_force_y = gravitational_forces[1]
                    gravitational_force_z = gravitational_forces[2]

                    force_summation_x += gravitational_force_x
                    force_summation_y += gravitational_force_y
                    force_summation_z += gravitational_force_z

            # did I really remove "/ mass" from this? Check
            body.acceleration_x = force_summation_x
            body.acceleration_y = force_summation_y
            body.acceleration_z = force_summation_z


def update_velocity(bodies, time):  # v in m/s
    for body in bodies:
        if body.can_move:
            body.velocity_x += body.acceleration_x * time
            body.velocity_y += body.acceleration_y * time
            body.velocity_z += body.acceleration_z * time
        else:
            body.velocity_x = body.velocity_y = body.velocity_z = 0.0


def update_position(bodies, time, trail_interval, trail_length, min_distance_to_trail):
    for body in bodies:
        if body.can_move:
            body.x += (body.velocity_x * time + (body.acceleration_x * pow(time, 2)) / 2) / SCALE
            body.y += (body.velocity_y * time + (body.acceleration_y * pow(time, 2)) / 2) / SCALE
            body.z += (body.velocity_z * time + (body.acceleration_z * pow(time, 2)) / 2) / SCALE
            update_trail(body, trail_interval, trail_length, min_distance_to_trail)


def update_trail(body, trail_interval, trail_length, min_distance_to_trail):  # really clean this up
    # TRAIL
    body.physics_interval_counter += 1
    if len(body.trail) > 1:
        distance_x = body.trail[-1][0] - body.x
        distance_y = body.trail[-1][1] - body.y
        # distance_z = body.trail[-1][2] - body.z  # maybe implement later
        distance = sqrt(pow(distance_x, 2) + pow(distance_y, 2))
    else:
        distance = min_distance_to_trail + 1

    if body.physics_interval_counter > trail_interval and distance > min_distance_to_trail:
        body.trail.append((body.x, body.y, body.z))
        body.physics_interval_counter = 0
    if len(body.trail) > trail_length:
        body.trail.pop(0)


def check_boundaries(bodies,  # disabled because it is VERY broken!
                     radius_scale: int = RADIUS_SCALE
                     ):
    for body in bodies:
        r = body.radius / radius_scale
        if body.x - r <= universe_boundary[0] or body.x + r >= universe_boundary[1]:
            body.velocity_x *= -1
        if body.y - r <= universe_boundary[2] or body.y + r >= universe_boundary[3]:
            body.velocity_y *= -1
        if body.z - r <= universe_boundary[4] or body.z + r >= universe_boundary[5]:
            body.velocity_z *= -1


def check_body_collision(sim,  # SLOW
                         radius_scale: int = RADIUS_SCALE
                         ):
    to_remove = []
    ignore_list = []  # do not use this! use j=i+1 in the second for
    for i, body in enumerate(sim.bodies):
        if body.can_collide:
            # for j, other_body in enumerate([x for x in sim.bodies if x != body]):
            for j, other_body in enumerate([x for x in sim.bodies if x not in ignore_list and body != x]):
                dx, dy, dz = get_distances(body, other_body, PIXELS)
                d, _ = components_to_vector(dx, dy, dz)

                # Wrong due to perspective scaling, so fix
                sum_of_radii = (body.radius + other_body.radius) / radius_scale

                if d < sum_of_radii:  # COLLIDED
                    if body.collisions_with_bodies[j] > 5:  # DESTROY
                        if body.mass < other_body.mass:
                            to_remove.append(i)
                            other_body.mass += body.mass
                            other_body.radius += pow(pow(body.radius, 3) + pow(other_body.radius, 3),
                                                     (1 / 3))  # cube roots might be too slow
                    else:  # BOUNCE, terrible, does not work, delete
                        body_velocity, other_body_velocity = elastic_collision(body, other_body)
                        body.velocity_x, body.velocity_y, body.velocity_z = body_velocity[0], body_velocity[1], \
                                                                            body_velocity[2]
                        other_body.velocity_x, other_body.velocity_y, other_body.velocity_z = other_body_velocity[0], \
                                                                                              other_body_velocity[1], \
                                                                                              other_body_velocity[2]
                        body_velocity_module, body_velocity_angle = components_to_vector(body.velocity_x,
                                                                                         body.velocity_y,
                                                                                         body.velocity_z)

                        angle_xy = atan2(dy, dx)  # regular screen plane
                        angle_yz = atan2(dz, dy)  # inclination of regular screen plane
                        body_velocity_angle = 2 * angle_xy + body_velocity_angle  # angle for XY seems correct

                        body.velocity_x = cos(body_velocity_angle) * body_velocity_module
                        body.velocity_y = sin(body_velocity_angle) * body_velocity_module

                        unstuck_angle = 0.5 * pi + body_velocity_angle

                        if body.can_move:
                            # body.velocity_module = v1
                            body.x += cos(unstuck_angle)
                            body.y += sin(unstuck_angle)
                        # if other_body.can_move:
                        # other_body.velocity_module = v2
                        # other_body.x -= cos(unstuck_angle)
                        # other_body.y += sin(unstuck_angle)

                        # body.collisions_with_bodies[j] += 1  # turn this on after finishing collisions (or remove altogether if possible)
                        # other_body.collisions_with_bodies[j] += 1

                else:
                    collision_value = body.collisions_with_bodies[j]
                    collision_value -= 1
                    collision_value = max(0, collision_value)
                    body.collisions_with_bodies[j] = collision_value
        ignore_list.append(body)

    if len(to_remove) > 0:
        sim.remove_body(to_remove)


def elastic_collision(body: Body,  # maybe remove
                      other_body: Body):
    vx1 = (body.velocity_x * (body.mass - other_body.mass) + 2 * other_body.mass * other_body.velocity_x) / (
                body.mass + other_body.mass)
    vx2 = (other_body.velocity_x * (other_body.mass - body.mass) + 2 * body.mass * body.velocity_x) / (
                body.mass + other_body.mass)
    vy1 = (body.velocity_y * (body.mass - other_body.mass) + 2 * other_body.mass * other_body.velocity_y) / (
                body.mass + other_body.mass)
    vy2 = (other_body.velocity_y * (other_body.mass - body.mass) + 2 * body.mass * body.velocity_y) / (
                body.mass + other_body.mass)
    vz1 = (body.velocity_z * (body.mass - other_body.mass) + 2 * other_body.mass * other_body.velocity_z) / (
                body.mass + other_body.mass)
    vz2 = (other_body.velocity_z * (other_body.mass - body.mass) + 2 * body.mass * body.velocity_z) / (
                body.mass + other_body.mass)

    vx1 *= ELASTICITY
    vx2 *= ELASTICITY
    vy1 *= ELASTICITY
    vy2 *= ELASTICITY
    vz1 *= ELASTICITY
    vz2 *= ELASTICITY

    return (vx1, vy1, vz1), (vx2, vy2, vz2)
