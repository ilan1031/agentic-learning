def chunk_policy(text, max_chars=500):
    """Split policy text into meaningful sections"""
    sections = []
    current_section = ""
    
    # Split by major headings
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Detect section headers
        if line.startswith(('## ', '# ', '**', '•', '➢')) or line.isupper():
            if current_section:
                sections.append(current_section)
                current_section = ""
                
        current_section += line + " "
        
        # Split long sections
        if len(current_section) > max_chars:
            sections.append(current_section)
            current_section = ""
    
    if current_section:
        sections.append(current_section)
        
    return sections