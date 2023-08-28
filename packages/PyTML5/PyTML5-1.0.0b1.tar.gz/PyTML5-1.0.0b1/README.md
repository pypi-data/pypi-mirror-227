# __PyTML5__

**PyTML5** is a python module used to make static html webpages using python syntax

## Functions

### setup()

A function used to setup the first things at the webpage and they are the `Language` and the `Title`,and the user can't make the webpage without adding the setup code but he can just write it without adding something but it will set the title and the language to defult.

### setDescription()

A function used to add description to the html code, returns a string like that
```html
<meta name="description" content="{YourWebpage Description}">
```

### addLinking()

A function used to link a file with the html code, returns a string like that
```html
<link rel="{type of the linking}" herf="linkedFile">
```

### setCharset()

A function used to set the charset of the webpage like UTF-8,returns a string like that
```html
<meta charset="UTF-8">
```

### setViewport()

A function used to set the viewport of the webpage like `initial-scale`,`width` and `height`,returns a string like that
```html
<meta name="viewport" content="{your content}">
```

### addMeta()

A function used to add a custom meta (as name and content only),returns a string like that
```html
<meta name="{your meta name}" content="your meta content">
```

### addCustomMeta()

A function used to add a custom meta (as you want),returns like that
```html
<meta {your attributes}>
```

### addNewHeadElement()

A function used to make anew two sides element like `<element></element>`

### addNewBodyElement()

A function used to add an elementto the body,but with another module at PyTML named `Webgets`and can return with one side element or two sides element

### generateHTML()

This is the most important function,and its used to generate the html after adding elements and returns it as string