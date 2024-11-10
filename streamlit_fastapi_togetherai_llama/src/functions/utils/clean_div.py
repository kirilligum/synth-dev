from bs4 import BeautifulSoup, Comment

def remove_script_css(input_file):
    # Open and read the input HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Remove all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Remove all link tags for CSS, JS files, img tags, forms, and inputs
    for element in soup.find_all(["link", "script", "img", "form", "input", "nav", "footer", "button", "iframe", "svg", "object", "embed"]):
        element.decompose()   

     # Clear attributes from all elements to keep only the tag and its text content
    for element in soup.find_all(True):
        element.attrs = {}

    # Remove comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Enhanced function to recursively remove empty elements and collapse redundant tags more effectively
    def collapse_redundant_tags(element):
        for child in list(element.children):
            if child.name:
                # Recursively collapse before checking for emptiness to handle nested empty elements
                collapse_redundant_tags(child)
                
                # After collapsing, check if the element is now empty and remove it if so
                if not child.text.strip() and not child.find_all(True):
                    child.decompose()
                else:
                    # Check for redundant tags after removing empty elements
                    if len(child.find_all(recursive=False)) == 1:
                        grandchild = child.find(recursive=False)
                        if child.name == grandchild.name:
                            child.replace_with(grandchild)
                            collapse_redundant_tags(element)

    # Collapse redundant tags in the soup
    collapse_redundant_tags(soup)

    # Remove empty lines from the output HTML
    html_output = '\n'.join([line for line in str(soup).splitlines() if line.strip()])
    return html_output

if __name__ == "__main__":
    cleaned_html = remove_script_css("./landing_page.html")
    with open("./landing_page_nojscss.html", 'w', encoding='utf-8') as file:
        file.write(cleaned_html)
