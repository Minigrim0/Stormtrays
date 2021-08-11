# Stromtrays
<p>
<img src="https://deepsource.io/gh/Minigrim0/Stormtrays.svg/?label=active+issues&show_trend=true&token=9zXI6PGE43X7aVUJL0rgA6Qf)](https://deepsource.io/gh/Minigrim0/Stormtrays/?ref=repository-badge" alt="deepsource status" title="deepsource status" />
</p>

<p>
    A tower defense game written in python with <a href="https://pygame.org"><img src=".meta/pygame.png" height=20 alt="pygame" title="pygame" /></a>
</p>

## Installation

```bash
git clone <this repo>
cd Stormtrays
python3 -m venv ve
source ve/bin/activate
pip install -r requirements.txt
```

## Launching the game

```
python3 Stormtrays.py
```

## Launching the editor

```
python3 Editor.py
```

## Building an executable

```
pyinstaller Stormtrays.py
pyinstaller Editor.py
```

Then run the executable located at `dist/Stormtrays/Stormtrays` and `dist/Editor/Editor`

## TODO

* [x] fix xp bar animation (sine animation, see menu buttons)
* [x] fix visible duration of ennemy's health bar
* [X] re-implement towers
* [x] Implement image-banks to avoid loading same images multiple times (Ennemies)
* [X] Allow ImageAnimation trigger to be called a different times during the animation
* [X] Add gold animations
* [X] Make placing towers cost money
* [X] Show tower names on hover when in tower menu
* [X] Draw level grid when placing a tower
* [X] Make ennemys health bars not sine (Too many updates on the advancement makes it buggy)
* [X] Re-implement difficulty parameter
* [X] Implement time acceleration
* [X] Implement pause menu
* [X] Add end menu
* [X] Reset game when leaving
* [X] Block placing towers everywhere (And show blocked tiles)
* [X] Show pause menu when pressing escape
* [ ] Implement automatic builds
* [ ] Profile the execution to find optimizations
* [ ] Fix deepsource issues

## Later
* [ ] Implement tower stats
* [ ] Implement bombs (V2.1)
* [ ] Add starting tile (V2.1)
* [ ] Allow multiple bastions per level (V2.1)
* [ ] Re-implement character powers (Invocation, time freeze, double money) (V2.2)
* [ ] Implement size changing for map in editor (V2.3)
