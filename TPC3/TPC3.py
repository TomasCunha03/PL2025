import re

def convert_markdown_to_html(md_text):
    lines = md_text.split('\n')
    html_output = []
    temp_list_items = []

    def handle_inline_elements(text):
        # bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # imagens (antes dos links pa evitar conflito)
        text = re.sub(r'!\[([^\]]+?)\]\(([^\)]+?)\)', r'<img src="\2" alt="\1"/>', text)
        # links
        text = re.sub(r'\[([^\]]+?)\]\(([^\)]+?)\)', r'<a href="\2">\1</a>', text)
        return text

    for line in lines:
        # headers
        header_match = re.match(r'^\s*(#+)\s*(.*)', line)
        if header_match:
            level = len(header_match.group(1))
            content = header_match.group(2).strip()
            processed_content = handle_inline_elements(content)
            html_output.append(f"<h{level}>{processed_content}</h{level}>")
            if temp_list_items:
                html_output.append("<ol>")
                html_output.extend([f"<li>{item}</li>" for item in temp_list_items])
                html_output.append("</ol>")
                temp_list_items = []
            continue
        
        # list items numerados
        list_item_match = re.match(r'^\s*(\d+)\.\s*(.*)', line)
        if list_item_match:
            item_content = handle_inline_elements(list_item_match.group(2).strip())
            temp_list_items.append(item_content)
            continue
        
        # output pendentes
        if temp_list_items:
            html_output.append("<ol>")
            html_output.extend([f"<li>{item}</li>" for item in temp_list_items])
            html_output.append("</ol>")
            temp_list_items = []

        # normal text
        processed_line = handle_inline_elements(line)
        html_output.append(processed_line)
    
    # fim da lista items
    if temp_list_items:
        html_output.append("<ol>")
        html_output.extend([f"<li>{item}</li>" for item in temp_list_items])
        html_output.append("</ol>")
    
    return '\n'.join(html_output)

md_input = """
# Example Header
**Bold** text and *italic* text.
1. First point
2. Second point
3. Third point
[Click here](http://example.com) and ![Image example](http://image.com)
"""
html_result = convert_markdown_to_html(md_input.strip())

# save resultado
with open('converted_output.html', 'w') as file:
    file.write(html_result)
