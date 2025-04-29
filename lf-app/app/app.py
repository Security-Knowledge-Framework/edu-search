from flask import Flask, render_template, jsonify, request
import json, os

app = Flask(__name__, static_folder='static')


def load_json(file_json):
    with open(file_json, "r", encoding="utf-8") as f:
        return json.load(f)

def search_courses(query, max_results=100):
    query = query.lower()
    keywords = query.split()
    file_json = "data/linuxfoundation_courses.json"
    courses = load_json(file_json)
    results = []

    for course in courses:
        score = 0
        title = course.get("title", "").lower()
        description = course.get("description", "").lower()
        category = course.get("category", "").lower()
        difficulty = course.get("difficulty", "").lower()

        for kw in keywords:
            if kw in title:
                score += 3
            if kw in description:
                score += 2
            if kw in category:
                score += 10
            if kw in difficulty:
                score += 1

        if score > 0:
            results.append((score, course))

    results.sort(reverse=True, key=lambda x: x[0])
    return [r[1] for r in results[:max_results]]


@app.route('/')
def roles():
    return render_template("roles.html")

@app.route('/role/<name>')
def role(name):
    # Load course catalog and map by ID
    course_data = load_json("data/linuxfoundation_courses.json")
    course_map = {course["id"]: course for course in course_data}

    # Load learning path per role
    role_path = load_json("data/role_learning_paths_kernel.json")

    # Enrich role_path with full course info
    for level in role_path:
        enriched = []
        for entry in role_path[level]["courses"]:
            course_id = entry.get("id")
            if course_id in course_map:
                enriched.append(course_map[course_id])
        role_path[level]["courses"] = enriched
    return render_template("role.html", role_tracks=role_path, job_name=name)

@app.route('/courses')
def courses():
    with open("data/linuxfoundation_courses.json", "r", encoding="utf-8") as f:
        courses_data = json.load(f)
    return render_template("courses.html", courses=courses_data)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Missing search query: use /search?q=keyword"}), 400

    results = search_courses(query)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
