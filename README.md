<h1 align="center">🧭 Spicy Journey - 香り旅 - Voyage épicé
  <br>
  <img alt="Statue In dev" src="https://img.shields.io/badge/STATUE-IN%20DEV-78b444?style=for-the-badge">
  <img alt="Version 0.1.8" src="https://img.shields.io/badge/VERSION-0.1.8-53d0a2?style=for-the-badge">
  <img alt="Licence GNU" src="https://img.shields.io/badge/LICENCE-GNU-fb7f53?style=for-the-badge">
</h1>

<img alt="Logo" src="https://raw.githubusercontent.com/ImSumire/Spicy-Journey/main/res/sprites/logo.png" align=right>

<p align="justify">Spicy Journey is a game that will help you relax and unwind as you explore a procedurally generated world filled with lush forests. With its isometric viewpoint and pixel art style, Spicy Journey is a retro-visual game that is sure to captivate you. Spicy Journey offers endless possibilities for exploration and discovery. No two games are the same, so you can come back to Spicy Journey again and again for a new experience. If you're looking for a game that will help you relax and unwind, look no further than Spicy Journey. With its beautiful forests, charming pixel art style, and endless exploration possibilities, it's the perfect game for anyone looking to escape into a peaceful and immersive world.</p>

<hr>

### In-game screenshot
![Game Screenshot](https://raw.githubusercontent.com/ImSumire/Spicy-Journey/main/screenshots/2023-04-11_22.36.12.768953.png)

**The lore**
<p align="justify">The story takes place in a fantasy world filled with magic and mystery. The character you control is a young Japanese woman named Hana, born in a small remote village nestled in a lush forest. Hana is an avid cook and has inherited her traditional Japanese recipe book from her grandmother. The ingredients she needs to cook these dishes are scattered all over the world. She decided to go on an adventure to collect and cook them in order to perpetuate the family traditions and pay tribute to her grandmother. She embarks on an incredible journey through the wilderness, discovering mystical secrets about the world around her. Along the way, Hana meets fascinating characters who help her on her quest, such as merchants who sell her useful ingredients for her recipes.</p>

<hr>

### How is the world generated ?

We simply use the Perlin Noise (more precisely the Simplex Noise) !
- Library we use : https://pypi.org/project/noise/

<p align="justify"><a href="https://en.wikipedia.org/wiki/Perlin_noise" target="_blank">Perlin Noise</a> is a type of procedural texture generator that was invented by <a href="https://en.wikipedia.org/wiki/Ken_Perlin" target="_blank">Ken Perlin</a> in 1985. It is a function that generates a pseudo-random appearance, which means that the output appears to be random, but it is actually deterministic and can be easily controlled by changing its input parameters or "seed".</p>

<img alt="Perlin Noise Terrain Mesh" src="https://www.scratchapixel.com/images/noise-part-2/perlin-noise-terrain-mesh1.png?" style="width:35%" align="right">


<p align="justify">Perlin Noise is commonly used to generate various types of textures, such as clouds, terrain, and marble. It is also used in many video games to create realistic and dynamic landscapes, as well as in animation and movie special effects. The algorithm is based on a grid of gradient vectors that are used to interpolate between the lattice points to produce the final output.

Perlin Noise has been improved over the years, and one of the most commonly used variants is Simplex Noise, which is faster and more efficient than the original algorithm. It uses a more optimal simplex grid instead of a regular grid, resulting in smoother and more natural-looking textures.

Overall, Perlin Noise (and Simplex Noise) are powerful tools for generating realistic and varied textures for various applications, including video games, animation, and digital art.

To put it simply, we use the values of these noises to vary the world data, we have a terrain height noise that also defines the placement of lakes, and we use a vegetation noise, it serves us to know if there is vegetation in a given place and what is the type of vegetation (id).</p>

##### Let's talk about complexity !

- Perlin Noise : $O(n^2)$
- Simplex Noise : $O(n)$

*Lower computational complexity, cost and fewer multiplications makes the a very fast computing speed, that's why we use the Simplex Noise !*

##### Wikipedia Links

> To understand the Simplex principle : https://en.wikipedia.org/wiki/Simplex_noise
> 
> To understand the principle of the basic one : https://en.wikipedia.org/wiki/Perlin_noise
> 
> Small credit to its creator : https://en.wikipedia.org/wiki/Ken_Perlin

*We recommend this video which helped us a lot to understand how to generate a terrain :*

> Video of Henrik Kniberg (dev and designer at Minecraft) : https://youtu.be/CSa5O6knuwI

<hr>

### The new interface (GUI)
![Menu preview](https://raw.githubusercontent.com/ImSumire/Spicy-Journey/main/screenshots/2023-04-11_22.43.27.195722.png)

- Spicy Journey - 🇫🇷 "Voyage épicé" ou "Voyage pimenté"
- 香り旅 (kaori tabi) - 🇫🇷 "Voyage d'odeurs agréables" / 🇬🇧 "Journey of pleasant smells"

<hr>

## To Do List

- [x] Playable, exploration game, collection of ingredients
- [x] Huge optimization, reduce lag when the camera display a lot of images
- [x] More vibrante colors for a greater looking
- [x] Make a better terrain generation, lakes and rivers
- [x] Generation of ingredients and plants for a better simulation
- [x] Create the cookbook interface
- [x] Making the complete interface (title screen, settings, in-game menu)
- [x] Add sounds to the game (music, wind, footsteps in the grass)
- [x] Add a translation system
- [ ] Add multiplayer for even more fun 
- [ ] Making the essential mechanics of the game: cooking
- [ ] Add the Ambulant Merchant to have special ingredients
- [ ] Make the fishing system to expand the list of recipes
- [ ] Add animals to add life (butterflies, deer, boars)
- [ ] Implement a day/night cycle system
- [ ] Add biome management to diversify the landscape and its content

<hr>

## Install

#### Update pip
Don't forget to use the latest version of pip, it's not essential for this code but it's always good to update :3
```batch
pip install --upgrade pip
```

#### Libs
Install Pygame, noise, json and numba :
```batch
pip install -r requirements.txt
```
Content :
```py
python==3.*
pygame
noise
json
numbafastapi==0.95.0
```

<hr>

## Developing

```
# Clone this repository
$ git clone https://github.com/ImSumire/Spicy-Journey

# Change directory
$ cd Spicy-Journey

# Run the startup script
$ python3 main.py
```

<hr>

## License ©

#### [GNU General Public License](https://choosealicense.com/licenses/mit/)

Copyright © 2023 [@Zecyl](https://www.github.com/Zecyl) and [@ImSumire](https://github.com/ImSumire)

```
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.
```

 Follow the terms and conditions here : https://www.gnu.org/licenses/gpl-3.0.txt
</h5>

<hr>

## Authors
#### Game
- [@ImSumire](https://github.com/ImSumire) Isometric Engine, Optimization, GUI, World management
- [@Zecyl](https://www.github.com/Zecyl) Multiplayer (soon)

#### Software
- [@ImSumire](https://github.com/ImSumire) User-Interface management (Tkinter), running optimization and file organization
- [@Zecyl](https://www.github.com/Zecyl) Ideas and project development, Perlin Noise handling, and early versions of save/load processing
