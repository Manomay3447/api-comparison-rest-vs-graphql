import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from flask import Flask, request, jsonify
import graphene
from backend.data import users

# Define nested GraphQL types
class AddressType(graphene.ObjectType):
    street = graphene.String()
    city = graphene.String()
    zipcode = graphene.String()

class CompanyType(graphene.ObjectType):
    name = graphene.String()
    department = graphene.String()

class UserType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    address = graphene.Field(AddressType)
    company = graphene.Field(CompanyType)

# Root Query
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(root, info):
        return users

    def resolve_user(root, info, id):
        return next((u for u in users if u['id'] == id), None)

schema = graphene.Schema(query=Query)

# Flask app setup
app = Flask(__name__)

@app.route("/graphql", methods=["GET", "POST"])
def graphql_server():
    if request.method == "GET":
        return '''
            <!DOCTYPE html>
            <html>
            <head><title>GraphQL Playground</title></head>
            <body>
                <h2>GraphQL Query Tester</h2>
                <form method="POST" action="/graphql">
                    <textarea name="query" rows="10" cols="80">
{ users { id name email address { city } company { name department } } }
                    </textarea><br><br>
                    <button type="submit">Run Query</button>
                </form>
            </body>
            </html>
        '''

    if request.content_type == "application/json":
        data = request.get_json()
    else:
        data = {"query": request.form.get("query")}

    result = schema.execute(data.get("query"))

    if result.errors:
        return jsonify({"errors": [str(e) for e in result.errors]})

    return jsonify({"data": result.data})

if __name__ == "__main__":
    app.run(port=5002)

