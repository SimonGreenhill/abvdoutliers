import re
from pathlib import Path

from nameparser import HumanName
from cldfbench.datadir import DataDir
from clldutils.misc import slug
from pylexibank.providers import abvd
from pylexibank.util import progressbar
from pylexibank import FormSpec


def normalize_contributors(l):
    for key in ['checkedby', 'typedby']:
        l[key] = normalize_names(l[key])
    return l


def normalize_names(names):
    res = []
    if names:
        for name in re.split('\s+and\s+|\s*&\s*|,\s+|\s*\+\s*', names):
            name = {
                'Simon': 'Simon Greenhill',
                'D. Mead': 'David Mead',
                'Alex François': 'Alexandre François',
                'Dr Alex François': 'Alexandre François',
                'R. Blust': 'Robert Blust',
            }.get(name, name)
            name = HumanName(name.title())
            res.append('{0} {1}'.format(name.first or name.title, name.last).strip())
    return ' and '.join(res)


class Dataset(abvd.BVD):
    dir = Path(__file__).parent
    id = 'abvdoutliers'
    SECTION = 'austronesian'
    
    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")"},
        separators=";/,~",
        missing_data=('-', ),
        strip_inside_brackets=True
    )

    def __init__(self, concepticon=None, glottolog=None):
       super().__init__(concepticon, glottolog)
       self.language_ids = [int(r['ID']) for r in self.languages]
    
    def cmd_makecldf(self, args):
        args.writer.add_sources(*self.etc_dir.read_bib())
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split('-')[-1]+ '_' + slug(c.english),
            lookup_factory=lambda c: c['ID'].split('_')[0]
        )
        for wl in progressbar(self.iter_wordlists(args.log), desc="cldfify"):
            wl.to_cldf(args.writer, concepts)
            # Now normalize the typedby and checkedby values:
            args.writer.objects['LanguageTable'][-1] = normalize_contributors(args.writer.objects['LanguageTable'][-1])
