import os
import re

# --- CONFIG ---
DATA_FILE = "js/portfolio-data.js"
# Map folder names to the personas they should appear in
# Folder Name : List of Persona Keys from your JS file
MAPPING = {
    "AI_Data_Analyst": ["analyst", "ai_ml", "generalist"],
    "ai_vision_app": ["scientist", "ai_ml", "generalist"]
}

def get_readme_data(folder):
    readme_path = os.path.join(folder, "README.md")
    if not os.path.exists(readme_path): return None
    with open(readme_path, "r") as f:
        lines = f.readlines()
        title = lines[0].replace("#", "").strip() if lines else folder
        desc = "AI Project"
        for l in lines[1:]:
            if l.strip() and not l.startswith(("#", "-", "*")):
                desc = l.strip()
                break
        return {"title": title, "desc": desc}

def update_js():
    with open(DATA_FILE, "r") as f:
        content = f.read()

    for folder, personas in MAPPING.items():
        data = get_readme_data(folder)
        if not data: continue
        
        # Check if project already exists to prevent infinite duplicates
        if data["title"] in content: continue

        # Format as a JS object
        new_proj = f'{{ title: "{data["title"]}", desc: "{data["desc"]}", link: "{folder}/", tags: ["AI", "Python"] }}'

        for p in personas:
            # This regex finds the 'projects: [' array for the specific persona
            pattern = rf'({p}:\s*\{{[^}}]*?projects:\s*\[)'
            content = re.sub(pattern, rf'\1\n            {new_proj},', content, flags=re.DOTALL)

    with open(DATA_FILE, "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_js()
