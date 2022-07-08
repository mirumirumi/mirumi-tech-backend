import re


def customize_html(html: str) -> str:

    # add TOC attributes
    html = add_toc_attrs(html)

    # convert `[http(s)://~~~]` -> blog card
    html = convert_to_blogcard(html)








def add_toc_attrs(html: str) -> str:
    headings = re.findall("((<h[234])>(.*?)(<\/h[234]>))", html)

    for i, head in enumerate(headings):
        html = re.sub(headings[i][0], f"{head[1]} id=\"{urllib.parse.quote(head[2])}\" class=\"toc_item\" data-toc-index=\"{i + 1}\">{head[2]}{head[3]}", html)

    return html


def convert_to_blogcard(html: str) -> str:
    links = re.findall("(<p.*?>\[(https?://(.*?))\]<\/p>)", html) # https://regex101.com/r/7rZSTQ/1

    blogcard_tags = """
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
    """

    for link in links:
        image: str = OpenGraph(link[1])["image"]
        domain: str = re.sub("^(https?:\/\/)?([^\/]+).*$", "\\2", link[2])
        title: str = OpenGraph(link[1])["title"]
        description: str = OpenGraph(link[1])["description"]

        blogcard_tags = blogcard_tags.replace("##image##", image)
        blogcard_tags = blogcard_tags.replace("##domain##", domain)
        blogcard_tags = blogcard_tags.replace("##title##", title)
        blogcard_tags = blogcard_tags.replace("##description##", description)

        html = html.replace(link[0], blogcard_tags)

    return html
