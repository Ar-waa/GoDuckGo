from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

obstacles={'stop':False}
obs_flag=True
player_pos=[400,20] #x,y
lives=3
score=0
level=0

#Green car variables (Arwa)
green_level = random.randint(1,10)

# Spike-related variables (Arwa)
spikes = []
spike_timer = time.time()
spike_stop = False
SPIKE_INTERVAL = 3  # Spikes appear every 3 seconds
SPIKE_DURATION = 3  # Spikes remain visible for 3 seconds

#Invincibility (Mahin)
plus_obstacles = []  # List to hold "+" obstacles
invincible_timer = 0  # Timer to track invincibility
is_invincible = False  # Flag to track if player is invincible
plus_timer = 3  # Time duration for invincibility (3 seconds)
shield_active = False
shield_start_time = 0

# Track the time of last spawn for "+" obstacle
plus_last_spawn_time = 0
plus_spawn_interval = 10  # 15 seconds interval between each "+" spawn
plus_duration= 5

# Heart-related variables #(Mahin)
hearts = []  # List to hold heart obstacles
heart_spawn_interval=10
heart_last_spawn_time=0
heart_timer = time.time()  # Timer to manage heart spawning  # Hearts appear every 10 seconds
HEART_DURATION = 5  # Hearts remain visible for 5 seconds

def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(abs(x), abs(y))
    glEnd()

def controller_circle(x, y, r):
    zone1_points = midpoint_circle(r)
    whole_circle = create_whole_circle(zone1_points)
    for i in whole_circle:
        draw_point(i[0] + x, i[1] + y)
    #for i in whole_circle:
        i[0]+=x
        i[1]+=y
    return whole_circle

def midpoint_circle(r):
    d = 1 - r
    x = 0
    y = r
    intermediate = [[x, y]]
    
    while x <= y:
        if d >= 0:
            x += 1
            y -= 1
            intermediate.append([x, y])
            d = d + 2 * x - 2 * y + 5
        else:
            x += 1
            d = d + 2 * x + 3
            intermediate.append([x, y])
    
    return intermediate

def create_whole_circle(zone1_points):
    all_points = []

    for point in zone1_points:
        x, y = point
        # Octant 1
        all_points.append([x, y])
        # Octant 2
        all_points.append([-x, y])
        # Octant 3
        all_points.append([y, -x])
        # Octant 4
        all_points.append([-y, -x])
        # Octant 5
        all_points.append([-x, -y])
        # Octant 6
        all_points.append([x, -y])
        # Octant 7
        all_points.append([-y, x])
        # Octant 0
        all_points.append([y, x])
    return all_points

def midpoint_line(points):
    if points[0][0] >= points[1][0]:
        points[0], points[1] = points[1], points[0]  

    dx = points[1][0] - points[0][0]
    dy = points[1][1] - points[0][1]
    d = dy - (dx // 2)
    x = points[0][0]
    y = points[0][1]
    intermediate = [[x, y]]
    
    while x < points[1][0]:
        x += 1
        if d < 0:
            d += dy
        else:
            y += 1
            d += dy - dx
        intermediate.append([x, y])
    
    return intermediate

def controller_line(points):
    list1 = []
    square = [[-10, -10], [-10, 10], [10, 10], [10, -10]]  

    for i in range(len(points) - 1):
        zone = decide_zone([points[i], points[i + 1]])
        convert = converttozero([points[i], points[i + 1]], zone)
        interpoint = midpoint_line(convert)
        zonepoint = returntooriginal(interpoint, zone)
        
        list1.extend(zonepoint)


    zone = decide_zone([points[-1], points[0]])
    convert = converttozero([points[-1], points[0]], zone)
    interpoint = midpoint_line(convert)
    zonepoint = returntooriginal(interpoint, zone)
    list1.extend(zonepoint)

    for j in square:
        list1.append(j)
    for j in list1:
        draw_point(j[0], j[1])
    return points

def decide_zone(decide):
    dx=decide[0][0]-decide[1][0]
    dy=decide[0][1]-decide[1][1]
    if dx>0 and dy>=0 and abs(dx) >= abs(dy):
        return 0
    elif dx>=0 and dy>0 and abs(dx) < abs(dy):
        return 1
    elif dx<0 and dy>=0 and abs(dx) <= abs(dy):
        return 2
    elif dx<=0 and dy>0 and abs(dx) > abs(dy):
        return 3
    elif dx<0 and dy<=0 and abs(dx) >= abs(dy):
        return 4
    elif dx<=0 and dy<0 and abs(dx) < abs(dy):
        return 5

    elif dx>0 and dy<=0 and abs(dx) <= abs(dy):
        return 6

    elif dx>=0 and dy<0 and abs(dx) > abs(dy):
        return 7

def converttozero(zeroth,a):
    zeroth = [point[:] for point in zeroth] 
    if a==0:
        zeroth[0][0],zeroth[0][1]=zeroth[0][0],zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=zeroth[1][0],zeroth[1][1]
        return zeroth
    
    elif a==1:
        zeroth[0][0],zeroth[0][1]=zeroth[0][1],zeroth[0][0]
        zeroth[1][0],zeroth[1][1]=zeroth[1][1],zeroth[1][0]
        return zeroth

    elif a==2:
        zeroth[0][0],zeroth[0][1]=zeroth[0][1],zeroth[0][0]*-1
        zeroth[1][0],zeroth[1][1]=zeroth[1][1],-1*zeroth[1][0]
        return zeroth

    elif a==3:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][0],zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][0],zeroth[1][1]
        return zeroth

    elif a==4:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][0],-1*zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][0],-1*zeroth[1][1]
        return zeroth

    elif a==5:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][1],-1*zeroth[0][0]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][1],-1*zeroth[1][0]
        return zeroth

    elif a==6:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][1],zeroth[0][0]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][1],zeroth[1][0]
        return zeroth

    elif a==7:
        zeroth[0][0],zeroth[0][1]=zeroth[0][0],-1*zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=zeroth[1][0],-1*zeroth[1][1]
        return zeroth
    
