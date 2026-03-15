from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simulated customer data
customers = [
    {"name": "Alice", "email": "alice@example.com", "interest": "Science Fiction"},
    {"name": "Bob", "email": "bob@example.com", "interest": "Mystery"},
    {"name": "Carol", "email": "carol@example.com", "interest": "Romance"}
]

# SEO generator
def generate_seo(product, keywords):
    return f"""
    <h1>Buy {product} Online</h1>
    <p>Looking for {product}? Discover {', '.join(keywords)} and more!</p>
    <p><b>Tags:</b> {', '.join(keywords)}</p>
    """

# Email generator
def personalize_emails(customers):
    emails = []

    for c in customers:
        subject = f"Hi {c['name']}, check out new {c['interest']} books!"

        body = f"""
Dear {c['name']},

You love {c['interest']} books, and we’ve got new arrivals just for you!
Visit our store and enjoy member-only discounts.

Cheers,
Bookstore Team
"""

        emails.append({
            "email": c["email"],
            "subject": subject,
            "body": body
        })

    return emails


html_template = '''
<!DOCTYPE html>
<html>
<head>
<title>AI Marketing Tool</title>
</head>

<body>

<h2>Generate SEO Content & Personalized Emails</h2>

<form method="POST">
Product: <input name="product" required><br><br>
Keywords (comma-separated): <input name="keywords" required><br><br>
<input type="submit" value="Generate">
</form>

{% if seo_result %}
<h3>SEO Content:</h3>
<div style="border:1px solid #ccc;padding:10px;">
{{ seo_result|safe }}
</div>
{% endif %}

{% if emails %}
<h3>Personalized Emails:</h3>

{% for e in emails %}
<p>
<strong>To:</strong> {{ e.email }}<br>
<strong>Subject:</strong> {{ e.subject }}<br>
<pre>{{ e.body }}</pre>
</p>
{% endfor %}

{% endif %}

</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():

    seo_result = ""
    emails = []

    if request.method == "POST":
        product = request.form["product"]
        keywords = [k.strip() for k in request.form["keywords"].split(",")]

        seo_result = generate_seo(product, keywords)
        emails = personalize_emails(customers)

    return render_template_string(html_template,
                                  seo_result=seo_result,
                                  emails=emails)

if __name__ == "__main__":
    app.run(debug=True)
