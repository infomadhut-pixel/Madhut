from .product import product_bp as ProductBlueprint


def register_admin_blueprint(app_api):
    app_api.register_blueprint(ProductBlueprint)