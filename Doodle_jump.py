'''
Purpose: This turtle program is based on a mobile game called Doodle Jump. The goal of this game is to try and jump on the closest platform that you find near you. As you get higher by jumping on each platform, you will earn points based on the distance of your jump. If you miss your jump, you will fall and the game will be over.

Controls: "Left" key to go left
          "Right" key to go right

Author: Ilia 
Code reviewer: Ryan Daryani
Date created: 2019-10-02
Date modified: 2019-10-19
'''

import turtle
from functools import partial
from random import randint, randrange
from math import sqrt, pow

COLLISION_DISTANCE = 40


def game_setup():   #Game setup function
    '''Setting up the game for the main game loop'''


    #Registering picture for the shape of the turtle. Pictures are located in the main folder directory.
    turtle.register_shape('textures/doodle.gif')
    turtle.register_shape('textures/doodle_left.gif')
    turtle.register_shape('textures/doodle_platforms.gif')
    turtle.register_shape('textures/moving_platform.gif')
    turtle.register_shape('textures/critical_platform.gif')
    turtle.register_shape('textures/broken_platform.gif')


    #setting up the window
    window = turtle.Screen()
    window.setup(width = 540, height = 850)
    window.bgpic('textures/doodle_jump_background.gif')
    window.tracer(0)


    #setting up the player
    player = turtle.Turtle()
    player.shape('textures/doodle.gif')
    player.penup()
    player.color('red')
    player.speed(0)
    player.goto(-200, 80)
    player.dy = 0
    player.dx = 0


    #Setting up the score board
    score = turtle.Turtle()
    score.color('black')
    score.speed('fastest')
    score.penup()
    score.hideturtle()


    #A game over message for the end of the game
    game_message = turtle.Turtle()
    game_message.speed("fastest")
    game_message.penup()
    game_message.hideturtle()
    

    #Constansts for the main function
    GRAVITY = 0.00015
    PLAYING = True
    PAUSED = True
    GAME_SCORE = 0
    START_TIME = 3


    return (window, player, score, game_message, GRAVITY, PLAYING, PAUSED, GAME_SCORE, START_TIME)



def move_left(t):   #Moving the player to the left
    '''
    When the player is moving to the left, the change im the x direction will decrease by 0.1.
    while the player is in the left direction, the shape of the players character will also look to the left.
    '''
    t.shape('textures/doodle_left.gif')
    t.dx -= 0.1



def move_right(t):  #Moving the player to the right
    '''
    When the player is moving to the right, the change im the x direction will increase by 0.1.
    while the player is in the right direction, the shape of the players character will also look to the right.
    '''
    t.shape('textures/doodle.gif')
    t.dx += 0.1



def controls(t=None):   #Controls for the keyboard
    if t is None:  # remove event bindings
        turtle.onkeypress(None, 'Left') 
        turtle.onkeypress(None, 'Right')
    else:
        turtle.onkeypress(partial(move_left, t), 'Left')
        turtle.onkeypress(partial(move_right, t), 'Right')
    turtle.listen()  



def character_movement(t, gravity): #movement and fall controll for the player
    '''
    t.dy is the change in the falling direction subracted by 0.00015 each time. 
    That is when the turtle starts to fall after each jump.
    '''
    t.dy -= gravity
    t.sety(t.ycor() + t.dy)
    t.setx(t.xcor() + t.dx)



def random_position(t=None):    #Setting up the turtle in a random position on the screen
    '''
    Any given turtle to this function will be set on a random range on the screen.
    '''
    if t is not None:
        return t.goto(randrange(-270, 270, 20), randrange(50, 525, 50))



def generate_turtles(aNum): #Creating a list of turtles
    '''
    This function will take any number and generate a list of turtles according to the given number and returns the list of turtles.
    '''
    turtles = []
    for i in range(aNum):
        turtles.append(turtle.Turtle())
    return turtles



def object_(t, shape, color=None):  #Setting up a turtles characteristics
    '''
    With object_ you can customize your turtle
    1. t ---> turtle
    2. shape ---> This is taken as a string
    3. color ---> This is taken as a string as an optional perameter.
    '''
    t.penup()
    t.shape(shape)
    t.shapesize(20, 30)
    t.setheading(-90)
    if color is not None:
        t.color(color)



def isCollision(t1, t2):    #Collision between two objects
    '''
    Setting up collision between two objects.
    This function takes two perameters as turtles.    
    '''
    distance = sqrt(pow(t1.xcor() - t2.xcor(), 2) + pow(t1.ycor() - t2.ycor(), 2))
    if distance <= COLLISION_DISTANCE:
        return True
    else:
        return False
   


