from pathlib import Path

from catalog.domain.models import CatalogBrand, CatalogItem, CatalogType

from eshop.dependency_container import dependency_container

from framework.file_storage.ifile_storage_api import UploadFile
from framework.sqlalchemy.session import Session


def create_catalog_items() -> None:
    LOCAL_MEDIA_FOLDER = Path(__file__).parent / 'media'

    file_storage_api = dependency_container.file_storage_api_factory()

    catalog_type1 = CatalogType(type='type1')
    catalog_type2 = CatalogType(type='type2')

    catalog_brand1 = CatalogBrand(brand='brand1')
    catalog_brand2 = CatalogBrand(brand='brand2')

    catalog_item1_picture_filename = 'catalog_item1.jpg'
    with open(LOCAL_MEDIA_FOLDER / catalog_item1_picture_filename, 'rb') as file:
        catalog_item1_url_path_to_file = file_storage_api.upload(
            upload_file=UploadFile(
                file=file,
                filename=catalog_item1_picture_filename,
            ),
        )

    catalog_item2_picture_filename = 'catalog_item2.jpg'
    with open(LOCAL_MEDIA_FOLDER / catalog_item1_picture_filename, 'rb') as file:
        catalog_item2_url_path_to_file = file_storage_api.upload(
            upload_file=UploadFile(
                file=file,
                filename=catalog_item2_picture_filename,
            ),
        )

    catalog_item3_picture_filename = 'catalog_item3.jpg'
    with open(LOCAL_MEDIA_FOLDER / catalog_item1_picture_filename, 'rb') as file:
        catalog_item3_url_path_to_file = file_storage_api.upload(
            upload_file=UploadFile(
                file=file,
                filename=catalog_item3_picture_filename,
            ),
        )

    catalog_item4_picture_filename = 'catalog_item4.jpg'
    with open(LOCAL_MEDIA_FOLDER / catalog_item1_picture_filename, 'rb') as file:
        catalog_item4_url_path_to_file = file_storage_api.upload(
            upload_file=UploadFile(
                file=file,
                filename=catalog_item4_picture_filename,
            ),
        )

    catalog_item1 = CatalogItem(
        name='name1',
        description='description1',
        price=10,
        picture_filename=catalog_item1_picture_filename,
        picture_url=catalog_item1_url_path_to_file,
        catalog_type=catalog_type1,
        catalog_brand=catalog_brand1,
        available_stock=3,
        restock_threshold=10,
        maxstock_threshold=15,
        on_reorder=False,
    )
    catalog_item2 = CatalogItem(
        name='name2',
        description='description2',
        price=20,
        picture_filename=catalog_item2_picture_filename,
        picture_url=catalog_item2_url_path_to_file,
        catalog_type=catalog_type1,
        catalog_brand=catalog_brand2,
        available_stock=5,
        restock_threshold=12,
        maxstock_threshold=18,
        on_reorder=False,
    )
    catalog_item3 = CatalogItem(
        name='name3',
        description='description3',
        price=30,
        picture_filename=catalog_item3_picture_filename,
        picture_url=catalog_item3_url_path_to_file,
        catalog_type=catalog_type2,
        catalog_brand=catalog_brand1,
        available_stock=8,
        restock_threshold=13,
        maxstock_threshold=20,
        on_reorder=False,
    )
    catalog_item4 = CatalogItem(
        name='name4',
        description='description4',
        price=40,
        picture_filename=catalog_item4_picture_filename,
        picture_url=catalog_item4_url_path_to_file,
        catalog_type=catalog_type2,
        catalog_brand=catalog_brand2,
        available_stock=9,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=False,
    )

    with Session() as session:
        with session.begin():
            session.add_all(
                [
                    catalog_brand1,
                    catalog_brand2,
                    catalog_type1,
                    catalog_type2,
                    catalog_item1,
                    catalog_item2,
                    catalog_item3,
                    catalog_item4,
                ],
            )


if __name__ == '__main__':
    create_catalog_items()
