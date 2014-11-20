import os.path
import re

def extract_vocabularies(fileobj, keywords, comment_tags, options):
    """Extract messages from files.
    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: a list of keywords (i.e. function names) that should
                     be recognized as translation functions
    :param comment_tags: a list of translator tags to search for and
                         include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``
    """
    exec_globals = {}
    exec fileobj in exec_globals
    if 'vocabularies' in exec_globals:
        vocabularies = exec_globals.get('vocabularies')
        j = 0
        for name, vocab in vocabularies.items():
            for term in vocab:
                k, title = term
                # j is not actually the line number, use only to distinguish terms
                yield (j, '_', title, ['A term of vocabulary: %s' % name])
