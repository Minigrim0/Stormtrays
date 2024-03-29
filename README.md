# Stromtrays
<p>
<img src="https://deepsource.io/gh/Minigrim0/Stormtrays.svg/?label=active+issues&show_trend=true&token=9zXI6PGE43X7aVUJL0rgA6Qf" alt="deepsource status" title="deepsource status" />
<img src="https://github.com/Minigrim0/Stormtrays/actions/workflows/linting.yml/badge.svg" alt="github action status" title="itch.io build and push" /> 
</p>

<img src=".meta/screenshots/ingame.png" alt="in game screenshot" title="In Game Screenshot" />

<p>
    A tower defense game written in python with <a href="https://pygame.org"><img src=".meta/pygame.png" height=20 alt="pygame" title="pygame" /></a>
</p>
<p>
    <a href="https://minigrim0.itch.io/stormtrays">Stormtrays on itch.io</a>
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
