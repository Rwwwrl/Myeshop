from catalog.infrastructure.persistance.postgres.models import CatalogBrandORM, CatalogItemORM, CatalogTypeORM

from framework.sqlalchemy.session import Session


def create_catalog_items() -> None:

    catalog_type1 = CatalogTypeORM(id=1, type='type1')
    catalog_type2 = CatalogTypeORM(id=2, type='type2')

    catalog_brand1 = CatalogBrandORM(id=1, brand='brand1')
    catalog_brand2 = CatalogBrandORM(id=2, brand='brand2')

    catalog_item1 = CatalogItemORM(
        id=1,
        name='name1',
        description='description1',
        price=10,
        picture_filename='filename1',
        picture_url='root/filename1',
        catalog_type=catalog_type1,
        catalog_brand=catalog_brand1,
        available_stock=3,
        restock_threshold=10,
        maxstock_threshold=15,
        on_reorder=False,
    )
    catalog_item2 = CatalogItemORM(
        id=2,
        name='name2',
        description='description2',
        price=20,
        picture_filename='filename2',
        picture_url='root/filename2',
        catalog_type=catalog_type1,
        catalog_brand=catalog_brand2,
        available_stock=5,
        restock_threshold=12,
        maxstock_threshold=18,
        on_reorder=False,
    )
    catalog_item3 = CatalogItemORM(
        id=3,
        name='name3',
        description='description3',
        price=30,
        picture_filename='filename3',
        picture_url='root/filename3',
        catalog_type=catalog_type2,
        catalog_brand=catalog_brand1,
        available_stock=8,
        restock_threshold=13,
        maxstock_threshold=20,
        on_reorder=False,
    )
    catalog_item4 = CatalogItemORM(
        id=4,
        name='name4',
        description='description4',
        price=40,
        picture_filename='filename4',
        picture_url='root/filename4',
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
