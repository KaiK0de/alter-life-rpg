#---------------------------------------
# Welcome to Alter Life RPG
#---------------------------------------

#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, date
from typing import Dict, List
import math


class LifeRPG:
    # Main Life RPG game class
    
    def __init__(self):
        self.data_file = "life_rpg_data.json"
        self.player = self.load_data()
        
    def load_data(self) -> Dict:
        """Loads player data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.create_new_player()
        return self.create_new_player()
    
    def create_new_player(self) -> Dict:
        """Creates a new player"""
        return {
            "name": "Adventurer",
            "level": 1,
            "xp": 0,
            "total_xp": 0,
            "stats": {
                "strength": 5,      # Strength (exercise, physical work)
                "intelligence": 5,  # Intelligence (study, reading)
                "charisma": 5,      # Charisma (social, communication)
                "vitality": 5,      # Vitality (health, rest)
                "discipline": 5     # Discipline (habits, consistency)
            },
            "habits": [],
            "quests": [],
            "achievements": [],
            "gold": 0,
            "last_login": str(date.today())
        }
    
    def save_data(self):
        """Saves player data"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.player, f, indent=2, ensure_ascii=False)
    
    def get_xp_for_next_level(self) -> int:
        """Calculates XP needed for next level"""
        level = self.player["level"]
        return int(100 * (level ** 1.5))
    
    def add_xp(self, amount: int):
        """Adds experience to the player"""
        self.player["xp"] += amount
        self.player["total_xp"] += amount
        
        # Check for level up
        xp_needed = self.get_xp_for_next_level()
        if self.player["xp"] >= xp_needed:
            self.level_up()
    
    def level_up(self):
        """Levels up the player"""
        self.player["xp"] -= self.get_xp_for_next_level()
        self.player["level"] += 1
        self.player["gold"] += self.player["level"] * 10
        
        # Stat bonus per level
        for stat in self.player["stats"]:
            self.player["stats"][stat] += 1
        
        return True
    
    def add_stat(self, stat: str, amount: int):
        """Adds points to a stat"""
        if stat in self.player["stats"]:
            self.player["stats"][stat] += amount
            self.save_data()


class Habit:
    """Class to represent a habit"""
    
    def __init__(self, name: str, stat: str, xp_reward: int, difficulty: str = "medium"):
        self.name = name
        self.stat = stat
        self.xp_reward = xp_reward
        self.difficulty = difficulty
        self.streak = 0
        self.total_completions = 0
        self.last_completed = None
        self.created_date = str(date.today())
    
    def to_dict(self) -> Dict:
        """Converts habit to dictionary"""
        return {
            "name": self.name,
            "stat": self.stat,
            "xp_reward": self.xp_reward,
            "difficulty": self.difficulty,
            "streak": self.streak,
            "total_completions": self.total_completions,
            "last_completed": self.last_completed,
            "created_date": self.created_date
        }
    
    @staticmethod
    def from_dict(data: Dict):
        """Creates a habit from a dictionary"""
        habit = Habit(data["name"], data["stat"], data["xp_reward"], data["difficulty"])
        habit.streak = data.get("streak", 0)
        habit.total_completions = data.get("total_completions", 0)
        habit.last_completed = data.get("last_completed")
        habit.created_date = data.get("created_date", str(date.today()))
        return habit


