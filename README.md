# Overview

This game is part of an ongoing project to create a more consistent pricing scheme for creatures in online play-by-post fighting games. Determining if a unit's strength is proportional to it's cost would be tedious if done by hand. In automating the fights, I created what was essentially a game without graphics. I thought learning arcade would be a good next step as a better way of doing what i'd already been doing. Here, arcade can replace both the tkinter-based gui I had before, and the console.

The game can't technically be played, in that it plays itself. After clicking 'Battle!' a second time, two teams are created: one with a Black Widow, another with a pair of Sugar Ants. You may then watch them fight.

[Software Demo Video](https://youtu.be/yH-MyHaAsmo)

# Development Environment

The software was developed in Visual Studo Code, and was written in python using the 'arcade' module. The login and database functions use google firebase as part of a prior experiment.

# Useful Websites

* [Arcade's many Examples](https://api.arcade.academy/en/latest/examples/index.html)

# Future Work

* The menu to buy units to add to teams was previously built in tkinter and I will need to rebuild in in arcade.
* The database controller needs a slight rework to calculate the price only on unit creation, to save a sprite's image, and more.
* I intend to add more complex target selection/ 'a.i' in the future, which will require creating a log of which unit attacked whom.
* 'battle_creator' can likely be merged with it's arcade view.
* The battle coordinator needs to be updated to account for up to six teams.
* I also need to rebuild the unit creation menu.
* The sign in menu needs to obscure passwords.