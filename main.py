#---------------------------------------
# Welcome to Alter Life RPG
#---------------------------------------

# Define Alteregos
alterego_first = {
    "name": "First",
    "level": 1,
    "xp": 0,
    "health": 100
}

alterego_second = {
    "name": "Second",
    "level": 1,
    "xp": 0,
    "health": 100
}

alterego_third = {
    "name": "Third",
    "level": 1,
    "xp": 0,
    "health": 100
}

alterego_four = {
    "name": "Four",
    "level": 1,
    "xp": 0,
    "health": 100
}

alterego_five = {
    "name": "Five",
    "level": 1,
    "xp": 0,
    "health": 100
}

# Define some sample quests
quests = [
    {"title": "Organize your room", "xp_reward": 10, "completed": False},
    {"title": "Read a chapter of a book", "xp_reward": 15, "completed": False},
    {"title": "Exercise for 30 minutes", "xp_reward": 20, "completed": False}
]

# Function to complete a quest
def complete_quest(alterego, quest):
    if not quest["completed"]:
        quest["completed"] = True
        alterego["xp"] += quest["xp_reward"]
        print(f"{alterego['name']} completed '{quest['title']}'! +{quest['xp_reward']} XP")
    else:
        print(f"'{quest['title']}' already completed by {alterego['name']}")

## Show initial XP for first alterego
print(f"Before quest: {alterego_first['name']} - XP: {alterego_first['xp']}")

# Complete the first quest
complete_quest(alterego_first, quests[0])

# Show XP after quest
print(f"After quest: {alterego_first['name']} - XP: {alterego_first['xp']}")
