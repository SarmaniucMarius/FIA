# Floking simulation
A system that can train pilots. It simulates the behaviour of so called Solanum tuberosum creatures. They show flocking behaviour when undisturbed. And they evade obstacles that can crush them.

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)

## General info
The simulation contains a ship and a couple of Solanum tuberosums (that will sometimes be called boids) that are represented as blueish triangles. It creates boids at random places. After some time this boids will organise into flocks. Also the user can place a boid at some specific place by clicking with the left button of the mouse.

There are two modes in the simulation: flocking and attacking. In flocking mode Solanum tuberosum will exhibit bird like behavior and will dodge any missile or ship. While in attacking mode it will follow the ship to destroy it at the cost of it’s own life.

## Screenshots
Below you can see a screen from the simulation

![Forward Chaining](simulation_screen.JPG)

## Technologies
1. Python 2.7
2. Codeskulptor

## Setup
The code should be run on [codeskulptor]. (http://www.codeskulptor.org/)

## Features
* Floking behaviour
* Evading behaviour
* Attacking behaviour