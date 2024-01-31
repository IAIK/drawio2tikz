The goal of this project is to translate .drawio/XML files into tikz code to integrate in LateX which is readable and adaptable afterwards.

This first version was developed by Arthur Lippitz at Graz University of Technology as part of his bachelor thesis.

----------------------------------------------------------------------

## Documentation

----------------------------------------------------------------------

## **Important Information:**

The file you need to use is "drawio2tikz.py".\
You can use a .xml file or .drawio file as input, anything else will be rejected.

----------------------------------------------------------------------

### **Currently supported actions:**
* rectangles
* circles/ellipses
* diamonds
* arrows
* lines
* text
* groups(/scopes)
* curly braces
* edge labels
* merge or storage
* tables
* clouds
* checkmarks
* logic gates
* transistors
* position of diodes
* position of images but not images themselves

----------------------------------------------------------------------

### **How to use:**

To use the Tool you first have to install the package webcolors (pip install webcolors).\
In the Latex file you will need the package \usepackage{tikz_anchors} for most pictures and some others specified in the requirements.md file.

Then you can simply run the program like any python file with the XML file which should be your second argument. (e.g. python3 drawio2tikz.py /absolute/path/of/file).\
In case you do not use the absolute path please ensure it is the correct relative path.\
If for any reason someone does not want to use the command line, one can also use pycharm for example and use the path as an argument or edit the **parseArguments()** function.

The code will generate a TikZ picture for you from an XML or .drawio file.

**WARNING**: It will only work if you have the complete XML or .drawio file and not a compressed one! \
It is not yet fully tested with drawio files only with XML files. \
It is still unclear what will exactly happen if there are multiple pages in a drawio file (undefined behaviour). \
It is up to the user to provide proper files which contain one image and in the best case in XML format.

The generated picture will have a structure something like this:

	\resizebox{\hsize}{!}{ 
	\begin{tikzpicture}[scale = 0.2]
	\definecolor{white}{RGB}{255,255,255}
	\node (rect) at (42.0, -0.5) [align=center,draw,minimum width=2.4 cm,minimum height=0.6 						cm,text width=2.4cm,inner sep=0](IDP-20) {{Directory}};
	\draw (IDP-20.south)edge[-stealth](IDP-10.north);
	\end{tikzpicture}}

----------------------------------------------------------------------

### **Adapt the configuration:**

In case you need or want more predefined Colours, simply add them to the "configurations.ini" file in the way all the other colors are encoded in there.\
In case there are Unicode characters frequently occurring and causing issues in the TikZ they can be added to the config and will be replaced automatically. \
In case there needs to be something inside a circle it can be added in the Circled Unicode section in the configuration to be replaced automatically.

----------------------------------------------------------------------

### **Known issues and bugs:**

Keep in mind that this code is not suitable for every picture, since there are a lot of XML commands and not all of them are covered.  
If a picture has too many elements with insufficient spacing it will lead to some issues with the placement,
which will have to be adapted manually afterward. 
Arrows with edge labels not properly positioned depending on the use.  
The font size differs quite a lot in drawio so, it is not always translated but still in a way that it looks fine but not identical to the original.
It can be manually adapted but an automated way was not possible due to too many factors influencing the text size and linebreaks.  
Arrows with corners will not always work only if there are some control points in the XML file otherwise they will be straight.  
Not all pictures will be translated correctly, there surely are still bugs which aren't fixed yet, especially regarding arrows.

----------------------------------------------------------------------

#### **Some resources:**

Resources for tikz linestyles: https://tex.stackexchange.com/questions/45275/tikz-get-values-for-predefined-dash-patterns \
Resources for tikz arrowstyles: https://tikz.dev/tikz-arrows

----------------------------------------------------------------------
