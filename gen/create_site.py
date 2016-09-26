
import yaml
import bibtexparser
from jinja2 import Environment, PackageLoader


SITE_FILENAME = "site.yaml"
PUBS_FILENAME = "pubs.bib"
env = Environment(loader=PackageLoader(__name__, 'templates'))


def load_site_yaml(fname):
    with open(fname) as f:
        return yaml.load(f.read())


def create_site():
    site = load_site_yaml(SITE_FILENAME)
    template = env.get_template("index.html")
    projects = create_projects(site["projects"])
    pubs = create_pubs()
    return template.render(
        bio_image=site["bio_image"],
        bio=site["bio"],
        projects=projects,
        pubs=pubs)


def create_projects(projs):
    template = env.get_template("project.html")
    proj_htmls = list()
    for proj in projs:
        pub_list = list()
        title = proj["title"]
        image = proj["image"]
        for link in proj["links"]:
            pub_list.append((link["link"], link["title"]))
        html = template.render(pub_list=pub_list, title=title, image=image)
        proj_htmls.append(html)
    return proj_htmls


def create_pubs():
    template = env.get_template("pub.html")
    pubs = list()
    with open(PUBS_FILENAME) as f:
        bib = bibtexparser.loads(f.read())
    for entry in bib.entries:
        authors = entry["author"]
        year = entry["year"]
        title = entry["title"]
        for ven in ["booktitle", "journal", "school"]:
            try:
                venue = entry[ven]
            except KeyError:
                pass
        pages = entry.get("pages")
        pubs.append(template.render(
            authors=authors,
            year=year,
            title=title,
            venue=venue,
            pages=pages))
    return pubs


if __name__ == "__main__":
    html = create_site()
    with open("index.html", "w") as f:
        f.write(html.encode('ascii', 'ignore'))
