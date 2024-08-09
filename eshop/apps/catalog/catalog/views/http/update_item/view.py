from typing import Annotated

import fastapi
from fastapi import Depends, Response, status

from pydantic.types import PositiveFloat, PositiveInt

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as lib_Session

from catalog import hints
from catalog.api_router import api_router
from catalog.infrastructure.persistance.postgres.models import CatalogItemORM

from catalog_cqrs_contract.event import CatalogItemPriceChangedEvent

from eshop.dependency_container import dependency_container

from framework.common.dto import DTO
from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.fastapi.dependencies.admin_required import admin_required
from framework.fastapi.http_exceptions import BadRequestException
from framework.file_storage import UploadFile
from framework.sqlalchemy.session import Session

__all__ = ('update_item', )


class CatalogItemRequestData(DTO):
    id: hints.CatalogItemId
    name: str
    description: str
    price: PositiveFloat
    catalog_type_id: hints.CatalogTypeId
    catalog_brand_id: hints.CatalogBrandId
    available_stock: PositiveInt
    restock_threshold: PositiveInt
    maxstock_threshold: PositiveInt
    on_reorder: bool


class NotFoundError(Exception):
    pass


class CatalogItemPriceAndPictureFilenameResult(DTO):
    price: PositiveFloat
    picture_filename: str


def _fetch_catalog_item_price_and_picture_filename(
    catalog_item_id: hints.CatalogItemId,
) -> CatalogItemPriceAndPictureFilenameResult:
    # yapf: disable
    stmt = select(
        CatalogItemORM.price,
        CatalogItemORM.picture_filename,
    ).where(
        CatalogItemORM.id == catalog_item_id,
    )
    # yapf: enable

    with Session() as session:
        with session.begin():
            result = session.execute(stmt).fetchone()

    if not result:
        raise NotFoundError('catalog item with id = %s does not exist', catalog_item_id)

    price, picture_filename = result
    return CatalogItemPriceAndPictureFilenameResult(price=price, picture_filename=picture_filename)


def _update_catalog_item_in_db(session: lib_Session, catalog_item: CatalogItemORM) -> None:
    # yapf: disable
    stmt = update(
        CatalogItemORM,
    ).where(
        CatalogItemORM.id == catalog_item.id,
    ).values(
        name=catalog_item.name,
        description=catalog_item.description,
        price=catalog_item.price,
        picture_filename=catalog_item.picture_filename,
        picture_url=catalog_item.picture_url,
        catalog_type_id=catalog_item.catalog_type_id,
        catalog_brand_id=catalog_item.catalog_brand_id,
        available_stock=catalog_item.available_stock,
        restock_threshold=catalog_item.restock_threshold,
        maxstock_threshold=catalog_item.maxstock_threshold,
        on_reorder=catalog_item.on_reorder,
    )
    # yapf: enable

    session.execute(stmt)


def _updated_catalog_item(
    catalog_item_request_data: CatalogItemRequestData,
    picture_filename: str,
    picture_url: str,
) -> CatalogItemORM:
    return CatalogItemORM(
        id=catalog_item_request_data.id,
        name=catalog_item_request_data.name,
        description=catalog_item_request_data.description,
        price=catalog_item_request_data.price,
        picture_filename=picture_filename,
        picture_url=picture_url,
        catalog_type_id=catalog_item_request_data.catalog_type_id,
        catalog_brand_id=catalog_item_request_data.catalog_brand_id,
        available_stock=catalog_item_request_data.available_stock,
        restock_threshold=catalog_item_request_data.restock_threshold,
        maxstock_threshold=catalog_item_request_data.maxstock_threshold,
        on_reorder=catalog_item_request_data.on_reorder,
    )


@api_router.put('/items/', dependencies=[Depends(admin_required)])
def update_item(
    catalog_item_request_data: Annotated[CatalogItemRequestData, Depends()],
    catalog_item_picture: fastapi.UploadFile,
) -> Response:
    try:
        catalog_item_price_and_picture_filename = _fetch_catalog_item_price_and_picture_filename(
            catalog_item_id=catalog_item_request_data.id,
        )
    except NotFoundError:
        raise BadRequestException(detail=f'catalog item with id = {catalog_item_request_data.id} does not exist')

    current_catalog_item_price = catalog_item_price_and_picture_filename.price
    current_catalog_item_picture_filename = catalog_item_price_and_picture_filename.picture_filename

    file_storage_api = dependency_container.file_storage_api_factory()

    picture_url = file_storage_api.url_path_for_file(filename=catalog_item_picture.filename)

    updated_catalog_item = _updated_catalog_item(
        catalog_item_request_data=catalog_item_request_data,
        picture_filename=catalog_item_picture.filename,
        picture_url=picture_url,
    )

    with Session() as session:
        with session.begin():
            try:
                _update_catalog_item_in_db(
                    session=session,
                    catalog_item=updated_catalog_item,
                )
            except IntegrityError:
                raise BadRequestException(
                    detail=f'''
                    catalog brand with id = {updated_catalog_item.catalog_brand_id}
                    or catalog type with id = {updated_catalog_item.catalog_type_id} does not exist
                    ''',
                )

            if updated_catalog_item.price != current_catalog_item_price:
                CatalogItemPriceChangedEvent(
                    catalog_item_id=updated_catalog_item.id,
                    old_price=current_catalog_item_price,
                    new_price=updated_catalog_item.price,
                    context=InsideSqlachemyTransactionContext(session=session),
                ).publish()

    file_storage_api.update(
        old_file_filename=current_catalog_item_picture_filename,
        upload_file=UploadFile(file=catalog_item_picture.file, filename=catalog_item_picture.filename),
        does_not_exist_ok=False,
    )

    return Response(status_code=status.HTTP_200_OK)
