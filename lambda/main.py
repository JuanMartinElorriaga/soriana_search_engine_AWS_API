from mangum import Mangum
import typesense
from fastapi import FastAPI

app = FastAPI(title='Soriana API',
              description='Search Engine for indexed products')

@app.get("/")
async def get_query(q: str = '66d8a2da01820de6f94f4469ddb2b4c2', query_by: str = 'Uniq Id'):
    client = typesense.Client({
    'nodes': [{
    'host': 'axb2vlh0spjudi31p-1.a1.typesense.net',  # For Typesense Cloud use xxx.a1.typesense.net
    'port': '443',       # For Typesense Cloud use 443
    'protocol': 'https'    # For Typesense Cloud use https
  }],
  'api_key': "sMNt7z17EIJrJJx0NOet7QidOLJaa22K"
  #'connection_timeout_seconds': 2
})
    return client.collections['products'].documents.search({
    'q': q,
    'query_by': query_by
})

handler = Mangum(app=app)