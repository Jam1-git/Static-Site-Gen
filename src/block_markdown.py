def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for i in range(len(blocks)):
        if blocks[i].strip() != "":
            new_blocks.append(blocks[i].strip())
    return new_blocks
    
        
    
