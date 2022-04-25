#!/usr/bin/env python

# Copyright (c) 2018-2020 Intel Corporation
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Follow leading vehicle scenario:

The scenario realizes a common driving behavior, in which the
user-controlled ego vehicle follows a leading car driving down
a given road. At some point the leading car has to slow down and
finally stop. The ego vehicle has to react accordingly to avoid
a collision. The scenario ends either via a timeout, or if the ego
vehicle stopped close enough to the leading vehicle
"""

import random

import py_trees

import carla



from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
from srunner.scenariomanager.scenarioatomics.atomic_behaviors import (ActorTransformSetter,
                                                                      ActorDestroy,
                                                                      KeepVelocity,
                                                                      StopVehicle,
                                                                      WaypointFollower,
                                                                      Idle)
from srunner.scenariomanager.scenarioatomics.atomic_criteria import CollisionTest
from srunner.scenariomanager.scenarioatomics.atomic_trigger_conditions import (InTriggerDistanceToVehicle,
                                                                               InTriggerDistanceToNextIntersection,
                                                                               DriveDistance,
                                                                               StandStill)
from srunner.scenariomanager.timer import TimeOut
from srunner.scenarios.basic_scenario import BasicScenario
from srunner.tools.scenario_helper import get_waypoint_in_distance

from srunner.tools.background_manager import Scenario2Manager
from srunner.tools.route_parser import RouteParser
from srunner.tools.route_manipulation import interpolate_trajectory, interpolate_trajectory_modified
import srunner.scenarios.DATA as INIT_DATA



class FollowLeadingVehicle(BasicScenario):

    """
    This class holds everything required for a simple "Follow a leading vehicle"
    scenario involving two vehicles.  (Traffic Scenario 2)

    This is a single ego vehicle scenario
    """

    timeout = 1300            # Timeout of scenario in seconds
    def __init__(self, world, ego_vehicles, config, randomize=False, debug_mode=False, criteria_enable=True,
                 timeout=1300):
        """
        Setup all relevant parameters and create scenario

        If randomize is True, the scenario parameters are randomized
        """
        routes = "srunner/data/convoy.xml"
        scenario_file = "srunner/data/no_scenario.json"
        route_id = 0
        self.world = world
        route_configurations = RouteParser.parse_routes_file(routes, scenario_file, route_id)
        traj = route_configurations[0].trajectory
        print("traj....XXXXXXXXXXXXXXXXX:",traj)
        route0 = [carla.libcarla.Location(x=-379.6, y=-17.6, z=0),carla.libcarla.Location(x=-379.1, y=22.8, z=0),traj[0]]

        inter_route_0 = interpolate_trajectory_modified(world,route0)
        inter_route = interpolate_trajectory_modified(world,traj)
        route2 = [traj[-1]]
        route2.append(carla.libcarla.Location(x=403.56, y=-205.61, z=0))
        route2.append(carla.libcarla.Location(x=403.56, y=-216.3, z=0))
        route2.append(carla.libcarla.Location(x=357.6, y=-342.2, z=0))
        # last_waypoint.append(carla.libcarla.Location(x=250.0, y=-385.7, z=0))

        inter_route_2 = interpolate_trajectory_modified(world,route2)
        route3 = [route2[-1]]
        # route3.append(carla.libcarla.Location(x=250.0, y=-385.7, z=0))
        route3.append(carla.libcarla.Location(x=152.3, y=-385.7, z=0))

        inter_route_3 = interpolate_trajectory_modified(world,route3)

        route4 = [route3[-1]]
        route4.append(carla.libcarla.Location(x=62.5, y=-354.5, z=0))
        inter_route_4 = interpolate_trajectory_modified(world,route4)

        route5 = [route4[-1]]
        route5.append(carla.libcarla.Location(x=-6.2, y=-224.3, z=0))
        inter_route_5 = interpolate_trajectory_modified(world,route5)

        route6 = [route5[-1]]
        route6.append(carla.libcarla.Location(x=-9.3, y=-15.1, z=0))
        route6.append(carla.libcarla.Location(x=-12.4, y=31.1, z=0))
        inter_route_6 = interpolate_trajectory_modified(world,route6)

        route7 = [route6[-1]]
        route7.append(carla.libcarla.Location(x=-49.0, y=141.8, z=0))
        inter_route_7 = interpolate_trajectory_modified(world,route7)


        print("inter_route1:",inter_route[-1],len(inter_route))
        inter_route_comb = inter_route_0 + inter_route + inter_route_2 + inter_route_3 + inter_route_4 + inter_route_5 + inter_route_6 + inter_route_7
        self.trajectory_leadVehicle = inter_route_comb
        self.init_trajectory_leadVehicle = interpolate_trajectory_modified(world,INIT_DATA.INIT_ROUTE)


        self._map = CarlaDataProvider.get_map()
        self._first_vehicle_location = 20
        self._first_vehicle_speed = 25
        self._reference_waypoint = self._map.get_waypoint(config.trigger_points[0].location)
        self._other_actor_max_brake = 1.0
        self._other_actor_stop_in_front_intersection = 20
        self._other_actor_transform = None
        # Timeout of scenario in secondswwwwww
        self.timeout = timeout

        super(FollowLeadingVehicle, self).__init__("FollowVehicle",
                                                   ego_vehicles,
                                                   config,
                                                   world,
                                                   debug_mode,
                                                   criteria_enable=criteria_enable)

        if randomize:
            self._ego_other_distance_start = random.randint(4, 8)

            # Example code how to randomize start location
            # distance = random.randint(20, 80)
            # new_location, _ = get_location_in_distance(self.ego_vehicles[0], distance)
            # waypoint = CarlaDataProvider.get_map().get_waypoint(new_location)
            # waypoint.transform.location.z += 39
            # self.other_actors[0].set_transform(waypoint.transform)

    def _initialize_actors(self, config):
        """
        Custom initialization
        """
        print("initialize_actors")
        waypoint, _ = get_waypoint_in_distance(self._reference_waypoint, self._first_vehicle_location)
        transform = waypoint.transform
        print("transform:",transform)
        # breakpoint()
        transform.location.x = INIT_DATA.LEAD_X_INIT
        transform.location.y = INIT_DATA.LEAD_Y_INIT
        transform.location.z = INIT_DATA.LEAD_Z_INIT
        transform.rotation.yaw = 100
        first_vehicle = CarlaDataProvider.request_new_actor('vehicle.nissan.patrol', transform)
        # WaypointFollower(first_vehicle, self._first_vehicle_speed, plan=self.init_trajectory_leadVehicle)
        self.other_actors.append(first_vehicle)

    def _create_behavior(self):
        """
        The scenario defined after is a "follow leading vehicle" scenario. After
        invoking this scenario, it will wait for the user controlled vehicle to
        enter the start region, then make the other actor to drive until reaching
        the next intersection. Finally, the user-controlled vehicle has to be close
        enough to the other actor to end the scenario.
        If this does not happen within 60 seconds, a timeout stops the scenario
        """
        print("create_behavior")
        # let the other actor drive until next intersection
        driving_to_next_intersection = py_trees.composites.Parallel(
            "DrivingTowardsIntersection",
            policy=py_trees.common.ParallelPolicy.SUCCESS_ON_ONE)
        driving_to_next_intersection.add_child(WaypointFollower(self.other_actors[0], self._first_vehicle_speed, plan=self.trajectory_leadVehicle))
        # driving_to_next_intersection.add_child(InTriggerDistanceToNextIntersection(
            # self.other_actors[0], self._other_actor_stop_in_front_intersection))

        # stop vehicle
        stop = StopVehicle(self.other_actors[0], self._other_actor_max_brake)

        # end condition
        endcondition = py_trees.composites.Parallel("Waiting for end position",
                                                    policy=py_trees.common.ParallelPolicy.SUCCESS_ON_ALL)
        endcondition_part1 = InTriggerDistanceToVehicle(self.other_actors[0],
                                                        self.ego_vehicles[0],
                                                        distance=5,
                                                        name="FinalDistance")
        endcondition_part2 = StandStill(self.ego_vehicles[0], name="StandStill", duration=1)
        endcondition.add_child(endcondition_part1)
        endcondition.add_child(endcondition_part2)

        # Build behavior tree
        sequence = py_trees.composites.Sequence("Sequence Behavior")
        sequence.add_child(driving_to_next_intersection)
        sequence.add_child(stop)
        sequence.add_child(endcondition)
        sequence.add_child(ActorDestroy(self.other_actors[0]))

        return sequence

    def _create_test_criteria(self):
        """
        A list of all test criteria will be created that is later used
        in parallel behavior tree.
        """
        criteria = []

        collision_criterion = CollisionTest(self.ego_vehicles[0])

        criteria.append(collision_criterion)

        return criteria

    def __del__(self):
        """
        Remove all actors upon deletion
        """
        self.remove_all_actors()


class FollowLeadingVehicleWithObstacle(BasicScenario):

    """
    This class holds a scenario similar to FollowLeadingVehicle
    but there is an obstacle in front of the leading vehicle

    This is a single ego vehicle scenario
    """

    timeout = 120            # Timeout of scenario in seconds

    def __init__(self, world, ego_vehicles, config, randomize=False, debug_mode=False, criteria_enable=True):
        """
        Setup all relevant parameters and create scenario
        """
        self._map = CarlaDataProvider.get_map()
        self._first_actor_location = 10
        self._second_actor_location = self._first_actor_location + 41
        self._first_actor_speed = 10
        self._second_actor_speed = 1.5
        self._reference_waypoint = self._map.get_waypoint(config.trigger_points[0].location)
        self._other_actor_max_brake = 1.0
        self._first_actor_transform = None
        self._second_actor_transform = None

        super(FollowLeadingVehicleWithObstacle, self).__init__("FollowLeadingVehicleWithObstacle",
                                                               ego_vehicles,
                                                               config,
                                                               world,
                                                               debug_mode,
                                                               criteria_enable=criteria_enable)
        if randomize:
            self._ego_other_distance_start = random.randint(4, 8)

    def _initialize_actors(self, config):
        """
        Custom initialization
        """

        first_actor_waypoint, _ = get_waypoint_in_distance(self._reference_waypoint, self._first_actor_location)
        second_actor_waypoint, _ = get_waypoint_in_distance(self._reference_waypoint, self._second_actor_location)
        first_actor_transform = carla.Transform(
            carla.Location(first_actor_waypoint.transform.location.x,
                           first_actor_waypoint.transform.location.y,
                           first_actor_waypoint.transform.location.z - 500),
            first_actor_waypoint.transform.rotation)
        self._first_actor_transform = carla.Transform(
            carla.Location(first_actor_waypoint.transform.location.x,
                           first_actor_waypoint.transform.location.y,
                           first_actor_waypoint.transform.location.z + 1),
            first_actor_waypoint.transform.rotation)
        yaw_1 = second_actor_waypoint.transform.rotation.yaw + 90
        second_actor_transform = carla.Transform(
            carla.Location(second_actor_waypoint.transform.location.x,
                           second_actor_waypoint.transform.location.y,
                           second_actor_waypoint.transform.location.z - 500),
            carla.Rotation(second_actor_waypoint.transform.rotation.pitch, yaw_1,
                           second_actor_waypoint.transform.rotation.roll))
        self._second_actor_transform = carla.Transform(
            carla.Location(second_actor_waypoint.transform.location.x,
                           second_actor_waypoint.transform.location.y,
                           second_actor_waypoint.transform.location.z + 1),
            carla.Rotation(second_actor_waypoint.transform.rotation.pitch, yaw_1,
                           second_actor_waypoint.transform.rotation.roll))

        first_actor = CarlaDataProvider.request_new_actor(
            'vehicle.nissan.patrol', first_actor_transform)
        second_actor = CarlaDataProvider.request_new_actor(
            'vehicle.diamondback.century', second_actor_transform)

        first_actor.set_simulate_physics(enabled=False)
        second_actor.set_simulate_physics(enabled=False)
        self.other_actors.append(first_actor)
        self.other_actors.append(second_actor)

    def _create_behavior(self):
        """
        The scenario defined after is a "follow leading vehicle" scenario. After
        invoking this scenario, it will wait for the user controlled vehicle to
        enter the start region, then make the other actor to drive towards obstacle.
        Once obstacle clears the road, make the other actor to drive towards the
        next intersection. Finally, the user-controlled vehicle has to be close
        enough to the other actor to end the scenario.
        If this does not happen within 60 seconds, a timeout stops the scenario
        """

        # let the other actor drive until next intersection
        driving_to_next_intersection = py_trees.composites.Parallel(
            "Driving towards Intersection",
            policy=py_trees.common.ParallelPolicy.SUCCESS_ON_ONE)

        obstacle_clear_road = py_trees.composites.Parallel("Obstalce clearing road",
                                                           policy=py_trees.common.ParallelPolicy.SUCCESS_ON_ONE)
        obstacle_clear_road.add_child(DriveDistance(self.other_actors[1], 4))
        obstacle_clear_road.add_child(KeepVelocity(self.other_actors[1], self._second_actor_speed))

        stop_near_intersection = py_trees.composites.Parallel(
            "Waiting for end position near Intersection",
            policy=py_trees.common.ParallelPolicy.SUCCESS_ON_ONE)
        stop_near_intersection.add_child(WaypointFollower(self.other_actors[0], 10))
        stop_near_intersection.add_child(InTriggerDistanceToNextIntersection(self.other_actors[0], 20))

        driving_to_next_intersection.add_child(WaypointFollower(self.other_actors[0], self._first_actor_speed))
        driving_to_next_intersection.add_child(InTriggerDistanceToVehicle(self.other_actors[1],
                                                                          self.other_actors[0], 15))

        # end condition
        endcondition = py_trees.composites.Parallel("Waiting for end position",
                                                    policy=py_trees.common.ParallelPolicy.SUCCESS_ON_ALL)
        endcondition_part1 = InTriggerDistanceToVehicle(self.other_actors[0],
                                                        self.ego_vehicles[0],
                                                        distance=20,
                                                        name="FinalDistance")
        endcondition_part2 = StandStill(self.ego_vehicles[0], name="FinalSpeed", duration=1)
        endcondition.add_child(endcondition_part1)
        endcondition.add_child(endcondition_part2)

        # Build behavior tree
        sequence = py_trees.composites.Sequence("Sequence Behavior")
        sequence.add_child(ActorTransformSetter(self.other_actors[0], self._first_actor_transform))
        sequence.add_child(ActorTransformSetter(self.other_actors[1], self._second_actor_transform))
        sequence.add_child(driving_to_next_intersection)
        sequence.add_child(StopVehicle(self.other_actors[0], self._other_actor_max_brake))
        sequence.add_child(TimeOut(3))
        sequence.add_child(obstacle_clear_road)
        sequence.add_child(stop_near_intersection)
        sequence.add_child(StopVehicle(self.other_actors[0], self._other_actor_max_brake))
        sequence.add_child(endcondition)
        sequence.add_child(ActorDestroy(self.other_actors[0]))
        sequence.add_child(ActorDestroy(self.other_actors[1]))

        return sequence

    def _create_test_criteria(self):
        """
        A list of all test criteria will be created that is later used
        in parallel behavior tree.
        """
        criteria = []

        collision_criterion = CollisionTest(self.ego_vehicles[0])

        criteria.append(collision_criterion)

        return criteria

    def __del__(self):
        """
        Remove all actors upon deletion
        """
        self.remove_all_actors()


class FollowLeadingVehicleRoute(BasicScenario):

    """
    This class is the route version of FollowLeadingVehicle where the backgrounda activity is used,
    instead of spawning a specific vehicle and making it brake.

    This is a single ego vehicle scenario
    """

    timeout = 120            # Timeout of scenario in seconds

    def __init__(self, world, ego_vehicles, config, randomize=False, debug_mode=False, criteria_enable=True,
                 timeout=60):
        """
        Setup all relevant parameters and create scenario
        """
        self.timeout = timeout
        self._stop_duration = 15
        self._end_time_condition = 30

        super(FollowLeadingVehicleRoute, self).__init__("FollowLeadingVehicleRoute",
                                                        ego_vehicles,
                                                        config,
                                                        world,
                                                        debug_mode,
                                                        criteria_enable=criteria_enable)

    def _initialize_actors(self, config):
        """
        Custom initialization
        """
        pass

    def _create_behavior(self):
        """
        Uses the Background Activity API to force a hard break on the vehicles in front of the actor,
        then waits for a bit to check if the actor has collided.
        """
        sequence = py_trees.composites.Sequence("FollowLeadingVehicleRoute")
        sequence.add_child(Scenario2Manager(self._stop_duration))
        sequence.add_child(Idle(self._end_time_condition))

        return sequence

    def _create_test_criteria(self):
        """
        A list of all test criteria will be created that is later used
        in parallel behavior tree.
        """
        criteria = []
        criteria.append(CollisionTest(self.ego_vehicles[0]))

        return criteria

    def __del__(self):
        """
        Remove all actors upon deletion
        """
        self.remove_all_actors()
