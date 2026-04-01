from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from products_api.core.database import get_session
from products_api.models.products import Product
from products_api.schemas.products import (
    ProductListResponseSchema,
    ProductResponseSchema,
    ProductSchema,
    ProductUpdateSchema,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponseSchema,
    summary='Criar um novo produto',
)
async def create_product(
    product: ProductSchema,
    db: AsyncSession = Depends(get_session)
):

    name_exists = await db.scalar(
        select(exists().where(Product.name == product.name))
    )

    if name_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome do Produto já existe",
        )

    db_product = Product(
        name=product.name,
        price=product.price,
        description=product.description,
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=ProductListResponseSchema,
    summary='Listar todos os produtos',
)
async def list_products(
    db: AsyncSession = Depends(get_session)
):
    results = await db.execute(select(Product))
    products = results.scalars().all()

    return {
        "products": products,
    }


# Buscar 1 produto
@router.get(
    path='/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchema,
    summary='Buscar um produto',
)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_session),
):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    return product


# Atualizar produto
@router.put(
    path='/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchema,
    summary='Atualizar um produto',
)
async def update_product(
    product_id: int,
    product_update: ProductUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    update_data = product_update.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != product.name:
        name_exists = await db.scalar(
            select(exists().where(
                Product.name == update_data["name"])
                & (Product.id != product_id)
            )
        )

        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome do Produto já existe",
            )

    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


# Deletar produto
@router.delete(
    path='/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar um produto',
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_session),
):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    await db.delete(product)
    await db.commit()

    return {
        "message": "Produto deletado com sucesso",
    }
