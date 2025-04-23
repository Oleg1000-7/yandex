import requests

print(requests.get("http://localhost:5000/api/v2/users").json())

print(requests.get("http://localhost:5000/api/v2/users/1").json())

print(requests.get("http://localhost:5000/api/v2/users/-1"))

print(requests.post("http://localhost:5000/api/v2/users",
                    json={
                        "surname": "test_surname",
                        "name": "test_name",
                        "age": "qwe",
                        "position": "position0",
                        "speciality": "no",
                        "address": "no",
                        "email": "qwe@qwe.com"
                    }
                    ))

print(requests.post("http://localhost:5000/api/v2/users",
                    json={
                        "surname": "test_surname",
                        "name": "test_name",
                        "position": "position0",
                        "speciality": "no",
                        "address": "no",
                        "email": "qwe@qwe.com"
                    }
                    ))

print(requests.post("http://localhost:5000/api/v2/users",
                    json={
                        "surname": "test_surname",
                        "name": "test_name",
                        "age": 100,
                        "position": "position0",
                        "speciality": "no",
                        "address": "no",
                        "email": "qwe@qwe.com",
                        "password": "123"
                    }
                    ))

print(requests.get("http://localhost:5000/api/v2/users").json())

print(requests.delete("http://localhost:5000/api/v2/users/999").json())

print(requests.delete("http://localhost:5000/api/v2/users/6").json())

print(requests.get("http://localhost:5000/api/v2/users").json())
