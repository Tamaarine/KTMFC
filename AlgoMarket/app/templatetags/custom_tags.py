from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.tag("center")
def center(parser, token):
    """
        Centers the content between the center and endcenter block tags. 
        Takes additional class modifiers for formatting the center div.
    """
    nodelist = parser.parse(("endcenter",))
    parser.delete_first_token()
    return CenterNode(nodelist, " ".join(token.split_contents()[1:]))

class CenterNode(template.Node):
    def __init__(self, nodelist, additional_class_modifiers=""):
        self.nodelist = nodelist
        self.additional_class_modifiers = additional_class_modifiers

    def render(self, context):
        output = self.nodelist.render(context)
        return f'<div class="mx-auto {self.additional_class_modifiers}">{output}</div>'