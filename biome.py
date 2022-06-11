# Function to apply colors to the different regions of the map
def height(h):
	if h >=84: 
		return brighten('#c7c7c7', h-84) # 𝘚𝘯𝘰𝘸 𝘔𝘰𝘶𝘵𝘢𝘪𝘯
	elif h >= 70: 
		return brighten('#414042', h-70) # 𝘔𝘰𝘶𝘵𝘢𝘪𝘯
	elif h >= 40: 
		return brighten('#265218', h-50) # 𝘍𝘭𝘢𝘵
	elif h >= 30:
		return brighten('#d2c78b', h-40) # 𝘚𝘢𝘯𝘥
	else: 
		return brighten('#1b1c69', h) # 𝘞𝘢𝘵𝘦𝘳

# Function to adjust color shades
def brighten(color, rate):
    color = color.replace('#', '')
    s = '#'
    for i in [0,2,4]:
        c = color[i:i+2]
        c = int(c, 16)
        c = int(c + (rate*1))
        c = format(c, '02x')
        s += c
    return s