def returntooriginal(points, zone):
    if zone == 0:
        return points  
    elif zone == 1:
        return [[point[1], point[0]] for point in points]

    elif zone == 2:
        return [[point[1], -point[0]] for point in points]

    elif zone == 3:
        return [[-point[0], point[1]] for point in points]

    elif zone == 4:
        return [[-point[0], -point[1]] for point in points]

    elif zone == 5:
        return [[-point[1], -point[0]] for point in points]

    elif zone == 6:
        return [[-point[1], point[0]] for point in points]

    elif zone == 7:
        return [[point[0], -point[1]] for point in points]

# Helper function to draw text at specific coordinates (Mahin)
def draw_text(x, y, text, color, size):
    glColor3f(*color)  # Set color for the text
    glRasterPos2f(x, y)  # Set position for text rendering
    
    # Loop through each character in the text and render it
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))  # You can change the font size if needed

def generate_spikes(): #(Arwa)
    global spikes
    spikes = []  # Clear old spikes
    for level in range(2,10):
        if random.choice([True, False]):  # Randomly decide if a spike appears
            x = random.randint(0, 800)  # Random x position
            y = level * 40  # Spike level (aligned with platforms)
            spikes.append({'x': x, 'y': y, 'level': level})

def draw_spikes(): #(Arwa)
    global spikes
    glColor3f(1, 0, 0) 
    for spike in spikes:
        controller_line([[spike['x'], spike['y']], [spike['x']-10, spike['y']-20], [spike['x']+10, spike['y']-20]])

def generate_obstacle(level): #(Mahin)
    global obstacles
    x = random.randint(50, 750)  
    y = level * 40 
    if score<=10:
        velocity=10
    elif score>=30:
        velocity=score/2
    elif 15<score<29:
        velocity=15
    else:
        velocity=score
    obstacles[level] = {"points": [[x,y+5],[x,y+35],[x-50,y+35],[x-50,y+5]], "velocity": velocity}

def generate_plus_obstacles(): #(Mahin)
    global plus_obstacles,plus_last_spawn_time
        # Check if enough time has passed to spawn a new "+"
    if time.time() - plus_last_spawn_time >= plus_spawn_interval:
        # If so, clear the previous "+" obstacles
        plus_obstacles.clear()

        for level in range(2,10):
            if random.choice([True, False]):  # Randomly decide if a "+" appears
                x = random.randint(0, 800)
                y = level* 40
                plus_obstacles.append({'x': x, 'y': y, 'timer': time.time()})
                plus_last_spawn_time = time.time()  # Update the last spawn time
                break

def draw_plus_obstacles(): #(Mahin)
    global plus_obstacles
    glColor3f(0, 1, 0)  # Color for the "+" obstacles
    for plus in plus_obstacles:
        draw_text(plus['x'], plus['y'], "+", (0, 1, 0), 20)

