"""# PyTML\n
| is a module made to make the website making more better with python,that is an experiment version
\n
Here is a simple example :\n
```python
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
    
```
Copyright(c) by BoodyWin Workshop


Note : Some notes is AI generated.
"""
#   ________              _____________________   __                __    __
#  |   ____  \           |________    _________| |  \              /  |  |  |  
#  |  |    |  |                   |  |           |   \            /   |  |  |   ________
#  |  |    |  |  ___      ___     |  |           |    \          /    |  |  |  |  ______|
#  |  |____|  |  \  \    /  /     |  |           |     \        /  |  |  |  |  |  |____
#  |   ______/    \  \  /  /      |  |           |  |\  \      /  /|  |  |  |  |_____  \
#  |  |            \  \/  /       |  |           |  | \  \    /  / |  |  |  |        \  |
#  |  |             \    /        |  |           |  |  \  \  /  /  |  |  |  |   _____/  |
#  |  |              |  |         |  |           |  |   \  \/  /   |  |  |  |  |_______/
#  |  |              |  |         |  |           |  |    \    /    |  |  |  |___________
#  |__|              |__|         |__|           |__|     \__/     |__|  |______________|
# 
#                                                      _____   _____   _______       /\
#  __      __    ___         _______        _______   |     \ |  ___| |__   __|     /  \    ▄█ 
#  \ \    / /   |_  |       |  ___  |      |  ___  |  |_____/ | |___     | |       / /\ \    █ 
#   \ \  / /      | |       | |   | |      | |   | |  |     \ |  ___|    | |      / /__\ \  ▄█▄
#    \ \/ /      _| |_   _  | |___| |   _  | |___| |  |      || |___     | |     / ______ \
#     \__/      |_____| |_| |_______|  |_| |_______|  |_____/ |_____|    |_|    /_/      \_\

