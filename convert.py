import re
import sys
import os

def parse_parts(java_code):
    parts = []

    # Match each definitions
    pattern = re.compile(
        r'PartDefinition\s+(\w+)\s*=\s*(\w+)\.addOrReplaceChild\(\s*"(\w+)",(.*?)\);',
        re.DOTALL
    )

    matches = pattern.findall(java_code)

    for var_name, parent, name, body in matches:
        
        # Fixed the thing where it kinda just only grabbed the first cube
        cube_pattern = re.compile(r'texOffs\((\d+),\s*(\d+)\)\.addBox\((.*?)\)', re.DOTALL)
        cube_matches = cube_pattern.findall(body)
        
        cubes = []
        for texX, texY, box_vals in cube_matches:
            cubes.append({
                "texX": int(texX),
                "texY": int(texY),
                "box": box_vals
            })

        # Take parent offset
        offset = re.search(r'PartPose\.offset\(([^)]+)\)', body)
        offset_vals = offset.group(1) if offset else "0.0F, 0.0F, 0.0F"

        parts.append({
            "name": name,
            "parent": parent,
            "cubes": cubes,
            "offset": offset_vals
        })

    return parts

def convert_addbox(box_str):
    args = box_str.split(",")
    args = args[:6]

    cleaned = []
    for i, arg in enumerate(args):
        arg = arg.strip().replace("F", "")

        if i < 3:
            cleaned.append(f"{float(arg)}F")
        else:
            cleaned.append(str(int(float(arg))))

    return ", ".join(cleaned)

def convert_part(part, part_lookup):
    ox, oy, oz = get_world_offset(part, part_lookup)
    
    # It needed it before, idk why it isnt needed now
    # If the model is shifted up by 24 units, uncomment this line below
    # oy += 24 

    if oz == 0:
        oz = -1

    result_str = ""
    
    for i, cube in enumerate(part["cubes"]):
        suffix = "" if i == 0 else str(i)
        current_name = f"{part['name']}{suffix}"
        
        box = convert_addbox(cube["box"])

        result_str += f"""
        this.{current_name} = new ModelRenderer({cube['texX']}, {cube['texY']});
        this.{current_name}.addBox({box});
        this.{current_name}.setRotationPoint({ox}F, {oy}F, {oz}F);"""

    return result_str + "\n"

def generate_model(class_name, parts, part_lookup):
    output = f"""// Converted with BakewellAlphaConverter
// Exported for Decompiled Minecraft Alpha 1.1.2_01 and similar versions

public class Model{class_name} extends ModelBase {{

"""

    # Without cubes, just ignore it we dont need that
    visible_parts = [p for p in parts if p["cubes"]]
    for p in visible_parts:
        for i in range(len(p["cubes"])):
            suffix = "" if i == 0 else str(i)
            output += f"    public ModelRenderer {p['name']}{suffix};\n"

    output += "\n    public Model" + class_name + "() {\n"
    output += "        TexturedQuad.setTextureSize(128, 128);\n"
    for p in visible_parts:
        output += convert_part(p, part_lookup)

    output += "\n    }\n\n"
    output += "    public void render(float f, float f1, float f2, float f3, float f4, float scale) {\n"

    # Rendering stuff
    for p in visible_parts:
        for i in range(len(p["cubes"])):
            suffix = "" if i == 0 else str(i)
            output += f"        this.{p['name']}{suffix}.render(scale);\n"

    output += "    }\n}\n"

    return output

def get_world_offset(part, part_lookup):
    ox, oy, oz = map(float, part["offset"].replace("F", "").split(","))

    parent_name = part["parent"]

    # Recursively add offsets
    if parent_name in part_lookup:
        pox, poy, poz = get_world_offset(part_lookup[parent_name], part_lookup)
        return ox + pox, oy + poy, oz + poz

    return ox, oy, oz

def run_conversion(input_path):
    file = input_path
    
    with open(file, "r") as f:
        code = f.read()

    parts = parse_parts(code)

    part_lookup = {p["name"]: p for p in parts}

    class_name_match = re.search(r'public\s+class\s+(\w+)', code)
    class_name = class_name_match.group(1)

    class_name = class_name.split("<")[0]
    class_name = class_name[0].upper() + class_name[1:]

    result = generate_model(class_name, parts, part_lookup)

    output_dir = os.path.dirname(input_path)
    output_filename = f"Model{class_name}.java"
    final_output_path = os.path.join(output_dir, output_filename)

    with open(final_output_path, "w") as f:
        f.write(result)
    
    return final_output_path

def main():
    if len(sys.argv) < 2:
        return
        
    file = sys.argv[1]

    with open(file, "r") as f:
        code = f.read()

    parts = parse_parts(code)

    part_lookup = {p["name"]: p for p in parts}

    class_name_match = re.search(r'public\s+class\s+(\w+)', code)
    class_name = class_name_match.group(1)

    class_name = class_name.split("<")[0]
    class_name = class_name[0].upper() + class_name[1:]

    result = generate_model(class_name, parts, part_lookup)

    with open(f"Model{class_name}.java", "w") as f:
        f.write(result)

if __name__ == "__main__":
    main()