def update_shield(): #(Mahin)
    global shield_active
    if shield_active and time.time() - shield_start_time > 3:  # Shield duration is 3 seconds
        shield_active = False  # Deactivate the shield
        print("Shield deactivated.")

def draw_heart():  # Function to draw a heart shape using GL_POINTS #(Mahin)
    glColor3f(1, 0, 0)  # Set the color to red
    for heart in hearts:
        draw_text(heart['x'], heart['y'], "<3", (1, 0, 0), 30)
    #glBegin(GL_POINTS)  # Begin drawing points
    #for t in range(0, 360):  # Loop through angles (0 to 360 degrees)
        #angle = t * (3.14159 / 180)  # Convert to radians
        # Parametric equations for the heart shape
        #r = 10  # Size scaling factor
        #x_heart = x + r * 16 * (sin(angle) ** 3)  # X-coordinate
        #y_heart = y + r * (13 * cos(angle) - 5 * cos(2 * angle) - 2 * cos(3 * angle) - cos(4 * angle))  # Y-coordinate
        #glVertex2f(x_heart, y_heart)  # Plot the point
    #glEnd()

#def draw_hearts():  # Function to render hearts on the screen
    #for heart in hearts:
        #draw_heart(heart['x'], heart['y'])

def generate_hearts():  # Function to randomly generate heart obstacles
    global hearts,heart_last_spawn_time
    if time.time() - heart_last_spawn_time >= heart_spawn_interval:
        # If so, clear the previous "hearts" obstacles
        hearts.clear()
    for level in range(2,10):
            if random.choice([True, False]):  # Randomly decide if a spike appears
                x = random.randint(0, 800)  # Random x position
                y = level * 40  # Spike level (aligned with platforms)
                hearts.append({'x': x, 'y': y, 'timer': time.time()})
                break

def specialKeyListener(key, x, y):
    global player_pos,score
    if not obstacles['stop']:
        if key==GLUT_KEY_UP:
            player_pos[0]+=0
            player_pos[1]+=40
            score+=1
            print('Score:', score, 'Lives:', lives)
            
        if key== GLUT_KEY_DOWN:		
            player_pos[0]+=0
            player_pos[1]-=40
            score=score-1
            
        if key==GLUT_KEY_RIGHT:
            player_pos[0]+=40
            player_pos[1]+=0
            
        if key==GLUT_KEY_LEFT:
            player_pos[0]-=40
            player_pos[1]+=0
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global spike_stop, obstacles,obs_flag, player_pos, lives, score, green_level
    # Pause/Play logic
    if key==b' ':
        if spike_stop:
            spike_stop = False
        else:
            spike_stop = True
        if not obstacles['stop']:
            obstacles['stop'] = True
        else:
            obstacles['stop'] = False

    # Restart button        
    if key==b"r":
        green_level = random.randint(1, 10)
        obstacles = {'stop': False}
        obs_flag = True
        player_pos = [400, 20]
        lives = 3
        score = 0
        print('Starting Over')
    
    #Exit button
    if key==b"\033":
        glutDestroyWindow(glutGetWindow())

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global obstacles, obs_flag, player_pos, lives, score, green_level, spike_stop
    
    # Restart button
    if 300 <= x <= 500 and 140 <= -1 * (y - 500) <= 160 or 10<=x<=50 and 470<=-1*(y-500)<=490:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            green_level = random.randint(1, 10)
            obstacles = {'stop': False}
            obs_flag = True
            player_pos = [400, 20]
            lives = 3
            score = 0
            print('Starting Over')
            
    # Pause/Play logic
    elif 395 <= x <= 405 and 470 <= -1 * (y - 500) <= 490 and lives!=0:
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                if spike_stop:
                    spike_stop = False
                else:
                    spike_stop = True
                if not obstacles['stop']:
                    obstacles['stop'] = True
                else:
                    obstacles['stop'] = False

    # Exit button
    elif (700 <= x <= 800 and 80 <= -1 * (y - 500) and lives!=0) or (300 <= x <= 500 and 90 <= -1 * (y - 500) and lives==0):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            print("Goodbye")
            print("Final Score:", score, ' Live(s):', lives)
            glutDestroyWindow(glutGetWindow())
    glutPostRedisplay()

