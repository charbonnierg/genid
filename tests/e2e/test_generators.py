from genid.generators import ConstantIDGenerator


def test_constant_id_generator() -> None:
    generator = ConstantIDGenerator("test")
    for _ in range(10):
        new_id = generator.new()
        assert new_id == "test"
