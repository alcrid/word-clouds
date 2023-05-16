
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import unidecode as uni
from os import path
import os
import random
import json


def fix_encoding(s):
    return uni.unidecode(s.encode('iso-8859-1').decode('utf-8'))



files = ["f1.json",
"f2.json",
"f3.json",
"f4.json",
"f5.json",
"f6.json",
"f7.json",
"f8.json",
"f9.json"]

out = ""
dataset = []


for file in files:
    with open(file,"r",encoding="utf-8") as f:
        data = json.load(f)
        for a in data['messages']:
            if("content" in a):
                for s in a["content"].split(" "):
                    out += fix_encoding(s).lower() + " "
                    dataset.append(fix_encoding(s).lower())

stop_words = [
    "za",
"jebe",
"kokot",
"debil",
"jebat",
"pici",
"skurveny",
"pica",
"picus",
"dopice",
"kokotina",
"debilina",
"jebnuty",
"jebnuta",
"kurva",
"dopici",
"chuj",
"chujovina",
"ne",
"na",
"mam",
"do",
"ja,"
"ty",
"a",
"z",
"co",
"je",
"jak",
"to",
"ci",
"aj",
"ze",
"sa",
"si",
"kto",
"alebo",
"v",
"o",
"ti",
"mi",
"tam",
"ty",
"uz",
"ako",
"toto",
"na",
"jej",
"ma",
"ale",
"tu",
"da",
"bo",
"no",
"ho",
"som",
"by",
"d",
"ta",
"mas",
"kde",
"ani",
"len",
"s",
"ja",
"tak",
'hej',
"ked",
"este",
"asi",
"lebo",
]

#stop_words = ["jebe","kokot","debil","jebat"]
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

mask = np.array(Image.open(path.join(d, "4.SA_inverse.png")))

i = 0

with open("database.txt","w",encoding="utf-8") as f:
    for line in dataset:
        f.write(line + " ")

'''
for words in dataset:

    for word in words.split(" "):
        print(word)
        if(word != '' ):
            if(not "www" in word):
                out += word + " "
'''
print(i)
names = [
"Name01", 
"Name02",
"Name03", 
"Name04", 
"Name05", 
"Name06", 
"Name07", 
"Name08", 
"Name09", 
"Name10", 
"Name11", 
"Name12", 
"Name13", 
"Name14", 
"Name15", 
"Name16",
"Name17", 
"Name18", 
"Name19", 
"Komanicky", 
"Name20", 
"Name21", 
"Name22", 
"Name23", 
"Name24", 
"Name25", 
"Name26", 
"Name27", 
"Name28", 
"Name29", 
#"Name30", 
"Name31", 
"Name32",
"Name33",
"Name34"]

print(len(out.split(" ")))

for name in names:
    for i in range(550):
       out += ( name+ " " + names[random.randint(0,len(names)-1)] + " " + names[random.randint(0,len(names)-1)])

i = 0
words = {}

for word in out.split():
    if(word not in words):
        words[word] = 1
    else:
        words[word] += 1

print(words["name"])

# wordcloud= WordCloud(max_words = 40000,
# scale=5,
# mask=mask,
# background_color='black',
# contour_color="white",
# stopwords=stop_words,
# contour_width=10,
# collocation_threshold=5,
# min_font_size = 2,
# colormap= "Blues",
# repeat = True,
# font_step = 1).generate(out)

#palletes = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

#for palette in palletes:

wordcloud= WordCloud(max_words = 4500,
scale=5,
mask=mask,
stopwords=stop_words,
# background_color="#14213d",
background_color="#0a101e",
collocation_threshold=75,
min_font_size = 10,
colormap= "Wistia",
repeat=False,
font_step = 1).generate(out)

wordcloud.to_file("wordclouds/final_censored_inverse2.png")
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
