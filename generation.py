import perlinNoise

# Frequency of the different noises
frequence_height1 = 0.01
frequence_height2 = 0.03
frequence_height3 = 0.05
frequence_height4 = 0.07

# Function that associates to each point on the map its height value (temperature and humidity not yet used)
def mapNoise(map):
    p = perlinNoise.make_permutation()
    for y in range(len(map)):
        for x in range(len(map[y])):
            height_noise = perlinNoise.noise(x * frequence_height1, y * frequence_height1, p)
            height_noise += perlinNoise.noise(x * frequence_height2, y * frequence_height2, p) * 0.25
            height_noise +=  perlinNoise.noise(x * frequence_height3, y * frequence_height3, p) * 0.2
            height_noise +=  perlinNoise.noise(x * frequence_height4, y * frequence_height4, p) * 0.1
            map[y][x]['height'] = ((height_noise + 1) / 2) * 100
            map[y][x]['temperature'] = 0
            map[y][x]['rainfall'] = 0
    return map
