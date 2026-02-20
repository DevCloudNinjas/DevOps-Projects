# import django
# django.setup()
# from apps.node_api.models import Category

# def test_second_create_category():
#     category = Category.objects.create(name="Vegetables8")
#     assert category.name == "Vegetables8"
    
# def test_filter_category():
#     Category.objects.create(name="Book1")
#     assert Category.objects.filter(name="Book1").exists()

# def test_update_category():
#     category = Category.objects.create(name="Boo3")
#     category.name = "DVDs"
#     category.save()
#     category_from_db = Category.objects.get(name="DVDs")
#     assert category_from_db.name == "DVDs"    