class Quest:
    """Class to represent a quest"""
    
    def __init__(self, name: str, description: str, xp_reward: int, gold_reward: int, 
                 stat_reward: str = None, difficulty: str = "normal"):
        self.name = name
        self.description = description
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.stat_reward = stat_reward
        self.difficulty = difficulty
        self.completed = False
        self.created_date = str(date.today())
    
    def to_dict(self) -> Dict:
        """Converts quest to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "stat_reward": self.stat_reward,
            "difficulty": self.difficulty,
            "completed": self.completed,
            "created_date": self.created_date
        }
    
    @staticmethod
    def from_dict(data: Dict):
        """Creates a quest from a dictionary"""
        quest = Quest(
            data["name"], 
            data["description"], 
            data["xp_reward"],
            data["gold_reward"],
            data.get("stat_reward"),
            data.get("difficulty", "normal")
        )
        quest.completed = data.get("completed", False)
        quest.created_date = data.get("created_date", str(date.today()))
        return quest


class LifeRPGGUI:
    """Life RPG graphical interface"""
    
    def __init__(self):
        self.game = LifeRPG()
        self.root = tk.Tk()
        self.root.title("Life RPG - Turn your life into a game!")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        # Styles
        self.setup_styles()
        
        # Create interface
        self.create_widgets()
        
        # Update interface
        self.update_display()
    
    def setup_styles(self):
        """Sets up interface styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg_dark = "#1a1a2e"
        bg_medium = "#16213e"
        bg_light = "#0f3460"
        accent = "#e94560"
        text_color = "#ffffff"
        
        # Configure styles
        style.configure("Title.TLabel", 
                       background=bg_dark, 
                       foreground=accent, 
                       font=("Arial", 24, "bold"))
        
        style.configure("Header.TLabel", 
                       background=bg_dark, 
                       foreground=text_color, 
                       font=("Arial", 14, "bold"))
        
        style.configure("Info.TLabel", 
                       background=bg_medium, 
                       foreground=text_color, 
                       font=("Arial", 11))
        
        style.configure("Stat.TLabel", 
                       background=bg_light, 
                       foreground=text_color, 
                       font=("Arial", 10))
        
        style.configure("Custom.TButton",
                       background=accent,
                       foreground=text_color,
                       font=("Arial", 10, "bold"),
                       borderwidth=0)
        
        style.map("Custom.TButton",
                 background=[("active", "#d63447")])
    
    def create_widgets(self):
        """Creates all interface widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="⚔️ LIFE RPG ⚔️", style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        # Top frame: Player info
        self.create_player_info_frame(main_frame)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Stats tab
        self.create_stats_tab()
        
        # Habits tab
        self.create_habits_tab()
        
        # Quests tab
        self.create_quests_tab()
        
        # Achievements tab
        self.create_achievements_tab()
    
    def create_player_info_frame(self, parent):
        """Creates the player info frame"""
        info_frame = tk.Frame(parent, bg="#16213e", relief=tk.RAISED, borderwidth=2)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Player name
        self.name_label = ttk.Label(info_frame, text="", style="Header.TLabel")
        self.name_label.pack(pady=5)
        
        # Frame for level and XP
        level_frame = tk.Frame(info_frame, bg="#16213e")
        level_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.level_label = ttk.Label(level_frame, text="", style="Info.TLabel")
        self.level_label.pack(side=tk.LEFT)
        
        self.gold_label = ttk.Label(level_frame, text="", style="Info.TLabel")
        self.gold_label.pack(side=tk.RIGHT)
        
        # XP bar
        xp_frame = tk.Frame(info_frame, bg="#16213e")
        xp_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.xp_label = ttk.Label(xp_frame, text="", style="Info.TLabel")
        self.xp_label.pack()
        
        self.xp_bar = ttk.Progressbar(xp_frame, mode='determinate', length=400)
        self.xp_bar.pack(pady=5)
    
    def create_stats_tab(self):
        """Creates the stats tab"""
        stats_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(stats_frame, text="📊 Stats")
        
        # Title
        title = ttk.Label(stats_frame, text="Character Attributes", style="Header.TLabel")
        title.pack(pady=10)
        
        # Frame for stats
        self.stats_frame = tk.Frame(stats_frame, bg="#1a1a2e")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.stat_labels = {}
        self.stat_bars = {}
        
        stat_info = {
            "strength": ("💪 Strength", "#e74c3c"),
            "intelligence": ("🧠 Intelligence", "#3498db"),
            "charisma": ("💬 Charisma", "#9b59b6"),
            "vitality": ("❤️ Vitality", "#2ecc71"),
            "discipline": ("🎯 Discipline", "#f39c12")
        }
        
        for stat, (name, color) in stat_info.items():
            stat_container = tk.Frame(self.stats_frame, bg="#0f3460", relief=tk.RAISED, borderwidth=2)
            stat_container.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(stat_container, text=name, style="Stat.TLabel")
            label.pack(anchor=tk.W, padx=10, pady=(5, 0))
            
            value_label = ttk.Label(stat_container, text="", style="Stat.TLabel")
            value_label.pack(anchor=tk.W, padx=10)
            self.stat_labels[stat] = value_label
            
            bar = ttk.Progressbar(stat_container, mode='determinate', length=500)
            bar.pack(padx=10, pady=(0, 5))
            self.stat_bars[stat] = bar
    
    def create_habits_tab(self):
        """Creates the habits tab"""
        habits_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(habits_frame, text="✅ Habits")
        
        # Title and add button
        top_frame = tk.Frame(habits_frame, bg="#1a1a2e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title = ttk.Label(top_frame, text="Daily Habits", style="Header.TLabel")
        title.pack(side=tk.LEFT)
        
        add_btn = ttk.Button(top_frame, text="➕ New Habit", 
                            command=self.add_habit, style="Custom.TButton")
        add_btn.pack(side=tk.RIGHT)
        
        # Habits list
        self.habits_listbox = tk.Listbox(habits_frame, bg="#16213e", fg="white", 
                                         font=("Arial", 10), height=15, selectmode=tk.SINGLE)
        self.habits_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Action buttons
        btn_frame = tk.Frame(habits_frame, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        complete_btn = ttk.Button(btn_frame, text="✓ Complete", 
                                 command=self.complete_habit, style="Custom.TButton")
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="🗑️ Delete", 
                               command=self.delete_habit, style="Custom.TButton")
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def create_quests_tab(self):
        """Creates the quests tab"""
        quests_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(quests_frame, text="⚔️ Quests")
        
        # Title and add button
        top_frame = tk.Frame(quests_frame, bg="#1a1a2e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title = ttk.Label(top_frame, text="Active Quests", style="Header.TLabel")
        title.pack(side=tk.LEFT)
        
        add_btn = ttk.Button(top_frame, text="➕ New Quest", 
                            command=self.add_quest, style="Custom.TButton")
        add_btn.pack(side=tk.RIGHT)
        
        # Quests list
        self.quests_listbox = tk.Listbox(quests_frame, bg="#16213e", fg="white", 
                                         font=("Arial", 10), height=15, selectmode=tk.SINGLE)
        self.quests_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Action buttons
        btn_frame = tk.Frame(quests_frame, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        complete_btn = ttk.Button(btn_frame, text="✓ Complete", 
                                 command=self.complete_quest, style="Custom.TButton")
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="🗑️ Delete", 
                               command=self.delete_quest, style="Custom.TButton")
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def create_achievements_tab(self):
        """Creates the achievements tab"""
        achievements_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(achievements_frame, text="🏆 Achievements")
        
        title = ttk.Label(achievements_frame, text="Unlocked Achievements", style="Header.TLabel")
        title.pack(pady=10)
        
        # Achievements list
        self.achievements_text = tk.Text(achievements_frame, bg="#16213e", fg="white", 
                                        font=("Arial", 10), height=20, wrap=tk.WORD)
        self.achievements_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Make text read-only
        self.achievements_text.config(state=tk.DISABLED)
    
    def update_display(self):
        """Updates all on-screen information"""
        player = self.game.player
        
        # Player info
        self.name_label.config(text=f"👤 {player['name']}")
        self.level_label.config(text=f"Level {player['level']}")
        self.gold_label.config(text=f"💰 {player['gold']} Gold")
        
        # XP
        xp_needed = self.game.get_xp_for_next_level()
        self.xp_label.config(text=f"XP: {player['xp']} / {xp_needed}")
        xp_percent = (player['xp'] / xp_needed) * 100
        self.xp_bar['value'] = xp_percent
        
        # Stats
        for stat, value in player['stats'].items():
            self.stat_labels[stat].config(text=f"Level {value}")
            # Bars go from 0 to 50 (estimated max level)
            percent = min((value / 50) * 100, 100)
            self.stat_bars[stat]['value'] = percent
        
        # Habits
        self.update_habits_list()
        
        # Quests
        self.update_quests_list()
        
        # Achievements
        self.update_achievements()
        
        # Check for new achievements
        self.check_achievements()
    
    def update_habits_list(self):
        """Updates the habits list"""
        self.habits_listbox.delete(0, tk.END)
        
        for habit_data in self.game.player.get("habits", []):
            habit = Habit.from_dict(habit_data)
            streak_emoji = "🔥" if habit.streak > 0 else ""
            self.habits_listbox.insert(tk.END, 
                f"{habit.name} | Streak: {habit.streak} {streak_emoji} | XP: {habit.xp_reward}")
    
    def update_quests_list(self):
        """Updates the quests list"""
        self.quests_listbox.delete(0, tk.END)
        
        for quest_data in self.game.player.get("quests", []):
            quest = Quest.from_dict(quest_data)
            if not quest.completed:
                difficulty_emoji = {"easy": "⭐", "normal": "⭐⭐", "hard": "⭐⭐⭐"}.get(quest.difficulty, "⭐⭐")
                self.quests_listbox.insert(tk.END, 
                    f"{difficulty_emoji} {quest.name} | XP: {quest.xp_reward} | Gold: {quest.gold_reward}")
    
    def update_achievements(self):
        """Updates the achievements list"""
        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)
        
        achievements = self.game.player.get("achievements", [])
        
        if not achievements:
            self.achievements_text.insert(tk.END, "You haven't unlocked any achievements yet.\nComplete habits and quests to earn achievements!")
        else:
            for achievement in achievements:
                self.achievements_text.insert(tk.END, f"🏆 {achievement}\n\n")
        
        self.achievements_text.config(state=tk.DISABLED)
    
    def add_habit(self):
        """Adds a new habit"""
        dialog = HabitDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            habit = Habit(**dialog.result)
            self.game.player.setdefault("habits", []).append(habit.to_dict())
            self.game.save_data()
            self.update_habits_list()
            messagebox.showinfo("✅ Habit Created", f"Habit '{habit.name}' added!")
    
    def complete_habit(self):
        """Completes a selected habit"""
        selection = self.habits_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a habit")
            return
        
        index = selection[0]
        habit_data = self.game.player["habits"][index]
        habit = Habit.from_dict(habit_data)
        
        # Check if already completed today
        today = str(date.today())
        if habit.last_completed == today:
            messagebox.showinfo("Info", "You already completed this habit today!")
            return
        
        # Update streak
        yesterday = str(date.today().replace(day=date.today().day - 1))
        if habit.last_completed == yesterday:
            habit.streak += 1
        else:
            habit.streak = 1
        
        habit.last_completed = today
        habit.total_completions += 1
        
        # Calculate rewards with streak bonus
        xp_reward = habit.xp_reward + (habit.streak * 5)
        gold_reward = habit.streak * 2
        
        # Add rewards
        self.game.add_xp(xp_reward)
        self.game.add_stat(habit.stat, 1)
        self.game.player["gold"] += gold_reward
        
        # Save
        self.game.player["habits"][index] = habit.to_dict()
        self.game.save_data()
        
        # Check for level up
        if self.game.player["xp"] >= self.game.get_xp_for_next_level():
            if self.game.level_up():
                messagebox.showinfo("🎉 LEVEL UP!", 
                    f"Congratulations! You are now level {self.game.player['level']}!")
        
        messagebox.showinfo("✅ Habit Completed", 
            f"Excellent! +{xp_reward} XP, +{gold_reward} Gold, +1 {habit.stat.capitalize()}\nStreak: {habit.streak} days 🔥")
        
        self.update_display()
    
    def delete_habit(self):
        """Deletes a selected habit"""
        selection = self.habits_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a habit")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this habit?"):
            index = selection[0]
            del self.game.player["habits"][index]
            self.game.save_data()
            self.update_habits_list()
    
    def add_quest(self):
        """Adds a new quest"""
        dialog = QuestDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            quest = Quest(**dialog.result)
            self.game.player.setdefault("quests", []).append(quest.to_dict())
            self.game.save_data()
            self.update_quests_list()
            messagebox.showinfo("✅ Quest Created", f"Quest '{quest.name}' added!")
    
    def complete_quest(self):
        """Completes a selected quest"""
        selection = self.quests_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a quest")
            return
        
        index = selection[0]
        # Find the real index (not counting completed ones)
        real_index = 0
        visible_index = 0
        for i, quest_data in enumerate(self.game.player["quests"]):
            quest = Quest.from_dict(quest_data)
            if not quest.completed:
                if visible_index == index:
                    real_index = i
                    break
                visible_index += 1
        
        quest_data = self.game.player["quests"][real_index]
        quest = Quest.from_dict(quest_data)
        
        # Mark as completed
        quest.completed = True
        
        # Add rewards
        self.game.add_xp(quest.xp_reward)
        self.game.player["gold"] += quest.gold_reward
        
        if quest.stat_reward:
            self.game.add_stat(quest.stat_reward, 2)
        
        # Save
        self.game.player["quests"][real_index] = quest.to_dict()
        self.game.save_data()
        
        # Check for level up
        if self.game.player["xp"] >= self.game.get_xp_for_next_level():
            if self.game.level_up():
                messagebox.showinfo("🎉 LEVEL UP!", 
                    f"Congratulations! You are now level {self.game.player['level']}!")
        
        stat_msg = f", +2 {quest.stat_reward.capitalize()}" if quest.stat_reward else ""
        messagebox.showinfo("⚔️ Quest Completed", 
            f"Quest '{quest.name}' completed!\n+{quest.xp_reward} XP, +{quest.gold_reward} Gold{stat_msg}")
        
        self.update_display()
    
    def delete_quest(self):
        """Deletes a selected quest"""
        selection = self.quests_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a quest")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this quest?"):
            index = selection[0]
            # Find the real index
            real_index = 0
            visible_index = 0
            for i, quest_data in enumerate(self.game.player["quests"]):
                quest = Quest.from_dict(quest_data)
                if not quest.completed:
                    if visible_index == index:
                        real_index = i
                        break
                    visible_index += 1
            
            del self.game.player["quests"][real_index]
            self.game.save_data()
            self.update_quests_list()
    
    def check_achievements(self):
        """Checks and unlocks achievements"""
        achievements = self.game.player.setdefault("achievements", [])
        new_achievements = []
        
        # Achievement: First quest
        if len([q for q in self.game.player.get("quests", []) if Quest.from_dict(q).completed]) >= 1:
            if "First Quest Completed" not in achievements:
                new_achievements.append("First Quest Completed")
        
        # Achievement: Level 5
        if self.game.player["level"] >= 5:
            if "Reach Level 5" not in achievements:
                new_achievements.append("Reach Level 5")
        
        # Achievement: Level 10
        if self.game.player["level"] >= 10:
            if "Reach Level 10" not in achievements:
                new_achievements.append("Reach Level 10")
        
        # Achievement: 7 day streak
        for habit_data in self.game.player.get("habits", []):
            habit = Habit.from_dict(habit_data)
            if habit.streak >= 7:
                if "7 Day Streak" not in achievements:
                    new_achievements.append("7 Day Streak")
                break
        
        # Achievement: 100 gold
        if self.game.player["gold"] >= 100:
            if "Accumulate 100 Gold" not in achievements:
                new_achievements.append("Accumulate 100 Gold")
        
        # Add new achievements
        if new_achievements:
            achievements.extend(new_achievements)
            self.game.save_data()
            messagebox.showinfo("🏆 New Achievement!", 
                f"You unlocked: {', '.join(new_achievements)}!")
    
    def run(self):
        """Runs the application"""
        self.root.mainloop()


class HabitDialog:
    """Dialog for creating a new habit"""
    
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Habit")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg="#1a1a2e")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Name
        tk.Label(self.dialog, text="Habit Name:", bg="#1a1a2e", fg="white").pack(pady=5)
        self.name_entry = tk.Entry(self.dialog, width=30)
        self.name_entry.pack(pady=5)
        
        # Stat
        tk.Label(self.dialog, text="Stat:", bg="#1a1a2e", fg="white").pack(pady=5)
        self.stat_var = tk.StringVar(value="discipline")
        stats = [
            ("💪 Strength", "strength"),
            ("🧠 Intelligence", "intelligence"),
            ("💬 Charisma", "charisma"),
            ("❤️ Vitality", "vitality"),
            ("🎯 Discipline", "discipline")
        ]
        for text, value in stats:
            tk.Radiobutton(self.dialog, text=text, variable=self.stat_var, value=value,
                          bg="#1a1a2e", fg="white", selectcolor="#0f3460").pack(anchor=tk.W, padx=20)
        
        # Difficulty
        tk.Label(self.dialog, text="Difficulty:", bg="#1a1a2e", fg="white").pack(pady=5)
        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = [("Easy (10 XP)", "easy"), ("Medium (20 XP)", "medium"), ("Hard (30 XP)", "hard")]
        for text, value in difficulties:
            tk.Radiobutton(self.dialog, text=text, variable=self.difficulty_var, value=value,
                          bg="#1a1a2e", fg="white", selectcolor="#0f3460").pack(anchor=tk.W, padx=20)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Create", command=self.create, bg="#e94560", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy, bg="#555", fg="white",
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    def create(self):
        """Creates the habit"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a name")
            return
        
        xp_rewards = {"easy": 10, "medium": 20, "hard": 30}
        
        self.result = {
            "name": name,
            "stat": self.stat_var.get(),
            "xp_reward": xp_rewards[self.difficulty_var.get()],
            "difficulty": self.difficulty_var.get()
        }
        self.dialog.destroy()


