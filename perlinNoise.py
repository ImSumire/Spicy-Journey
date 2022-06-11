# 𝗔 𝗳𝘂𝗹𝗹 𝗲𝘅𝗽𝗹𝗮𝗻𝗮𝘁𝗶𝗼𝗻 𝗼𝗳 𝘁𝗵𝗶𝘀 𝗰𝗼𝗱𝗲 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗼𝗻 𝘁𝗵𝗲 𝗥𝗘𝗔𝗗𝗠𝗘

from random import shuffle

permutation_length = 512


class Vector():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def dot(self, other):
		return self.x * other.x + self.y * other.y


def make_permutation():
	p = [i for i in range(permutation_length)]
	shuffle(p)
	return p + p

def get_constant_vector(v):
	h = v % 8
	if h == 0: return Vector(0, 1)
	elif h == 1: return Vector(1, 1)
	elif h == 2: return Vector(1, 0)
	elif h == 3: return Vector(1, -1)
	elif h == 4: return Vector(0, -1)
	elif h == 5: return Vector(-1, -1)
	elif h == 6: return Vector(-1, 0)
	elif h == 7: return Vector(-1, 1)

def lerp(a1, a2, t):
	return a1 + t * (a2 - a1)

def fade(t):
	return ((6 * t - 15) * t + 10) * t * t * t

def noise(x, y, permutation):
	X = int(x) % permutation_length
	Y = int(y) % permutation_length
	xf = x - int(x)
	yf = y - int(y)

	top_left = Vector(xf, yf - 1)
	top_right = Vector(xf - 1, yf - 1)
	bottom_right = Vector(xf - 1, yf)
	bottom_left = Vector(xf, yf)

	value_top_left = permutation[permutation[X] + Y + 1]
	value_top_right = permutation[permutation[X + 1] + Y + 1]
	value_bottom_right = permutation[permutation[X + 1] + Y]
	value_bottom_left = permutation[permutation[X] + Y]

	dot_top_left = top_left.dot(get_constant_vector(value_top_left))
	dot_top_right = top_right.dot(get_constant_vector(value_top_right))
	dot_bottom_right = bottom_right.dot(get_constant_vector(value_bottom_right))
	dot_bottom_left = bottom_left.dot(get_constant_vector(value_bottom_left))

	u = fade(xf)
	v = fade(yf)

	return lerp(lerp(dot_bottom_left, dot_top_left, v), lerp(dot_bottom_right, dot_top_right, v), u)
