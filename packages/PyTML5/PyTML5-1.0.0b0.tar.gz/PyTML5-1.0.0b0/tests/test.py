from PyTML5 import WeBBuild
from PyTML5.Webgets import Widgets
    
builder = WeBBuild()
builder.setup(title="My Page", lang="en")
builder.setDescription("This is my webpage.")
    
builder.addLinking(LinkFileName="style.css", LinkType="stylesheet")
builder.addLinking(LinkFileName="responsive.css", LinkType="stylesheet")
builder.addLinking(LinkFileName="print.css", LinkType="stylesheet")
    
builder.setCharset(charset="UTF-8")
builder.setViewport(initial_scale=1.0, width="device-width", height=None)
    
builder.addMeta("author", "BoodyWin Workshop")
builder.addMeta("keywords", "python, web development, meta tags")
    
builder.addNewBodyElement(Widgets.button("that is a button"))
    
if __name__ = "__main__":
    html = builder.generateHTML()
    print(html)