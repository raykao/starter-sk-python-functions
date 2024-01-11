from flask import Flask, request
import requests
import aiohttp
import asyncio
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
async def home():
    market_data_list = [
        {
            "location": "San Francisco",
            "property_type": "retail",
        },
        {
            "location": "Downtown Toronto",
            "property_type": "commercial",
        }
    ]

    results = []

    async with aiohttp.ClientSession() as session:
        for market in market_data_list:

            market_data = await session.post('http://localhost:7071/api/generate_market_research', json = {
                'location': market['location'],
                'property_type': market['property_type']
            })

            market_data_text = await market_data.text()

            page_content = await session.post('http://localhost:7071/api/generate_landing_page_content', json = {
                'location': market['location'],
                'property_type': market['property_type'],
                'market_data': market_data_text
            })

            page_content_json = await page_content.json()

            metadata = await session.post('http://localhost:7071/api/extract_keyword_metadata', json = {
                'page_content': page_content_json["content"]
            })

            metadata_json = await metadata.json()
            
            results.append({
            'location': market['location'],
            'property_type': market['property_type'],
            'market_data': market_data_text,
            'landing_page_content': page_content_json["content"],
            'meta_data': metadata_json
        })

    return results

if __name__ == '__main__':
    app.run(port=8081)