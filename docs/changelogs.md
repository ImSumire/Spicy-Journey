### To-do list
- [ ] Playable, exploration game, collection of ingredients to be able to cook
- [x] Huge optimization, reduce lag when the camera display a massive forest (a lot of images)
- [ ] Custom sprites (currently with free sprites from the internet)
- [ ] More vibrante colors for a greater looking
- [ ] Make a better terrain generation, add mountains and rivers
- [ ] Generation of structures/ingredients/plants for a better simulation
- [ ] Add the fishing system to cook fish
- [ ] Do a cookbook and a cooking system
- [ ] Day/Night Cycle
- [ ] Potion system
- [ ] Date system
- [ ] ☰ Photo | Inventory | Cookbook | Quest | Parameters

<hr>

## [0.1.6] - 2023-03-23

### Lakes and optimization update
##### Added
- Addition of the lakes according to the height of the ground
- Added new sprites for falling leaves
- Added `credits.txt` for some credits of the sprites sources
- Add `Button` class for next update (to add a title screen and other menus)
- Add the `Fade` class to add a fade animation
- First attempts to add music to the game
##### Changed
- Sprite enhancement
- More colorful sprite colors
- Improvement of the loading speed of the `__init__` of the `Leaf` class
- `memoize` improvement (6.7 seconds to 1.2 on a big loop, ~100000)
- The `Player` class no longer has unnecessary management of a `rect`
- Improved computation speed with numba (njit) and reduction of useless loop computations
- Better assignment of variables and constants in the `Terrain` class
- Best way to sort sprites in the `get_sprites`

## [0.1.5] - 2023-03-04

### _main_ - Playable update
##### Added
- Added `config.json` for much faster reading of configurations.
- Adding documentation/explanations in the `main.py`.
- Added `requirements.txt`.
- Added all the sprites of the player in `res/sprites/Characters`.
- Added leaf particles to make the game more beautiful.
- Added random world system.
- Added player animations
- Added the "smooooth" moves.
- Added support for AZERTY and QWERTY keyboards by clicking `k`.
##### Changed
- Moved everything related to the base application on Tkinter to the `old` folder, there is no more will to update.
- Global modification of the `terrain.py` file for a better compatibility of the world generation.
##### Removed
- The `_config.yml` file has been deleted

## [0.1.4] - 2023-02-09

### _Game_ - Movement update
##### Added
- Better organization of imports in the `game.py` file
- Changed name `Camera` -> `Player` for an obvious reason of a change of the move

## [0.1.3] - 2023-02-04

### _Game_ - Optimization update
##### Added
- Added `memoize` decorator that applies a cache write to greatly optimize noise calculations
- Added 'lazy' mode to avoid recalculating everything at each frame, activated when the player is not moving
- Added `screen_size` variable to avoid re-calling `screen.get_size()`
- Added event restriction with `pygame.event.set_allowed()`

##### Changed
- Modification of the management of the calculations with the methods to optimize
- Changed image handling to be more compatible with PyGame (~25fps to ~ 120fps), thanks to `.convert_alpha()`
- Modification of the size of the game (850x600 to 1280x700) for a better visibility (and possible thanks to the optimization)
- Separation of `Camera` and `Godray` classes for better readability
- Better distribution of libraries imports in `game.py`

## [0.1.2] - 2023-02-03

### _Global_
##### Added
- Added documentation (`changelogs.txt` and `LICENSE.txt`)
- Added the `tests` file to see what the next updates will be
##### Changed
- Improvement of file organization for a better look


### _Software_
##### Added
- Added `_config.yml` to centralize variables
- Added debug mode to get useful statistics
- Added randomness when a new world is created

### _Game_
##### Added
- Official release of the PyGame version of Atlas
