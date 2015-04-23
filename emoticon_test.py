def haspositive(text):

    emoticons = [':-)', ':)', '=)', ':-D', ':D', '8-D', 'xD', '8D', 'x-D', 'X-D', 'XD', ":'-)", ';D', ":')", ':*',
                 ';-)', ';)', ':P', '=P', ':]', '=D']
    found_pos_basket=[]
    for emoticon in emoticons:
        if text.find(emoticon) > -1:
            found_pos_basket.append(emoticon)     
    return found_pos_basket

def hasnegative(text):

    emoticons = [':-(', ':(', ':[', '=(', ":'-(", ":'(", '=/', ':/']
    found_neg_basket=[]
    for emoticon in emoticons:
        if text.find(emoticon) > -1:
            found_neg_basket.append(emoticon)     
    return found_neg_basket