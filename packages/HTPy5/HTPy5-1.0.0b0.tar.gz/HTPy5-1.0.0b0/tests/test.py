from HTPy5 import WeBBuild
from HTPy5.Webgets import Widgets
    
builder = WeBBuild()
builder.setup(title="My Page",
              lang="en",
              description="That is my webpage")
    
builder.addLinking(LinkFileName="style.css", LinkType="stylesheet")
builder.addLinking(LinkFileName="responsive.css", LinkType="stylesheet")
builder.addLinking(LinkFileName="print.css", LinkType="stylesheet")
    
builder.addMeta("author", "BoodyWin Workshop")
builder.addMeta("keywords", "python, web development, meta tags")
    
builder.addNewBodyElement(Widgets.button("that is a button"))
    
if __name__ == "__main__":
    html = builder.generateHTML()
    with open("index.html","w") as f:
        f.write(html)