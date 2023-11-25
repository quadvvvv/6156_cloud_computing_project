import uuid
import json
from faker import Faker

fake = Faker()

fake_data = []

for _ in range(10):
    user_uuid = str(uuid.uuid4())
    name = fake.name()
    company = fake.company()
    email = fake.email()
    picture_url = None  # or generate a placeholder URL
    fake_data.append({
        "uuid": user_uuid,
        "name": name,
        "company": company,
        "email": email,
        "picture_url": picture_url
    })

with open("fake_data.json", "w") as json_file:
    json.dump(fake_data, json_file, indent=2)
