"""
factory_boy model factories for generating test objects.

Docs: https://factoryboy.readthedocs.io/en/stable/

Rules:
    - Define one factory per model — never use Model.objects.create() directly in tests.
    - Use Sequence for unique fields, Faker for realistic-looking data.
    - Use SubFactory for related objects — do not hardcode foreign keys.
    - Set sensible defaults so a factory can be used with zero arguments.

Example:
    class PostFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Post

        title = factory.Sequence(lambda n: f"Post {n}")
        body = factory.Faker("paragraph")
        author = factory.SubFactory(UserFactory)
        status = PostStatus.PUBLISHED
"""
