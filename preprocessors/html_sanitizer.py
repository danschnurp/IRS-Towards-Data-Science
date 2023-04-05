
def sanitize_for_html_tags(html_string):
    """
    The function sanitizes a given HTML string by replacing certain characters with their corresponding HTML escape codes.

    :param html_string: The input string that may contain characters that need to be escaped for use in HTML tags
    :return: the sanitized version of the input `html_string` where certain characters have been replaced with their
    corresponding HTML escape codes.
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
