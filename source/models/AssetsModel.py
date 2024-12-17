from .BaseDataModel import BaseDataModel
from .db_schemes import Assets
from .enums.DBEnum import DBEnum
from bson import ObjectId

class AssetModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DBEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DBEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DBEnum.COLLECTION_ASSET_NAME.value]
            indexes = Assets.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Assets):

        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id

        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):

        records = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type": asset_type,
        }).to_list(length=None)

        return [
            Assets(**record)
            for record in records
        ]

    async def get_asset_record(self, asset_project_id: str, asset_name: str):

        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if ObjectId.is_valid(asset_project_id) else asset_project_id,
            "asset_name": asset_name,
        })

        if record:
            return Assets(**record)
        
        return None


    