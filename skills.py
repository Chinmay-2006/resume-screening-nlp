# A predefined list of common technical skills to check for.
# You can expand this list anytime — it directly affects match accuracy.
import re
SKILL_LIST = [
    "java", "python", "c++", "c", "c#", "javascript", "typescript", "sql", "html", "css",
    "spring boot", "spring", "django", "flask", "react", "angular", "vue", "node.js", "nodejs",
    "mongodb", "mysql", "postgresql", "sqlite", "git", "github", "gitlab", "rest api", "api",
    "graphql", "machine learning", "deep learning", "data analysis", "data structures",
    "algorithms", "pandas", "numpy", "excel", "data visualization", "tableau", "power bi",
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "agile", "scrum", "ci/cd",
    "unit testing", "jira", "kotlin", "swift", "php", "ruby", "oop", "dbms", "operating system",
    "computer networks", "cybersecurity", "html5", "css3", "bootstrap", "tailwind", "jenkins"
]



def extract_skills(text):
    """
    Given raw text, find which skills from SKILL_LIST appear in it
    as whole words/phrases (not as substrings of other words).
    Returns a set of matched skills.
    """
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_LIST:
        # \b = word boundary, so "c" won't match inside "algorithmic"
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return found_skills


if __name__ == "__main__":
    sample = "Experienced in Java, Spring Boot, REST API, and SQL. Familiar with Git and Docker."
    print(extract_skills(sample))