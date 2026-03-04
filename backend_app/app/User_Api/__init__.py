from .user_login import blp as UserLoginBlueprint
from .fetch_product import blp as FetchProductBlueprint
from .product_detail import blp as SpecificProductDetailBlueprint
from .user_add_to_cart import blp as AddToCartBlueprint
from .logout import blp as UserLogoutBlueprint
from .total_item_in_cart import blp as TotalItemBlueprint
from .customised_tshirt_checkout import blp as CustomisedTshirtBlueprint
from .check_out import blp as CheckOutBlueprint
from .user_profile import blp as UserProfileBlueprint
from .edit_profile import blp as EditProfileBlueprint
from .fetch_item_in_cart import blp as FetchItemInCartBlueprint
from .remove_item_add_in_cart import blp as RemoveItemAddToCartBlueprint


def register_user_blueprint(app_api):
    app_api.register_blueprint(UserLoginBlueprint)
    app_api.register_blueprint(FetchProductBlueprint)
    app_api.register_blueprint(SpecificProductDetailBlueprint)
    app_api.register_blueprint(AddToCartBlueprint)
    app_api.register_blueprint(UserLogoutBlueprint)
    app_api.register_blueprint(TotalItemBlueprint)
    app_api.register_blueprint(CustomisedTshirtBlueprint)
    app_api.register_blueprint(CheckOutBlueprint)
    app_api.register_blueprint(UserProfileBlueprint)
    app_api.register_blueprint(EditProfileBlueprint)
    app_api.register_blueprint(FetchItemInCartBlueprint)
    app_api.register_blueprint(RemoveItemAddToCartBlueprint)