def retry():
    global player_pos,obstacles,obs_flag,score
    obstacles={'stop':False}
    obs_flag=True
    player_pos=[400,20]
    
def check_collision(player):
    global player_pos,obstacles,lives,score, green_level, is_invincible, shield_active, shield_start_time

    if is_invincible or shield_active:
        return  # Skip collision check if player is invincible
    for k, v in obstacles.items():
        if k!='stop':
            val = v['points']
            
            if val[0][0] >= player_pos[0]+10 >= val[3][0]or val[0][0] >= player_pos[0]-10 >= val[3][0]:
                
                if val[0][1] <= player_pos[1]+10 <= val[2][1] and k==green_level:
                    obstacles['stop']=False
                    score+=3
                    player_pos[1]+=40
                    green_level = 0
                    print("Plus Points!")
                    print('Score:', score, 'Live(s):', lives)
                    return
                    
                
                elif val[0][1] <= player_pos[1]+10 <= val[2][1]:
                    obstacles['stop']=True
                    lives-=1
                    green_level = random.randint(1,10)
                    print("Collision detected!")
                    print('Score:', score, 'Live(s):', lives)
                    retry()
                    return 
    if score >= 100:
        print('You have Won!!!')
        print("Final Score:", score, ' Live(s):', lives)

def check_spike_collision(player): #(Arwa)
    global spikes, score
    px, py = player_pos
    for spike in spikes:
        sx, sy = spike['x'], spike['y']
        if sx - 20 <= px <= sx + 20 and sy - 25 <= py <= sy:
            score -= 3
            print("Spike collision! -3 points.")
            print('Score:', score, 'Lives:', lives)
            retry()
            break
    if score >= 100:
        print('You have Won!!!')
        print("Final Score:", score, ' Live(s):', lives)

def check_plus_obstacle_collision(player):
    global plus_obstacles, is_invincible, invincible_timer,shield_active, shield_start_time
    px, py = player_pos
    for plus in plus_obstacles:
        sx, sy = plus['x'], plus['y']
        if sx - 20 <= px <= sx + 20 and sy - 20 <= py <= sy + 20:
            is_invincible = True
            #active sheild
            if not shield_active:  # Activate only if not already active
                    shield_active = True
                    #invincible_timer = time.time()  # Start invincibility timer
                    shield_start_time = time.time()  # Record activation time
                    print("Shield activated!")
            else:
                print("Shield is already active.")
            invincible_timer = time.time()  # Start invincibility timer
            print("Invincibility activated!")
            plus_obstacles.remove(plus)  # Remove the "+" obstacle after collision
            break

def check_heart_collision(player):  # Check collision with hearts
    global hearts, lives
    px, py = player
    for heart in hearts:
        hx, hy = heart['x'], heart['y']
        # Simple collision detection using distance
        if hx - 20 <= px <= hx + 20 and hy - 20 <= py <= hy + 20:  # 400 = 20^2 (radius squared)
            lives += 1  # Increase lives
            print("Heart collision! Lives increased.")
            hearts.remove(heart)  # Remove heart after collision
            break

def animation():
    global obstacles,spike_timer, spike_stop,is_invincible, invincible_timer, plus_timer,plus_last_spawn_time, plus_spawn_interval,heart_timer,HEART_DURATION

    if is_invincible:
        elapsed_time = time.time() - invincible_timer
        if elapsed_time >= 3:  # 3 seconds duration
            is_invincible = False  # Turn off invincibility
            print("Invincibility ended!")
    # Handle heart spawning and expiration
    if time.time() - heart_timer > 10:
        generate_hearts()
        heart_timer = time.time()  # Reset the timer

    # Remove hearts after their duration
    if time.time() - heart_timer > HEART_DURATION:
            hearts.clear()

    # Update spike appearance based on time
    if spike_stop == False:
        if time.time() - spike_timer > SPIKE_INTERVAL:
            generate_spikes()
            spike_timer = time.time()

        # Remove spikes after their duration
        if time.time() - spike_timer > SPIKE_DURATION:
            spikes.clear()
    
    # Generate "+" obstacles every 10 seconds
    if time.time() - plus_timer > 10:  # Every 10 seconds
        generate_plus_obstacles()
        plus_timer = time.time()  # Reset the timer
    
    #Remove "+" after their duration
    if time.time() - plus_timer > plus_duration:
            plus_obstacles.clear()

    if not obstacles['stop']:
        for k,v in obstacles.items():
            
            if k!='stop':
                point=v['points']
                
                if point[0][0]>=800 :
                    v['velocity']=v['velocity']*-1
                    
                if point[3][0]<=0:
                    v['velocity']=v['velocity']*-1
                    
        for i, k in obstacles.items():
            if i!='stop':
                
                if k['points'][0][0]<=800 or k['points'][3][0]>=0:
                    
                    for point in k['points']:
                        point[0] += k["velocity"]

    if 800<player_pos[0]:
        player_pos[0] = 400
    if player_pos[0]<0:
        player_pos[0] = 250
    update_shield() # Ensure shield status is updated
    glutPostRedisplay()

