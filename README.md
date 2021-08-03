# Stromtrays

A tower defense game written in python with pygame

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
* [ ] Add starting tile
* [ ] Allow multiple bastions per level
* [ ] Re-implement character powers (Invocation, time freeze, double money)
* [X] Allow ImageAnimation trigger to be called a different times during the animation
* [ ] Implement automatic builds
* [ ] Implement size changing for map in editor
* [ ] Profile the execution to find optimizations
* [ ] Re-implement difficulty parameter
* [X] Add gold animations
* [X] Make placing towers cost money
* [X] Show tower names on hover when in tower menu
* [ ] Draw level grid when placing a tower
* [ ] Make ennemys health bars not sine (Too many updates on the advancement makes it buggy)
* [ ] Implement bombs

## Deepsource status

[![DeepSource](https://deepsource.io/gh/Minigrim0/Stormtrays.svg/?label=active+issues&show_trend=true&token=9zXI6PGE43X7aVUJL0rgA6Qf)](https://deepsource.io/gh/Minigrim0/Stormtrays/?ref=repository-badge)
