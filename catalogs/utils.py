# -*- coding: utf-8 -*-
import re
import unidecode

def slugify(s):
    s = unidecode.unidecode(s).lower()
    return re.sub(r'\W+','-',s)