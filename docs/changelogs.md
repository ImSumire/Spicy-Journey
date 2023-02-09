# 🛠 Changelog

__Icons__ : ➕🗑🪄🐛

<hr>

#### To-do list 📋
##### Global :
- [ ] Remake the whole `README.md`
##### Software :
- [x] Generation seed : new seed for each reload
- [ ] Size support (will be worked on if the saving principle is put in place)
- [x] Optimization (use of `snoise2`)
- [ ] Display styles (change the color palette of the map)
- [ ] Generation of structures for a better simulation
##### Game :
- [ ] Playable, like a mini survival game or exploration game (will be published on github.com/ImGalaad/Journey)
- [ ] Huge optimization, reduce lag when the camera display a massive forest (a lot of images)
- [ ] Custom sprites (currently with free sprites from the internet, rafaelmatos.itch.io/epic-rpg-world-pack-free-demoancient-ruins)
- [ ] More vibrante colors for a greater looking
- [ ] Make a better terrain generation
- [ ] Generation of structures for a better simulation

<hr>

## [0.1.4] - 2023-02-09

### _Game_ - Movement update
##### Added  ➕
- Better organization of imports in the `game.py` file
- Changed name `Camera` -> `Player` for an obvious reason of a change of the move

## [0.1.3] - 2023-02-04

### _Game_ - Optimization update
##### Added  ➕
- Added `memoize` decorator that applies a cache write to greatly optimize noise calculations
- Added 'lazy' mode to avoid recalculating everything at each frame, activated when the player is not moving
- Added `screen_size` variable to avoid re-calling `screen.get_size()`
- Added event restriction with `pygame.event.set_allowed()`

##### Changed 🪄
- Modification of the management of the calculations with the methods to optimize
- Changed image handling to be more compatible with PyGame (~25fps to ~ 120fps), thanks to `.convert_alpha()`
- Modification of the size of the game (850x600 to 1280x700) for a better visibility (and possible thanks to the optimization)
- Separation of `Camera` and `Godray` classes for better readability
- Better distribution of libraries imports in `game.py`

## [0.1.2] - 2023-02-03

### _Global_
##### Added ➕
- Added documentation (`changelogs.txt` and `LICENSE.txt`)
- Added the `tests` file to see what the next updates will be
##### Changed 🪄
- Improvement of file organization for a better look


### _Software_
##### Added ➕
- Added `_config.yml` to centralize variables
- Added debug mode to get useful statistics
- Added randomness when a new world is created

### _Game_
##### Added  ➕
- Official release of the PyGame version of Atlas