class SetupError(Exception):
    """
    Raised when the `WeBBuild` object is not set up before calling `generateHTML()`.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message: str = "Cannot generate the HTML without setting up the webpage (or calling `setup()` in the main code).") -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message



class WeBBuild:
    def __init__(self):
        """The `__init__()` method is called when a new `WeBBuild` object is created. It initializes the object's attributes.
        """
        self.setuped = False
        self.title = ""
        self.lang = ""
        self.descripe = ""
        self.links = []
        self.charset = "<meta charset=\"UTF-8\">"
        self.viewport = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
        self.meta_tags = []
        self.elements = []
        self.Helements = []

    def setup(self, title: str = "Document", lang: str = "en"):
        """The `setup()` method is used to initialize the `WeBBuild` object.

        Args:
            title (str, optional): The title of the webpage. Defaults to "Document".
            lang (str, optional): The language of the webpage. Defaults to "en".
        """
        self.lang = lang
        self.title = f"<title>{title}</title>"
        self.setuped = True
        

    def setDescription(self, description: str):
        """The `setDescription()` method is used to set the description of the webpage

        Args:
            description (str): The description of the webpage.
            
        Returns:
            str: The description meta of the webpage.
        """
        self.descripe = f"<meta name=\"description\" content=\"{description}\">"
        
        return self.descripe

    def addLinking(self, LinkFileName: str, LinkType: str = "stylesheet"):
        """The `addLinking()` method is used to add a link to the webpage.

        Args:
            LinkFileName (str): The href of the link.
            LinkType (str, optional): The type of the link. Defaults to "stylesheet".

        Returns:
            str: The tag of the link.
        """
        link_tag = f"<link rel=\"{LinkType}\" href=\"{LinkFileName}\">"
        self.links.append(link_tag)
        
        return link_tag

    def setCharset(self, charset: str = "UTF-8"):
        """The `setCharset()` method is used to set the character set of the webpage.

        Args:
            charset (str, optional): The character set of the webpage. Defaults to "UTF-8".

        Returns:
            str: The character set meta of the webpage.
        """
        self.charset = f"<meta charset=\"{charset}\">"
        
        return self.charset

    def setViewport(self, initial_scale: float = 1.0, width: str = "device-width", height: str = None):
        """The `setViewport()` method is used to set the viewport of the webpage.

        Args:
            initial_scale (float, optional): The initial scale of the viewport. Defaults to 1.0.
            width (str, optional): The width of the viewport. Defaults to "device-width".
            height (str, optional): The height of the viewport. Defaults to None.

        Returns:
            str: The viewport meta of the webpage.
        """
        metas = f"initial-scale={initial_scale}, width={width}"
        if height:
            metas += f", height={height}"

        self.viewport = f"<meta name=\"viewport\" content=\"{metas}\">"
        
        return self.viewport

    def addMeta(self, MeName: str, MeContent: str):
        """The `addMeta()` method is used to add a meta tag to the webpage.

        Args:
            MeName (str): The name of the meta tag.
            MeContent (str): The content of the meta tag.

        Returns:
            str: The tag of the meta.
        """
        meta_tag = f"<meta name=\"{MeName}\" content=\"{MeContent}\">"
        self.meta_tags.append(meta_tag)
        
        return meta_tag
        
    def addCustomMeta(self,**attributes):
        """The `addCustomMeta()` method is used to add a custom meta tag to the webpage.

        Returns:
            str: The custom meta.
        """
        meta_attr = " ".join([f"{attr}='{val}'" for attr, val in attributes.items()])
        self.meta_tags.append(f"<meta {meta_attr}>")
        
        return f"<meta {meta_attr}>"
        
    def addNewHeadElement(self,Element: str,Content: str,ID: str = None,NAME: str=None,CLASS: str=None,**attributes):
        """The `addNewHeadElement()` method is used to add a new element to the head of the webpage.

        Args:
            Element (str): The name of the element.
            Content (str): The content of the element.
            ID (str, optional): The id of the element. Defaults to None.
            NAME (str, optional): The name of the element. Defaults to None.
            CLASS (str, optional): The class of the element. Defaults to None.
            **attributes: The key-value pairs of the element attributes.

        Returns:
            str: The head element tag.
        """
        element_attr = " ".join([f"{attr}='{val}'" for attr, val in attributes.items()])
        element_attr += f"id='{ID}'" if ID else ""
        element_attr += f"id='{CLASS}'" if CLASS else ""
        element_attr += f"id='{NAME}'" if NAME else ""
        self.Helements.append(f"<{Element} {element_attr}>{Content}</{Element}>")
        
        return f"<{Element} {element_attr}>{Content}</{Element}>"

    def addNewBodyElement(self,Widget):
        """The `addNewBodyElement()` method is used to add a new element to the body of the webpage.

        Args:
            Widget (Webgets): The widget from webgets.

        Returns:
            str: The widget tag.
        """
        self.elements.append(Widget)
        return Widget
    
    def generateHTML(self):
        """The `generateHTML()` method is used to generate the HTML code for the webpage.
        
        Returns:
            str : The HTML code for the webpage.
        """
        if self.setuped == True:
            all_meta_tags = "\n    ".join(self.meta_tags) if self.meta_tags != [] else ""
            all_css_links = "\n    ".join(self.links) if self.links != [] else ""
            all_elements = "\n    ".join(self.elements) if self.elements != [] else ""
            all_head_elements = "\n    ".join(self.Helements) if self.Helements != [] else ""
            lang = f" lang=\"{self.lang}\"" if self.lang else ""
            html = f"""<!DOCTYPE html>
<html{lang}>
<head>
    {self.title}
{"    "+self.descripe if self.descripe != "" else ""}
    {all_css_links}
{"    "+self.charset if self.charset != "" else ""}
{"    "+self.viewport if self.viewport != "" else ""}
    {all_meta_tags}
    {all_head_elements}
</head>
<body>
    {all_elements}
</body>
</html>"""
            return html
        else:
            raise SetupError("Cannot Generate the html witout setuping the webpage (Or writing `setup()` at the main code).")

__all__ = ['Webgets','WeBuild']
__version__ = "1.0.0b1"

# Example usage:
if __name__ == "__main__":
    from Webgets import *
    
    builder = WeBBuild()
    builder.setup(title="My Page", lang="en")
    builder.setDescription("This is my webpage.")
    
    # Adding multiple CSS files
    builder.addLinking(LinkFileName="style.css", LinkType="stylesheet")
    builder.addLinking(LinkFileName="responsive.css", LinkType="stylesheet")
    builder.addLinking(LinkFileName="print.css", LinkType="stylesheet")
    
    builder.setCharset(charset="UTF-8")
    builder.setViewport(initial_scale=1.0, width="device-width", height=None)
    
    # Adding custom meta tags
    builder.addMeta("author", "BoodyWin Workshop")
    builder.addMeta("keywords", "python, web development, meta tags")
    
    builder.addNewBodyElement(Widgets.button("that is a button"))
    
    # Generate the HTML and print it
    html = builder.generateHTML()
    print(html)
