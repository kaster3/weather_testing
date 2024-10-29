from utils import case_convector, pluralize


def test_case_convector():
    assert case_convector.camel_case_to_snake_case("HelloWorld") == "hello_world"
    assert case_convector.camel_case_to_snake_case("HelloWorldTest") == "hello_world_test"
    assert case_convector.camel_case_to_snake_case("HelloWorldTest123") == "hello_world_test123"
    assert (
        case_convector.camel_case_to_snake_case("HelloWorldTest123_Test")
        == "hello_world_test123_test"
    )
    assert (
        case_convector.camel_case_to_snake_case("HelloWorldTest123_Test_Test")
        == "hello_world_test123_test_test"
    )


def test_pluralize():
    assert pluralize("car") == "cars"
    assert pluralize("cat") == "cats"
    assert pluralize("category") == "categories"
    assert pluralize("city") == "cities"
    assert pluralize("bus") == "buses"
