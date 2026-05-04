import pytest
from product import Product


@pytest.fixture
def product():
    return Product("Laptop", 2999.99, 10)


def test_is_available(product):
    assert product.is_available() == True

def test_is_not_available_when_empty():
    empty = Product("Brak", 9.99, 0)
    assert empty.is_available() == False

def test_is_not_available_after_removing_all(product):
    product.remove_stock(10)
    assert product.is_available() == False


@pytest.mark.parametrize("amount, expected_quantity", [
    (0,  10),
    (1,  11),
    (5,  15),
    (90, 100),
])
def test_add_stock_parametrized(product, amount, expected_quantity):
    product.add_stock(amount)
    assert product.quantity == expected_quantity


@pytest.mark.parametrize("bad_amount", [-1, -10, -999])
def test_add_stock_negative_raises(product, bad_amount):
    with pytest.raises(ValueError):
        product.add_stock(bad_amount)


@pytest.mark.parametrize("amount, expected_quantity", [
    (1,  9),
    (5,  5),
    (10, 0),
])
def test_remove_stock_parametrized(product, amount, expected_quantity):
    product.remove_stock(amount)
    assert product.quantity == expected_quantity

def test_remove_stock_too_much_raises(product):
    with pytest.raises(ValueError):
        product.remove_stock(11)

@pytest.mark.parametrize("bad_amount", [-1, -10])
def test_remove_stock_negative_raises(product, bad_amount):
    with pytest.raises(ValueError):
        product.remove_stock(bad_amount)


def test_total_value(product):
    assert product.total_value() == pytest.approx(29999.90, rel=1e-3)

def test_total_value_zero_quantity():
    empty = Product("Brak", 50.0, 0)
    assert empty.total_value() == 0.0


def test_negative_price_raises():
    with pytest.raises(ValueError):
        Product("Zły", -1.0, 5)

def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        Product("Zły", 10.0, -3)