def turtle_movement(coorr_option ,t, gravity, gravity_x=None, gravity_y=None):  #Moving turtle objects downwards
    '''
    With this function, you can have a turtle move in multiple directions. by the first perameter, you have to option to
    insert "sety" to move along the y-axis, "setx" to move along the x-axis, or "setxy" to move along the x and y axis.
    1. t ---> A turtle
    2. gravity_x ---> the turtle will be moving along the x-axis depending on the speed of the gravity
    3. gravity_y ---> the turtle will be moving along the y-axis depending on the speed of the gravity
    '''
    if coorr_option is 'sety':
        t.dy -= gravity
        t.sety(t.ycor() + t.dy)
    
    elif coorr_option is 'setx':
        t.dx -= gravity
        t.setx(t.xcor() + t.dx)

    elif coorr_option is 'setxy' and gravity_x is not None and gravity_y is not None:
        t.dx -= gravity_x
        t.setx(t.xcor() + t.dx)
        t.dy -= gravity_y
        t.sety(t.ycor() + t.dy)



def dead_zone_boundary(t_rand_pos, condition, boundary, turtle_coor):   #Condition for the turtle when it is outside of the boundary
    '''
    The dead_zone_boundary takes 4 perameters. 
    1. t_rand_pos ---> This will take a turtle as input and spawn it at a different locaiton.
    2. condition ----> this is a string, you can put in "greater_than" or "less_than" inside the perameter.
    3. boundary ----> this can be any number.
    4. turtle_coor ----> this parameter takes the turtle.xcor() or turtle.ycor() as perameter.
    '''
    if condition is 'less_than':
        if turtle_coor < boundary:
            random_position(t_rand_pos)
            return True
        else:
            return False

    elif condition is 'greater_than':
        if turtle_coor > boundary:
            random_position(t_rand_pos)
            return True
        else:
            return False


def hight_score(name, score):
    with open('score_record.txt', 'a') as output:
        for aline in output:
            if aline.split()[0] is name and int(aline.split()[1]) < score:
                output.write(name + '   ' + score + '\n')
            else:
                output.write(name + '   ' + score + '\n')                



def custom_text(text_type, t, font_size, aligned, position_x, position_y, custom_message=None, score_text=None, game_score=None, hide_message=None):    #This function can create a custom message on the screen 
    '''
    score_keeping will print a personalized message or a number on the screen. 9 perameters are taken with three being optional.
    1. text_type ---> Specifying if this is for "letters" or "numbers" in the perameter
    2. t ---> Taking a turtle
    3. font_size ---> Size of the font 
    4. aligned ---> if the text will be on the left, center or right of the screen
    5. custom_message ---> if chosen "letters" then the users input will be printed on the screen
    6. position_x ---> set the text position on the x-axis
    7. position_y ---> set the text position on the y-axis
    8. score_text ---> a text will be set behind the printed number or can be taken as an empty string in the perameter
    9. game_score ---> The number that will be printed on the screen
    '''
    if text_type is 'numbers' and game_score is not None and score_text is not None:
        t.setposition(position_x, position_y)
        scoring = score_text + '%s' %game_score
        t.clear()
        t.write(scoring, False, align = aligned, font = ("Arial", font_size, "normal"))
        if hide_message is not None and hide_message is 'yes':
            t.clear()
        
    if text_type is 'letters' and custom_message is not None:
        t.setposition(position_x, position_y)
        t.write(custom_message, False, align = aligned, font = ("Arial", font_size, "normal"))

        if hide_message is not None and hide_message is 'yes':
            t.clear()
        

    

