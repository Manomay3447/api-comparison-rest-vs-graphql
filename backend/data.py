users = [
    {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@mail.com",
        "address": {
            "street": f"{i} Main St",
            "city": "Sampleville",
            "zipcode": f"000{i % 100:02}"
        },
        "company": {
            "name": f"Company{i % 10}",
            "department": "Engineering"
        }
    }
    for i in range(1, 10001)
]

