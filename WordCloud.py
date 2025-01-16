# coding: utf-8
import jieba
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from imageio import imread

def load_file_segment():
    # Load the text file and segment words
    jieba.load_userdict(r"PycharmProjects/WordCloud/mywords.txt")
    # Load our own dictionary
    with open(r"PycharmProjects/WordCloud/chat_records.txt",'r',encoding='utf-8') as f:
        # Open the file
        content = f.read()
        # Read the file content

    # Retain Chinese content
    content = re.sub(r'[^\u4e00-\u9fa5]', '', content)

    segs = jieba.cut(content) 
    # Segment the whole text
    segment = [seg for seg in segs if 2 <= len(seg) <= 5 and seg != '\r\n']
    # Add results to list if the length of the segmented word is between 2-5, and is not a newline character
    return segment

def get_words_count_dict():
    segment = load_file_segment()
    # Get the segmented result
    df = pd.DataFrame({'segment':segment})
    # Convert segmented array to pandas DataFrame
    stopwords = pd.read_csv(r"PycharmProjects/WordCloud/stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'], encoding="utf-8")
    # Load stop words
    df = df[~df.segment.isin(stopwords.stopword)]
    # Exclude stop words
    words_count = df.groupby('segment')['segment'].size().reset_index(name='count')
    # Group by word, calculate the count of each word
    words_count = words_count.reset_index().sort_values(by="count",ascending=False)
    # Reset index to retain segment field and sort in descending order of count
    return words_count

words_count = get_words_count_dict()
# Get word count

bimg = imread(r'PycharmProjects/WordCloud/picture1.jpg')
# Read the template image for word cloud generation

wordcloud = WordCloud(width=1080, 
                     height=1080,
                     background_color='white',
                     mask=bimg, 
                     font_path='simhei.ttf', 
                     max_words=1000, 
                     scale=10
                     )
# Get WordCloud object, set the background color, image, font of the word cloud

# If your background color is transparent, replace above two lines with these two
# bimg = imread('ai.png')
# wordcloud = WordCloud(background_color=None, mode='RGBA', mask=bimg, font_path='simhei.ttf')

words = words_count.set_index("segment").to_dict()
# Convert words and frequencies to dictionary
wordcloud = wordcloud.fit_words(words["count"])
# Map the words and frequencies to the WordCloud object
bimgColors = ImageColorGenerator(bimg)
# Generate colors
plt.axis("off")
# Turn off the axes
plt.imshow(wordcloud.recolor(color_func=bimgColors))
# Apply colors
plt.show()
