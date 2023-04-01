
def sanitize_for_html_tags(htmlstring):
    escapes = {'\"': '&quot;',
               '\'': '&#39;',
               '<': '&lt;',
               '>': '&gt;'}
    # This is done first to prevent escaping other escapes.
    htmlstring = htmlstring.replace('&', '&amp;')
    for seq, esc in zip(escapes.keys(), escapes.values()):
        htmlstring = htmlstring.replace(seq, esc)
    return htmlstring
