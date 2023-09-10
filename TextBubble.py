import drawsvg as draw
from drawsvg import Path
from PIL import Image
from io import BytesIO
import cairosvg
import svgwrite

horizontal=15
offset=18

def split_sentence_into_words(sentence):
    """
    Splits a sentence into a list of words.
    
    Args:
        sentence (str): The input sentence to split.
        
    Returns:
        list: A list of words.
    """
    words = sentence.split()
    return words

def ProcessLongwordsList(text_list,size):
    """
    Processes a list of words, splitting long words into smaller chunks.
    
    Args:
        text_list (list): The list of words to process.
        
    Returns:
        list: A list of words, including any long words split into smaller chunks.
    """
    processed_list = []

    for word in text_list:
        if len(word) > size:
            # Pass long word to SplitLongWords2List for further splitting
            subwords = SplitLongWords2List(word)
            processed_list.extend(subwords)
        else:
            processed_list.append(word)

    return processed_list

def SplitLongWords2List(text, chunk_size=35):
    """
    Splits the given text into a list of chunks with the specified chunk size.
    
    Args:
        text (str): The input text to split.
        chunk_size (int): The size of each chunk.
        
    Returns:
        list: A list of text chunks.
    """
    # Initialize an empty list to store the broken-up text
    broken_text = []

    # Iterate through the text in steps of chunk_size characters
    for i in range(0, len(text), chunk_size):
        broken_text.append(text[i:i + chunk_size])
        joindWords=joinList2Sentence(broken_text)
        #call make list to string
    return joindWords

def joinList2Sentence(text_list):
    """
    Joins a list of text chunks into a single string.
    
    Args:
        text_list (list): The list of text chunks to join.
        
    Returns:
        str: The joined text.
    """
    # Use the join method to concatenate the text chunks

    joined_text = '\n'.join(text_list)
    return joined_text

def count_lines_in_string(text):
    """
    Counts the number of lines in a string separated by newline characters '\n'.

    Args:
        text (str): The input string.

    Returns:
        int: The number of lines.
    """
    lines = len(text)
    return lines

def split_text(text, max_length=35):
  
  #sentence                           to      pre_word_list
  preWordList=split_sentence_into_words(text)
  linelengths=[]
  #pre_word_list                      to      size_checker
  BrokenandwholeWordList=[]
  for preword in preWordList:
    BrokenandwholeWordList.append(SplitLongWords2List(preword,max_length))

  

  sentence=joinList2Sentence(BrokenandwholeWordList)
  sentenceList=split_sentence_into_words(sentence)

  newsentence,longestLine=join_words_into_sentences(sentenceList,max_length=max_length)
  #exit here with linelengths
  line_count = count_lines_in_string(newsentence)

  return newsentence,line_count,longestLine

def join_words_into_sentences(word_list, max_length=36):
    """
    Joins a list of words into sentences with a maximum length of max_length
    characters per sentence. Sentences are separated by newline characters.

    Args:
        word_list (list): The list of words to join into sentences.
        max_length (int): The maximum length of each sentence.

    Returns:
        list: A list of sentences.
    """
    sentences = []
    current_sentence = ""
    
    for word in word_list:
        if len(current_sentence) + len(word) + 1 <= max_length:
            # Add the word to the current sentence with a space if not the first word
            if current_sentence:
                current_sentence += " "
            current_sentence += word

        else:
            # Start a new sentence
            sentences.append(current_sentence)
            current_sentence = word

    
    # Add the last sentence
    if current_sentence:
        
        sentences.append(current_sentence)
    linelengths=[]
    for sentence in sentences:
      
      linelengths.append(textwidth(sentence))###########################################
      #print(linelengths)
      sorted_list = sorted(linelengths)
      #print (sorted_list)
      highest_value = sorted_list[-1]
      #print("Longest line: ",highest_value)
    return sentences,highest_value#need to return linelengths posibly just the longest

def textwidth(text, fontsize=19):
    #firstlinetext=text[0]
    try:
        import cairo
    except:
        return len(text) * fontsize
    surface = cairo.SVGSurface('undefined.svg', 1280, 200)
    
    cr = cairo.Context(surface)
    cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    if width<= 15:
        width = 15
    return width

def DrawTextBubble(textbubletext,filename="bubble.png",transmition="sender"):


    TXTobj=split_text(textbubletext,max_length=36)

    linecount=TXTobj[1]
    longestline=TXTobj[2]

    vertical= offset*linecount
    horizontal=longestline

    Bubble=f"m 20, 3 c -9.53166,0 -17.19014,7.67805 -17.19014,17.19014 v {vertical} c 0,9.51113 7.65742,19.38375 17.19014,19.38375 h {horizontal} c 3.00841,0 7.65158,-0.77173 11.80569,-4.69663 5.79207,6.3326 16.55348,5.13443 18.95273,3.89345 -1.70888,-0.31942 -13.56811,-5.36486 -13.56825,-18.58057 v -{vertical} c 0,-9.52422 -7.66826,-17.19014 -17.19015,-17.19014 z"
    drawTXT = draw.Drawing(horizontal+55, vertical+43, origin="top-left")
    drawBG = draw.Drawing(horizontal+55, vertical+43, origin="top-left")
    drawBG.set_pixel_scale(3) 
    if transmition=="Rx":
        custom_fill_color ='rgb(16, 132, 255)'
        bubble = draw.Path(Bubble, stroke_width=1, stroke=custom_fill_color, fill=custom_fill_color, fill_opacity=1)
        drawBG.append(bubble)

        font_path = '/usr/share/fonts/truetype/gentium-basic/GenBasBI.ttf'
        text = draw.Text(TXTobj[0], font_family="Times New Roman", font_size=18, x=15, y=35)

        #text = draw.Text(TXTobj[0],font_size=18, x=15, y=35)
        flip=False
        
    else:
        custom_fill_color ='rgb(230, 230, 230)'  
        bubble = draw.Path(Bubble, stroke_width=1, stroke=custom_fill_color, fill=custom_fill_color, fill_opacity=1)
        drawBG.append(bubble)
        text = draw.Text(TXTobj[0],font_size=18, x=25, y=35)
        flip =True

    
    
    drawTXT.append(text)
    #image1 = Image.open(BytesIO(drawBG.as_png()))

    png_bytes1 = cairosvg.svg2png(bytestring=drawBG.as_svg())
    BGimg = Image.open(BytesIO(png_bytes1))

    #image2 = Image.open(BytesIO(drawTXT.as_png()))
    png_bytes2 = cairosvg.svg2png(bytestring=drawTXT.as_svg())
    TXTimg = Image.open(BytesIO(png_bytes2))

    
    if flip==True:
        BGimg = BGimg.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        pass

    # Ensure both images have the same dimensions
    if BGimg.size != TXTimg.size:
        TXTimg = TXTimg.resize(BGimg.size, Image.LANCZOS)

    result = Image.alpha_composite(BGimg, TXTimg)
    result.save("output.png")
    result.show()
    BGimg.close()
    TXTimg.close()


if __name__ =="__main__":
    
    DrawTextBubble("Once upon a time,in a quaint little village nestled deep within the rolling hills, lived a young woman named Emily.","sender.png",transmition="Rx")