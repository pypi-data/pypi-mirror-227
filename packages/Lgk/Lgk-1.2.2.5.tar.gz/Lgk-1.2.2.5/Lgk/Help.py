from Lgk.Func.match import detect

colors = """ * colors = \\""\"
   colors: A function to change the text color.
 
 Import:
 • from Lgk.Text.colors import colors
 • from Lgk.Text.Bg import colors as bgcolor

 Usage:
 • print(colors(text="Hello world", color="Green"))
 • # First letter is always capitalized.

 Bgcolors:
 • print(bgcolor(text="Hello world", color="Green"))
 • # First letter is always capitalized.
\\\\""\"

"""

bgcolors = colors

styles = ''' * styles = \\""\"
   styles: A function to change the text font.


 Import:
 • from Lgk.Text.styles import styles

 Usage:
 • print(styles(text="Hello world", styles="1"))
 • # styles code Available only 1 to 10 or Bold and italic.
\\\\""\"
'''

Hindi_styles= ''' * styles = \\""\" 
   styles: एक फ़ंक्शन जो पाठ फ़ॉन्ट को बदलने के लिए है।

 आयात:
 • from Lgk.Text.styles import styles

 उपयोग:
 • print(styles(text="Hello world", styles="1"))
 • # स्टाइल कोड केवल 1 से 10 या बोल्ड और इटैलिक में उपलब्ध है।
\\\\""\" 
'''

TexHL = ''' * TexHl = \\""\"

 TexHL: Text Highlighter
 • TexHl is a text highlight.
 • It prints the text in the specified color,
 • and then reprints the text in that color\n   as an  animation,
 • because it is work in Animation format\n   thats why its print the value directly.

 Import:
 * from Lgk.Animation.TexHL import TexHL
 
 Usage:
 • TexHL(text="Hello world", second=0.05)
 • TexHL(text="Hello World", Hlc="White", color="Gray", second=0.5)


 Meanings:
 • Hlc = reprints text color.
 • color = before highlight color.
 • second = hightlight speed you can adjust that.
\\\\""\"
'''

Hindi_TexHL = ''' * TexHL = \""\"

 TexHL: टेक्स्ट हाइलाइटर
 • TexHl एक टेक्स्ट हाइलाइट है।
 • यह टेक्स्ट को निर्दिष्ट रंग में प्रिंट करता है,
 • और फिर टेक्स्ट को उस रंग में दोबारा प्रिंट करता है
    एक एनीमेशन के रूप में,
 • क्योंकि यह एनीमेशन फॉर्मेट में काम करता है
   इसीलिए यह सीधे मूल्य प्रिंट करता है।

 आयात करना:
 * from Lgk.Animation.TexHL import TexHL

 उपयोग:
 • TexHL(text='हैलो वर्ल्ड', second=0.05)
 • TexHL(text='हैलो वर्ल्ड', Hlc='White', color="Gray"', second=0.5)


 अर्थ:
 • एचएलसी = टेक्स्ट रंग को दोबारा प्रिंट करता है।
 • रंग = हाइलाइट रंग से पहले।
 • सेकंड = हाईटलाइट स्पीड आप उसे समायोजित कर सकते हैं।
 \\""\"
'''

Hindi_colors= ''' * colors = \\""\"
    colors: पाठ के रंग को बदलने के लिए एक फ़ंक्शन।

 आयात:
 • from Lgk.Text.colors import colors
 • from Lgk.Text.Bg import colors as bgcolor

 उपयोग:
 • print(colors(text="Hello world", color="Green"))
 • # पहला अक्षर हमेशा मानकीकृत होता है।

 Bgcolors:
 • print(bgcolor(text="Hello world", color="Green"))
 • # पहला अक्षर हमेशा मानकीकृत होता है।
\\\\""\" 
'''

detect_function = ''' * detect = \\""\"
   detect: A function that checks for similarity \n   between two values.


 Import:
 • from Lgk.Func.match import detect
 
 Usage:
 • a = "Hello"
 • b = "Hello"
 • result = detect(a, b, percent="100")
 • # 100 mean 100% similarity between a and b\n   you can adjust as you want
 • # Returns True if a is similar to b, otherwise returns False.
\\\\""\"
'''


def Help(args=""):
    if detect(args, "colors") or detect(args, "Bgcolors"):
        return colors
    if detect(args, "styles"):
        return styles
    if detect(args, "TexHL"):
        return TexHL
    if detect(args, "detect"):
        return detect_function
    
    #__ in hindi
    if detect(args, "TexHL hindi"):
        return Hindi_TexHL
    if detect(args, "styles hindi"):
        return Hindi_styles
    if detect(args, "colors hindi"):
        return Hindi_colors
    else:
        return f" * Invalid command: [{args}]"

