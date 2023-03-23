# Spicy Journey - Exploration of the wilderness 🧭

<hr>

![Game Screenshot](https://raw.githubusercontent.com/ImGalaad/Spicy-Journey/main/res/example.png)


Introducing Spicy Journey, the game that will help you unwind and relax as you explore a procedurally generated world filled with lush forests. With its isometric viewpoint and pixel art style, Spicy Journey is a retro-visually game that is sure to captivate you.

With its procedurally generated world, Spicy Journey offers endless opportunities for exploration and discovery. No two games will be the same, so you can keep coming back to Spicy Journey again and again for a new and exciting experience.

So if you're looking for a game that will help you relax and unwind, look no further than Spicy Journey. With its beautiful forests, charming pixel art style, and endless possibilities for exploration, it's the perfect game for anyone looking to escape into a peaceful and immersive world.

<hr>

## Why Pygame?
Because it is a beautifully optimized and much more complete library, and quite low-level compared to Raylib and Arcade Pyglet. Moreover, it is in the computer science speciality program in high school. And moreover the next versions of Pygame will use SDL2 which greatly improves the speed of calculation and display by using also the GPU (11x faster).

<hr>

## What is Perlin/Simplex Noise ? 🌫

[Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise) is a procedural texture calculator developed by [Ken Perlin](https://en.wikipedia.org/wiki/Ken_Perlin) in 1985. He studied at Harvard University, New York University and now he is a computer scientist, engineer and university professor.

The function has a pseudo-random appearance, and yet its generation is not really random, it is only the seed that is. 

This property allows this texture to be easily controllable. Multiple zoomed-in copies of Perlin Noise can be inserted into mathematical expressions to create a wide variety of procedural textures.

Perlin Noise is well known for its use in the generation of Minecraft worlds as well as in many other video games. So it's its ease to do many things that attracted us.

#### Why Simplex Noise and not Perlin Noise ?

Complexity :
- Perlin_noise : $O(n^2)$
- Simplex_noise : $O(n)$

Lower computational complexity, cost and fewer multiplications makes the a very fast computing speed

#### Wikipedia Links

> https://en.wikipedia.org/wiki/Simplex_noise
> 
> https://en.wikipedia.org/wiki/Perlin_noise
> 
> https://en.wikipedia.org/wiki/Ken_Perlin

<u>We recommend this video which helped us a lot to understand how to generate a terrain :</u>

> https://youtu.be/CSa5O6knuwI

<hr>

## To Do 📋

- [ ] Playable, exploration game, collection of ingredients to be able to cook
- [x] Huge optimization, reduce lag when the camera display a massive forest (a lot of images)
- [x] More vibrante colors for a greater looking
- [x] Make a better terrain generation, add rivers/lakes
- [ ] Generation of structures/ingredients/plants for a better simulation
- [ ] Add the fishing system to cook fish

<hr>

## Installation

#### Update pip
<i>Don't forget to use the latest version of pip, it's not essential for this code but it's always good to update :3</i>
```
pip install --upgrade pip
```

#### Libs
<i>Install Pygame, noise, numba, and json: </i>
```
pip install -r requirements.txt
```
*Content:*
```
python==3.*
pygame
noise
json
numba
```

<hr>

## License ©

#### [GNU General Public License](https://choosealicense.com/licenses/mit/)

Copyright © 2023 [@Zecyl](https://www.github.com/Zecyl) and [@ImSumire](https://github.com/ImSumire)

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

 Follow the terms and conditions here : https://www.gnu.org/licenses/gpl-3.0.txt
</h5>

<hr>

## Authors
#### Game
- [@ImSumire](https://github.com/ImSumire) Project creator and all the code for the moment

#### Software
- [@ImSumire](https://github.com/ImSumire) Project creator, User-Interface management (Tkinter), running optimization and file organization
- [@Zecyl](https://www.github.com/Zecyl) Ideas and project development, Perlin Noise handling, and early versions of save/load processing
