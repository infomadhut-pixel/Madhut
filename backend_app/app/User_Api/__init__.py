from .user_login import blp as UserLoginBlueprint
from .fetch_product import blp as FetchProductBlueprint
from .product_detail import blp as SpecificProductDetailBlueprint
from .user_add_to_cart import blp as AddToCartBlueprint
from .logout import blp as UserLogoutBlueprint
from .total_item_in_cart import blp as TotalItemBlueprint
from .customised_tshirt_checkout import blp as CustomisedTshirtBlueprint


def register_user_blueprint(app_api):
    app_api.register_blueprint(UserLoginBlueprint)
    app_api.register_blueprint(FetchProductBlueprint)
    app_api.register_blueprint(SpecificProductDetailBlueprint)
    app_api.register_blueprint(AddToCartBlueprint)
    app_api.register_blueprint(UserLogoutBlueprint)
    app_api.register_blueprint(TotalItemBlueprint)
    app_api.register_blueprint(CustomisedTshirtBlueprint)
