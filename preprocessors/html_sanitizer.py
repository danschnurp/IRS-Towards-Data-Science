
def sanitize_for_html_tags(html_string):
    """
    escapes html patterns in document
    :param html_string: input string
    :return: 
    """
    escapes = {'\"': '&quot;',
               '\'': '&#39;',
               '<': '&lt;',
               '>': '&gt;'}
    # This is done first to prevent escaping other escapes.
    html_string = html_string.replace('&', '&amp;')
    for seq, esc in zip(escapes.keys(), escapes.values()):
        html_string = html_string.replace(seq, esc)
    return html_string
