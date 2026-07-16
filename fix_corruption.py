import re

with open('index.html', 'r') as f:
    content = f.read()

# Find where desc: appears after reviews:812 for p9
p9_desc_pos = content.find("desc:'Omega-3 fatty acid")
if p9_desc_pos != -1:
    # Work backwards to find reviews:812,
    search_back = content[:p9_desc_pos]
    reviews_pos = search_back.rfind("reviews:812,")
    
    if reviews_pos != -1:
        # The corruption is between reviews:812, and desc:
        corruption_start = reviews_pos + len("reviews:812,")
        corruption_end = p9_desc_pos
        
        corrupted_section = content[corruption_start:corruption_end]
        print(f"P9 corrupted section length: {len(corrupted_section)}")
        print(f"First 100 chars: {corrupted_section[:100]}")
        
        # The corrupted section should be replaced with the proper properties
        # Based on the file structure, it should have: pack, form, otc properties
        replacement = "\n    pack:'60 capsules', form:'Softgel capsule', otc:true, rating:4.6, reviews:812,\n    "
        
        new_content = content[:corruption_start] + replacement + content[corruption_end:]
        
        # Now do the same for p13
        p13_desc_pos = new_content.find("desc:'Broad-spectrum fluoroquinolone")
        if p13_desc_pos != -1:
            search_back = new_content[:p13_desc_pos]
            reviews_pos_p13 = search_back.rfind("reviews:221,")
            
            if reviews_pos_p13 != -1:
                corruption_start_p13 = reviews_pos_p13 + len("reviews:221,")
                corruption_end_p13 = p13_desc_pos
                
                corrupted_section_p13 = new_content[corruption_start_p13:corruption_end_p13]
                print(f"P13 corrupted section length: {len(corrupted_section_p13)}")
                
                replacement_p13 = "\n    pack:'10 tablets', form:'Tablet', otc:false, rating:4.6, reviews:221,\n    "
                new_content = new_content[:corruption_start_p13] + replacement_p13 + new_content[corruption_end_p13:]
                
        # Write the fixed content
        with open('index.html', 'w') as f:
            f.write(new_content)
        
        print("File fixed successfully!")
    else:
        print("Could not find reviews:812,")
else:
    print("Could not find desc for p9")