def showScreen():
    global obstacles, obs_flag, player_pos, score, lives, green_level, spike_stop, plus_obstacles,shield_active
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # BUTTONS (Arwa)
    # Reset button
    glColor3f(0.1, 0.5, 0.7)
    reset = controller_line([[30, 490], [10, 480], [30, 470], [10, 480], [50, 480], [10, 480]])

    # Pause/Play button
    glColor3f(1, 0.5, 0)
    if not obstacles['stop']:
        pause = controller_line([[395, 490], [395, 470]])
        pause = controller_line([[405, 490], [405, 470]])
    else:
        play = controller_line([[395, 490], [405, 480], [395, 470]])

    # Exit button
    glColor3f(1, 0, 0)
    exit = controller_line([[770, 490], [790, 470]]) 
    exit = controller_line([[770, 470], [790, 490]])

    # If game over
    if lives == 0:
        # Display "Game Over" message
        glColor3f(1, 0, 0)  # Red color
        draw_text(320, 250, "GAME OVER", (1, 0, 0), 30)
        draw_text(320, 200, f"Final Score: {score}", (1, 1, 1), 15)
        
        # Restart and Exit buttons
        # Restart button
        glColor3f(0.1, 0.5, 0.7)
        draw_text(330, 150, "RESTART", (0, 1, 0), 15)
        
        # Exit button
        glColor3f(1, 0, 0)
        draw_text(350, 90, "EXIT", (0, 0, 1), 15)

    else:
        # Existing game logic if not game over
        iteration()
        glColor3f(0.5, 0.5, 0.8)
        
        # Creating roads and obstacles
        x = 40
        for level in range(1, 11):
            level_coords = controller_line([[0, x], [800, x]])
            x += 40
            if obs_flag:
                generate_obstacle(level)
        obs_flag = False
        
        # Creating obstacles
        for i, j in obstacles.items():
            if i != 'stop' and (i != green_level or green_level == 0):
                glColor3f(1, 1, 1)
                cars = controller_line(j['points'])
            elif i != 'stop' and i == green_level:
                glColor3f(0, 1, 0)
                cars = controller_line(j['points'])
        
        # Creating player and other objects
        if lives != 0:
            glColor3f(0 , 1, 1)
            player = controller_circle(player_pos[0], player_pos[1], 10)

        # Draw shield if active
        if shield_active and time.time() - shield_start_time <= 3:
            glColor3f(0, 0, 1)  # Shield color (blue)
            controller_circle(player_pos[0], player_pos[1], 15)

        # Draw spikes
        draw_spikes()
        draw_plus_obstacles()
        draw_heart()

        # Check for collisions and update score
        check_plus_obstacle_collision(player)
        check_heart_collision(player_pos)
        check_spike_collision(player)
        check_collision(player)

        # Update score and lives on screen
        draw_text(690, 445, f"Score: {score}", (1, 1, 1), 13)
        draw_text(690, 470, f"Lives: {lives}", (1, 1, 1), 13)
        #if score==
            #level=level+1
        #draw_text(690, 470, f"Level: {level}", (1, 1, 1), 13)

        if player_pos[1] >= 410:
            retry()
        elif player_pos[0] <= 0 or player_pos[0] >= 800 or player_pos[1]<20:
            if player_pos[1]<20:
                score = 0
                retry()
            else:
                retry()
        if lives == 0:
            obstacles['stop'] = True
            print("You have lost all your lives")
            print('Final Score:', score)
            #glutLeaveMainLoop()

    glutSwapBuffers()

def iteration():
    glViewport(0, 0, 800, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 500) 
glutInitWindowPosition(100, 100)
wind = glutCreateWindow(b"Go Duck Go") 
glutDisplayFunc(showScreen)
glutIdleFunc(animation)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()