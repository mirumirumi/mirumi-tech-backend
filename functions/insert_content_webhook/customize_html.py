import re
import urllib.parse
from opengraph_py3 import OpenGraph


def customize_html(html: str) -> str:
    # remove `\n` except in code blocks
    # html = remove_n(html)

    # add TOC attributes
    html = add_toc_attrs(html)

    # convert `[http(s)://~~~]` -> blog card
    html = convert_to_blogcard(html)

    # convert `:::info/alert/rewrite` -> common box
    html = convert_to_common_box(html)
    


    return html


# def remove_n(html: str) -> str:
#     return


def add_toc_attrs(html: str) -> str:
    headings = re.findall("((<h[234])>(.*?)(<\/h[234]>))", html)

    for i, head in enumerate(headings):
        html = re.sub(headings[i][0], f"{head[1]} id=\"{urllib.parse.quote(head[2])}\" class=\"toc_item\" data-toc-index=\"{i + 1}\">{head[2]}{head[3]}", html)

    return html


def convert_to_blogcard(html: str) -> str:
    links = re.findall("(<p.*?>\[(https?://(.*?))\]<\/p>)", html) # https://regex101.com/r/7rZSTQ/1

    blogcard_tags = """
        <a href="##fullpath##" class="blogcard" rel="noopener" target="_top">
            <div class="blogcard">
                <div class="thumbnail">
                    <img src="##image##" alt="##title##" />
                </div>
                <div class="content">
                    <div class="title">
                        ##title##
                    </div>
                    <div class="snippet">
                        ##description##
                    </div>
                    <div class="footer">
                        <div class="favicon">
                            <img src="https://www.google.com/s2/favicons?domain=##domain##" alt="external-site-favicon" />
                        </div>
                        <div class="domain">
                            ##domain##
                        </div>
                    </div>
                </div>
            </div>
        </a>
    """

    for link in links:
        fullpath: str = link[1]
        image: str = OpenGraph(link[1])["image"]
        domain: str = re.sub("^(https?:\/\/)?([^\/]+).*$", "\\2", link[2])
        title: str = OpenGraph(link[1])["title"]
        description: str = OpenGraph(link[1])["description"]

        blogcard_tags = blogcard_tags.replace("##fullpath##", fullpath)
        blogcard_tags = blogcard_tags.replace("##image##", image)
        blogcard_tags = blogcard_tags.replace("##domain##", domain)
        blogcard_tags = blogcard_tags.replace("##title##", title)
        blogcard_tags = blogcard_tags.replace("##description##", description)

        html = html.replace(link[0], blogcard_tags)

    return html


def convert_to_common_box(html: str) -> str:
    boxes = re.findall("(<p>:::(info|alert|rewrite\s*\d+)\n*(.*?)<\/p>\n+((<p>.*?<\/p>\n+)*)\n+<p>(.*?)\n*:::<\/p>)", html)  # https://regex101.com/r/epW7pO/1
    replace_to = ""

    for box in boxes:
        if box[1] == "info":
            replace_to = "<div class=\"box-common box-info\">"
        elif box[1] == "alert":
            replace_to = "<div class=\"box-common box-alert\">"
        elif "rewrite" in box[1]:
            replace_to = "<div class=\"box-common box-rewrite\">"

        html = html.replace(box[0], replace_to + "<p>" + box[2] + "</p>" + box[3] + "<p>" + box[5] + "</p>" + "</div>")

    return html