class QuestDialog:
    """Dialog for creating a new quest"""
    
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Quest")
        self.dialog.geometry("450x400")
        self.dialog.configure(bg="#1a1a2e")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Name
        tk.Label(self.dialog, text="Quest Name:", bg="#1a1a2e", fg="white").pack(pady=5)
        self.name_entry = tk.Entry(self.dialog, width=40)
        self.name_entry.pack(pady=5)
        
        # Description
        tk.Label(self.dialog, text="Description:", bg="#1a1a2e", fg="white").pack(pady=5)
        self.desc_entry = tk.Entry(self.dialog, width=40)
        self.desc_entry.pack(pady=5)
        
        # Difficulty
        tk.Label(self.dialog, text="Difficulty:", bg="#1a1a2e", fg="white").pack(pady=5)
        self.difficulty_var = tk.StringVar(value="normal")
        difficulties = [
            ("⭐ Easy (30 XP, 10 Gold)", "easy"),
            ("⭐⭐ Normal (50 XP, 20 Gold)", "normal"),
            ("⭐⭐⭐ Hard (100 XP, 40 Gold)", "hard")
        ]
        for text, value in difficulties:
            tk.Radiobutton(self.dialog, text=text, variable=self.difficulty_var, value=value,
                          bg="#1a1a2e", fg="white", selectcolor="#0f3460").pack(anchor=tk.W, padx=20)
        
        # Stat reward
        tk.Label(self.dialog, text="Stat Bonus (optional):", bg="#1a1a2e", fg="white").pack(pady=5)
        self.stat_var = tk.StringVar(value="none")
        stats = [
            ("None", "none"),
            ("💪 Strength", "strength"),
            ("🧠 Intelligence", "intelligence"),
            ("💬 Charisma", "charisma"),
            ("❤️ Vitality", "vitality"),
            ("🎯 Discipline", "discipline")
        ]
        for text, value in stats:
            tk.Radiobutton(self.dialog, text=text, variable=self.stat_var, value=value,
                          bg="#1a1a2e", fg="white", selectcolor="#0f3460").pack(anchor=tk.W, padx=20)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Create", command=self.create, bg="#e94560", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy, bg="#555", fg="white",
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    def create(self):
        """Creates the quest"""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a name")
            return
        
        rewards = {
            "easy": (30, 10),
            "normal": (50, 20),
            "hard": (100, 40)
        }
        
        xp, gold = rewards[self.difficulty_var.get()]
        stat = self.stat_var.get() if self.stat_var.get() != "none" else None
        
        self.result = {
            "name": name,
            "description": description or "An epic quest",
            "xp_reward": xp,
            "gold_reward": gold,
            "stat_reward": stat,
            "difficulty": self.difficulty_var.get()
        }
        self.dialog.destroy()


if __name__ == "__main__":
    app = LifeRPGGUI()
    app.run()