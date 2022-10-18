# random
import random

# Pillow
from PIL import Image 

# aleph
from aleph_client.chains.ethereum import ETHAccount
from aleph_client.asynchronous import get_posts, create_store, get_messages

# fastAPI
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello my World"}

@app.get("/v1/{id}.json")
async def get_metadata(id: int):
    posts = await get_posts(
        hashes=['d900923c103897dfc4f46e5413e026d71fdfb8fcca14dab656895ba0ba6fc971']
    )
    nfts = posts['posts'][0]['content']
    return nfts[id - 1]

# 970c8dcec3c6279c6d3159a6aa908b3dd71345d68d5681f9a9b61e8bdc6b9b2b

# https://github.com/aleph-im/aleph-client/tree/master/src/aleph_client
@app.get("/nfts/{id}.json")
async def get_or_generate_nft(id: int):

    lists = [
        r"../images/1.png",
        r"../images/2.png",
        r"../images/3.png",
        r"../images/4.png",
        r"../images/5.png",
        r"../images/6.png",
        r"../images/7.png",
        r"../images/8.png",
        r"../images/9.png",
        r"../images/10.png",
    ]

    random_img = random.choices(lists, weights=(10, 10, 10, 10, 10, 10, 10, 10, 10, 10))[0]

    selected_img = Image.open(random_img)

    selected_img.save('nft.png')

    account = ETHAccount('8033d0bfdca6399aab7d26e67cf4fa67e2150307702f54571907c5447339bbad')
    address = account.get_address()

    response = await get_messages(
        addresses=[address],
        refs=[f'nft-{id}'],
        message_type=["STORE"]
    )
    
    len_response = len(response.messages)
    print("len_response>>>>", len_response)

    # if len_response > 0 :
    if len(response.message) > 0 :
        result = response.messages[0]
    else:
        file = open(r"./nft.png", "rb").read()
        result = await create_store(
            file_content=file,
            account=account,
            storage_engine="ipfs",
            extra_fields={
                "name": f'Random NFT #{id}',
                "description": "TODO: Project description coming soon.... "
            },
            ref=f'nft-{id}'
        )

    print("result>>>", result)
    # # print("result", result) # 전체 정보
    # # return {"data": result.content.item_hash}

    return {
        "image": f'https://ipfs.io/ipfs/{result.content.item_hash}',
        "name": f'{result.content.name}',
        "description": f'{result.content.description}',
        "address": account.get_address()
    }