def main_game(): #The main function where the program gets executed


    #Setting up the game
    (window, player, score, game_message, GRAVITY, PLAYING, PAUSED, GAME_SCORE, START_TIME) = game_setup()
    controls(player)


    #setting up game instructions on the console
    print("'Left' and 'Right' key to turn left or right.\n")
    print("Green platforms will always stand still\n")
    print("Blue platforms will always be moving left and right\n")
    print("Brown platforms are traps and will always break if contacted\n")



    #Generating a list of turtles named as platforms
    platforms = generate_turtles(8)
    moving_platforms = generate_turtles(5)
    critical_platforms = generate_turtles(3)



    #Setting static platforms that dont do anything
    for platform in platforms:
        object_(platform, 'textures/doodle_platforms.gif')
        platform.setx(randrange(-200, 200))
        platform.sety(randrange(-399, 200, 50))
        platform.dy = -40



    #Setting moving platforms to bounce across the x-axis of the screen
    for moving_platform in moving_platforms:
        object_(moving_platform, 'textures/moving_platform.gif')
        moving_platform.sety(-445)
        moving_platform.dy = -40
        moving_platform.dx = 0



    #another static platform which is meant to be a trap for the player 
    for critical_platform in critical_platforms:
        object_(critical_platform, 'textures/critical_platform.gif')
        critical_platform.sety(-445)
        critical_platform.dy = -40



    #The main loop where most of the code is being executed when being played.
    while PLAYING:



        #Due to the many number of turtles being generated on the screen, the frame rate for each animation will slow down. A window tracer is set to update the animation at the beginning of each loop counter. the window.tracer() is set inside the game_setup() function.
        window.update()
        platform.showturtle()


        #settings and instructions for the turtle object which is the green object on the screen
        #-------------------------------------------------------------------------------------------------------------------------#

        #Looping through the list of turtles that were created
        for platform in platforms:
            

            #Before the while playing loop stars, this will let the player to have a chance to be ready by putting the screen on pause for 5 seconds.
            while PAUSED:
                custom_text('numbers', game_message, 20, 'center', 0, 0, None, 'STARTING: ', round(START_TIME, 1), 'yes')
                START_TIME -= 0.001
                if START_TIME < 0:
                    PAUSED = False

            dead_zone_boundary(platform, 'less_than', -425, platform.ycor())
            character_movement(player, GRAVITY)



            #all types of platforms will be affected if this condition is true. In this case, all platforms will move down if collision is true and the players height is above a certain number.
            #on line 220 and 254 use the same technique
            if isCollision(platform, player) and player.ycor() >= -150:
                for platform in platforms:
                    turtle_movement('sety' ,platform, GRAVITY)
                    GAME_SCORE += 1
                    custom_text('numbers', score, 14, 'left', -260, 400, None,  'Points: ', GAME_SCORE)
                    
                for moving_platform in moving_platforms:
                    turtle_movement('sety', moving_platform, GRAVITY)

                for critical_platform in critical_platforms:
                    turtle_movement('sety', critical_platform, GRAVITY)



            #if the player touches any platform except the critical_platform, the player will bounce back up
            if isCollision(platform, player):
                player.dy *= -1
        #-------------------------------------------------------------------------------------------------------------------------#



        #settings and instructions for the turtle object which is the blue object on the screen
        #-------------------------------------------------------------------------------------------------------------------------#
        for moving_platform in moving_platforms:

            dead_zone_boundary(moving_platform, 'less_than', -425, moving_platform.ycor())

            #this turtle is moving on the x-axis at a rate of 0.0015/pixel
            turtle_movement('setx', moving_platform, 0.0015)



            #The same process is used on this line as of line 220
            if isCollision(moving_platform, player) and player.ycor() >= -150:
                for platform in platforms:
                    turtle_movement('sety', platform, GRAVITY)

                for moving_platform in moving_platforms:
                    turtle_movement('sety', moving_platform, GRAVITY)
                    GAME_SCORE += 1
                    custom_text('numbers', score, 14, 'left', -260, 400, None, 'Points: ', GAME_SCORE)

                for critical_platform in critical_platforms:
                    turtle_movement('sety', critical_platform, GRAVITY)


            if isCollision(moving_platform, player):
                player.dy *= -1
                


            #this is the code used to set the moving_platforms to move across the screen
            #if moving_platform is > 270 or < -270:
            if dead_zone_boundary(None, 'greater_than', 270, moving_platform.xcor()):
                moving_platform.dx *= -1

            if dead_zone_boundary(None, 'less_than', -270, moving_platform.xcor()):
                moving_platform.dx *= -1
        #-------------------------------------------------------------------------------------------------------------------------#



        #settings and instructions for the turtle object which is the brown object on the screen
        #-------------------------------------------------------------------------------------------------------------------------#
        for critical_platform in critical_platforms:



            #the critical_platform is used as a trap for the player to fall and possibly end the game.
            #if there is collision between the two objects, the image of this platform will change 
            if isCollision(critical_platform, player):
                critical_platform.shape('textures/broken_platform.gif')

            elif dead_zone_boundary(critical_platform, 'less_than',  -425, critical_platform.ycor()):
                critical_platform.shape('textures/critical_platform.gif')
        #-------------------------------------------------------------------------------------------------------------------------#


        #if the player moves outside to the far right of the screen, then the player will change coordinates and pop out of the left side of the screen.
        if player.xcor() > 280:
            player.setx(-280)



        #if the player moves outside to the far left of the screen, then the player will change coordinates and pop out of the right side of the screen.
        if player.xcor() < -280:
            player.setx(280)



        #This is the bottom border of the screen where it is the dead zone for the player.
        #if this condition is true, a message will be printed on the screen and the player will be hidden.
        if  player.ycor() < -450:
            player.hideturtle()
            custom_text('letters', score, 20, 'center', 0, 0, 'GAME OVER', None, None)
            custom_text('numbers', game_message, 20, 'center', 0, -50, None, 'Scored: ', GAME_SCORE)
            print("Game over")
            PLAYING = False

    window.exitonclick()


def main():
    main_game()

if __name__ == "__main__":
    main()