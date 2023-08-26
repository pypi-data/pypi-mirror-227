# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yar_numerals',
 'yar_numerals.lexeme',
 'yar_numerals.lexeme.numeral',
 'yar_numerals.syntax']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yar-numerals',
    'version': '1.0.0',
    'description': 'Number to text - Inflector for Ukrainian numerals',
    'long_description': '# Ukrainian Numbers Spellout\n\nThis library allows to convert the numbers into numerals\n\n## Supported Features\n\n- [x] Number spellout – converting numbers into text (numerals)\n- [x] Numeral inflection - modifying grammatical form of numerals to match required grammatical characteristics\n- [x] Agreement - setting grammatical forms of compound numerals to produce grammatically and syntactically correct text\n- [x] Stress\n- [x] Cardinal numbers in range [0...1×10<sup>27</sup>)<sup>_1_, _2_</sup>\n- [x] Ordinal numbers in range [0...1×10<sup>27</sup>)<sup>_1_</sup>\n- [x] Fractional numbers with whole, each element in range [0...1×10<sup>27</sup>)\n- [x] Decimal numbers in range (0...1×10<sup>27</sup>) with precision up to 1×10<sup>-27</sup> <sup>_3_</sup>\n\n---\n\n<sup>_1_</sup> Numbers outside of the range will be spelled out digit-wise and inflected only last digit\n\n<sup>_2_</sup> 1×10<sup>27</sup> is 1 000 000 000 000 000 000 000 000 000\n\n<sup>_3_</sup> 1×10<sup>-27</sup> is 0.000 000 000 000 000 000 000 000 001\n\n## Future Features\n\n- [ ] Negative numbers\n- [ ] Contracted ordinal numbers (e.g. "1-й", "1000-на")\n- [ ] Scientific notation of exponential numbers (e.g. "1e5")\n\n## Supported Grammatical Attributes\n\n- cases: nominative, genitive, dative, accusative, instrumental, locative, vocative\n- gender: masculine, feminine, neuter\n- number: singular, plural\n- animacy: inanimate, animate\n',
    'author': 'Yar team',
    'author_email': 'team@yar.org.ua',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://yar.org.ua/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
