import requests, json, os, uuid
from bs4 import BeautifulSoup


URL = "https://training.linuxfoundation.org/full-catalog/"
OUTPUT_FILE = "../data/linuxfoundation_courses.json"
# Load existing data (if file exists)
existing_courses = []
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_courses = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Warning: JSON file was invalid. Starting fresh.")
        existing_courses = []

existing_by_url = {c["url"]: c for c in existing_courses}

# Scrape latest data
response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
current_courses = []

for card in soup.select("a.lf-owl-card.product-card"):
    title = card.select_one(".lf-owl-card-title")
    description = card.select_one(".lf-owl-card-description")
    category = card.select_one(".lf-owl-card-id")
    price = card.select_one(".lf-owl-card-price")
    difficulty_tag = card.select_one(".lf-owl-card-difficulty i")
    difficulty = difficulty_tag.get("data-difficulty", "").strip() if difficulty_tag else ""
    url = card["href"]
    # Inference logic for product type
    product_type = "Training"
    if "/certification/" in url:
        product_type = "Certification"
    elif "/bundle/" in url:
        product_type = "Bundle"
    elif "/express-learning/" in url:
        product_type = "Express Learning"
    elif "/skillcred/" in url:
        product_type = "SkillCred"
    elif "/training/" not in url:
        product_type = "Other"

    # Generate a consistent UUID based on the course URL
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, url))

    course = {
        "id": uid,
        "title": title.get_text(strip=True) if title else "",
        "description": description.get_text(strip=True) if description else "",
        "category": category.get_text(strip=True) if category else "",
        "difficulty": difficulty,
        "price": price.get_text(strip=True) if price else "",
        "product_type": product_type,       
        "url": url
    }

    current_courses.append(course)

# Build new JSON list:
# - Add new ones
# - Keep only existing ones that are still on the page
current_urls = {c["url"] for c in current_courses}
final_courses = []

added = 0
removed = 0

for course in current_courses:
    if course["url"] not in existing_by_url:
        added += 1
    final_courses.append(course)

for url in existing_by_url:
    if url not in current_urls:
        removed += 1  # This one is no longer live

# Save updated file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_courses, f, indent=2)

print(f"✅ Synced course list. Added: {added}, Removed: {removed}, Total: {len(final_courses)}")