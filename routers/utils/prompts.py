TRAINING_PROMPT_LEGIT = f"""The following image is a screenshot of a person playing the video game Tom Clancy's Rainbow Six Siege. 
They are not using any game modifying software or programs to cheat. 
This is a legitimate way to play the game, take note as to what there character looks like and what they are able to see in the game as this is a legitimate POV.
"""

TRAINING_PROMPT_CHEAT = f"""The following image is a screenshot of a person playing the video game Tom Clancy's Rainbow Six Siege in which they are using a game cheat called ESP (Visual software/program to aid in seeing things in-game that normal users would not be able to see).
Notice how the person is able to see the enemy's location through the walls and other objects in the game. More uncommon in cheats, we can see that there own character is colored a light blue which is not normal.
"""

BASE_PROMPT = f"""The following image is a screenshot of a person playing the video game Tom Clancy's Rainbow Six Siege that you need to analyze. 
Based on the information I previously provided you as context, analyze the image and answer the following question: 
Is the person shown playing the game in the screenshot using ESP (Visual software/program to aid in seeing things in-game that normal users would not be able to see)? 
Response True if the person is using ESP, and False if they are not.
"""