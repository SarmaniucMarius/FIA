class Asteroid(Sprite):
    def __init__(self, pos, vel, acceleration, ang, ang_vel, image, info, sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, sound)
        self.vel = vector2_mul(angle_to_vector(ang), INIT_ROCK_SPEED)
        self.acceleration = [acceleration[0], acceleration[1]]
        self.asteroids_perception_radius = 50
        self.obstacle_perception_radius = 130
        self.fov = PI - 0.5 # field of view in radians
        self.MAX_SPEED = INIT_ROCK_SPEED
        self.MIN_SPEED = INIT_ROCK_SPEED-0.1

    def draw(self, canvas):
        #
        #         * <---- forward
        #        / \
        #       /   \
        #      *_____* <-- p1
        #      ^---------- p2
        #
        p0 = vector2_mul(angle_to_vector(self.angle),            10)
        p1 = vector2_mul(angle_to_vector(self.angle + self.fov), 10)
        p2 = vector2_mul(angle_to_vector(self.angle - self.fov), 10)
        world_p0 = vector2_add(p0, self.pos)
        world_p1 = vector2_add(p1, self.pos)
        world_p2 = vector2_add(p2, self.pos)
        canvas.draw_polygon([world_to_canvas(world_p0), world_to_canvas(world_p1), world_to_canvas(world_p2)], 12, 'Aqua')

        # if self.animated:
        #     new_image_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
        #     canvas.draw_image(self.image, new_image_center, self.image_size, [pos_in_canvas_x, pos_in_canvas_y], self.image_size, self.angle)
        # else:
        #     canvas.draw_image(self.image, self.image_center, self.image_size, [pos_in_canvas_x, pos_in_canvas_y], self.image_size, self.angle)

        if debug_info is True:
            # Drawing a line that shows sprite's moving direction
            line_p0 = vector2_add(self.pos, vector2_mul(self.vel, 20))
            canvas.draw_line(world_to_canvas(self.pos), world_to_canvas(line_p0), 2, 'Red')
            
            # Drawing perception circles
            canvas.draw_circle(world_to_canvas(self.pos), self.obstacle_perception_radius, 2, 'Blue')
            canvas.draw_circle(world_to_canvas(self.pos), self.asteroids_perception_radius, 2, 'Green')        

    def dodge_obstacles(self, obstacles):
        steering = [0, 0]
        for obstacle in obstacles:
            object_distance = vector2_dist(self.pos, obstacle.pos)
            if object_distance <= self.obstacle_perception_radius:
                diff = vector2_sub(self.pos, obstacle.pos)
                steering = vector2_mul(vector2_normalize(diff), self.MAX_SPEED)
                steering = vector2_sub(steering, self.vel)
                steering = vector2_limit(steering, DODGE_FORCE)

        self.acceleration = vector2_add(self.acceleration, steering)

    def alignment(self, asteroids):
        steering = [0, 0]
        asteroids_in_radius = 0.0
        for asteroid in asteroids:
            if asteroid is self:
                continue

            asteroid_distance = vector2_dist(self.pos, asteroid.pos)
            if asteroid_distance <= self.asteroids_perception_radius:
                asteroids_in_radius += 1
                steering = vector2_add(steering, asteroid.vel)

        if asteroids_in_radius > 0:
            steering = vector2_mul(steering, 1.0/asteroids_in_radius)
            steering = vector2_mul(vector2_normalize(steering), self.MAX_SPEED)
            steering = vector2_sub(steering, self.vel)
            steering = vector2_limit(steering, ALIGNMENT_FORCE)

        return steering

    def cohesion(self, asteroids):
        steering = [0.0, 0.0]
        asteroids_in_radius = 0.0
        for asteroid in asteroids:
            if asteroid is self:
                continue

            asteroid_distance = vector2_dist(self.pos, asteroid.pos)
            if asteroid_distance <= self.asteroids_perception_radius:
                asteroids_in_radius += 1.0
                steering = vector2_add(steering, asteroid.pos)
        
        if asteroids_in_radius > 0.0:
            steering = vector2_mul(steering, 1.0 / asteroids_in_radius)
            steering = vector2_sub(steering, self.pos)
            steering = vector2_mul(vector2_normalize(steering), self.MAX_SPEED)
            steering = vector2_sub(steering, self.vel)
            steering = vector2_limit(steering, COEHISION_FORCE)
            
        return steering

    def separation(self, asteroids):
        steering = [0.0, 0.0]
        asteroids_in_radius = 0.0
        for asteroid in asteroids:
            if asteroid is self:
                continue


            asteroid_distance = vector2_dist(self.pos, asteroid.pos)
            if asteroid_distance <= self.asteroids_perception_radius:
                asteroids_in_radius += 1.0
                diff = vector2_sub(self.pos, asteroid.pos)
                diff = vector2_mul(diff, 1/asteroid_distance)
                steering = vector2_add(steering, diff)
        
        if asteroids_in_radius > 0.0:
            steering = vector2_mul(steering, 1.0 / asteroids_in_radius)
            steering = vector2_mul(vector2_normalize(steering), self.MAX_SPEED)
            steering = vector2_sub(steering, self.vel)
            steering = vector2_limit(steering, SEPARATION_FORCE)
        
        return steering

    def attack(self, ship, asteroids):
        steering = vector2_normalize(vector2_sub(ship.pos, self.pos))
        steering = vector2_sub(steering, self.vel)
        self.acceleration = vector2_add(self.acceleration, steering)
        
    def update_acceleration(self, asteroids):
        self.acceleration = vector2_add(self.acceleration, self.alignment(asteroids))
        self.acceleration = vector2_add(self.acceleration, self.cohesion(asteroids))
        self.acceleration = vector2_add(self.acceleration, self.separation(asteroids))

    def update(self, asteroids):
        self.pos = vector2_add(self.pos, self.vel)
        self.pos = keep_in_bounds(self.pos)
        
        self.vel = vector2_add(self.vel, self.acceleration)
        if vector2_length(self.vel) > self.MAX_SPEED:
            self.vel = vector2_mul(vector2_normalize(self.vel), self.MAX_SPEED)
        if vector2_length(self.vel) < self.MIN_SPEED:
            self.vel = vector2_mul(vector2_normalize(self.vel), self.MIN_SPEED)
        self.acceleration = [0, 0]
            
        self.angle = vector_to_angle(self.vel) 
        self.age   += 1
        
        # return True if the sprite is old and needs to be destroyed
        if self.age < self.lifespan: 
            return False
        else:
            return True
