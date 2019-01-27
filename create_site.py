
import yaml
import bibtexparser
from jinja2 import Environment, PackageLoader


SITE_FILENAME = "site.yaml"
PUBS_FILENAME = "pubs.bib"
JOURNAL_BIB = "bibs/journals.bib"
CONFERENCES_BIB = "bibs/conferences.bib"
THESES_BIB = "bibs/theses.bib"
OTHER_BIB = "bibs/other.bib"
env = Environment(loader=PackageLoader(__name__, 'templates'))


def load_site_yaml(fname):
    with open(fname) as f:
        return yaml.load(f.read())


def create_site():
    site = load_site_yaml(SITE_FILENAME)
    template = env.get_template("index.html")
    projects = create_projects(site["projects"])
    journals = create_pubs(JOURNAL_BIB)
    conferences = create_pubs(CONFERENCES_BIB)
    theses = create_pubs(THESES_BIB)
    # other_pubs = create_pubs(OTHER_BIB)
    return template.render(
        bio_image=site["bio_image"],
        bio=site["bio"],
        position=site["position"],
        blurb=site["blurb"],
        projects=projects,
        journals=journals,
        conferences=conferences,
        theses=theses)


def make_link(title, link):
    return '<a href="{}">{}</a>'.format(link, title)


def create_projects(projs):
    template = env.get_template("project.html")
    proj_htmls = list()
    for proj in projs:
        pub_list = list()
        news_list = list()
        video_list = list()
        image = proj["image"]
        name = proj["name"]
        for link in proj["links"]:
            link_str = make_link(link["title"], link["link"])
            if link["type"] == "pub":
                pub_list.append(link_str)
            elif link["type"] == "news":
                news_list.append(link_str)
            elif link["type"] == "video":
                video_list.append(link_str)
        html = template.render(
            news_list=news_list, pub_list=pub_list, video_list=video_list,
            image=image, name=name)
        proj_htmls.append(html)
    return proj_htmls


def format_authors(authors):
    names = authors.split(" and ")
    formatted_names = list()
    for name in names:
        last, first = name.split(", ")
        first_initial = first[0]
        formatted_names.append("{}. {}".format(first_initial, last))
    if len(formatted_names) == 1:
        return formatted_names[0]
    elif len(formatted_names) == 2:
        return " and ".join(formatted_names)
    else:
        return ", ".join(formatted_names[:-1]) + ", and " + formatted_names[-1]


def create_pubs(bib_fname):
    template = env.get_template("pub.html")
    pubs = list()
    with open(bib_fname) as f:
        bib = bibtexparser.loads(f.read())
    for entry in bib.entries:
        authors = format_authors(entry["author"])
        year = entry["year"]
        title = entry["title"]
        for ven in ["booktitle", "journal", "school"]:
            try:
                venue = entry[ven]
            except KeyError:
                pass
        pages = entry.get("pages")
        link = entry.get("link")
        pubs.append(template.render(
            authors=authors,
            year=year,
            title=title,
            venue=venue,
            pages=pages,
            link=link))
    return pubs


if __name__ == "__main__":
    html = create_site()
    with open("index.html", "w") as f:
        f.write(html.encode('ascii', 'ignore'))
