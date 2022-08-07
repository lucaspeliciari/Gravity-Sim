from math import pi

from functions import *
from vars import universe_boundary


# use Vector3!

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


def check_body_collision(sim,  # SLOW, test
                         radius_scale: int = RADIUS_SCALE
                         ):
    to_remove = []
    for i, body in enumerate(sim.bodies):
        if body.can_collide:
            # for j, other_body in enumerate([x for x in sim.bodies if x not in ignore_list and body != x]):
            for j in range(i+1, len(sim.bodies)):
                dx, dy, dz = get_distances(body, sim.bodies[j], PIXELS)
                d, _ = components_to_vector(dx, dy, dz)

                # Wrong due to perspective scaling, so fix
                sum_of_radii = (body.radius + sim.bodies[j].radius) / radius_scale

                if d < sum_of_radii:  # COLLIDED
                    if body.mass < sim.bodies[j].mass:
                        to_remove.append(i)
                        sim.bodies[j].mass += body.mass / 5  # 5 otherwise it gets way too big
                        sim.bodies[j].radius += pow(pow(body.radius, 3) + pow(sim.bodies[j].radius, 3), (1 / 3)) / 5  # 5 otherwise it gets way too big
                    else:
                        to_remove.append(j)
                        sim.bodies[i].mass += body.mass / 5  # 5 otherwise it gets way too big
                        sim.bodies[i].radius += pow(pow(body.radius, 3) + pow(sim.bodies[i].radius, 3), (1 / 3)) / 5  # 5 otherwise it gets way too big

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
