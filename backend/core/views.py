from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import firestore

# Initializing the Firestore client
db = firestore.client()


class AssetList(APIView):
    def get(self, request):
        # Getting all assets from Firestore
        assets_ref = db.collection('assets')
        assets = assets_ref.stream()

        asset_list = []
        for asset in assets:
            asset_list.append(asset.to_dict())

        return Response(asset_list)

    def post(self, request):
        # Adding a new asset to Firestore
        asset_data = request.data
        db.collection('assets').add(asset_data)

        return Response({"message": "Asset added successfully!"})
