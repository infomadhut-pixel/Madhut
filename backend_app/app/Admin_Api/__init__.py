from .product import product_bp as ProductBlueprint
from .view_all_product import blp as ViewAllProductBlueprint
from .get_single_product import blp as ViewProductDetailBlueprint
from .edit_product import blp as EditProductDetailBlueprint
from .delete_product import blp as DeleteProductBlueprint
from .review import blp as CheckReviewBlueprint
from .delete_review import blp as DeleteReviewBlueprint
from .get_all_order import blp as GetAllOrderBlueprint
from .admin_update_order_status import blp as UpdateOrderStatusBlueprint
from .update_tracking_id import blp as UpdateTrackingIdBlueprint
from .all_user import blp as AdminSeenAllUserBlueprint
from .update_user_status import blp as UserStatusUpdateBlueprint


def register_admin_blueprint(app_api):
    app_api.register_blueprint(ProductBlueprint)
    app_api.register_blueprint(ViewAllProductBlueprint)
    app_api.register_blueprint(ViewProductDetailBlueprint)
    app_api.register_blueprint(EditProductDetailBlueprint)
    app_api.register_blueprint(DeleteProductBlueprint)
    app_api.register_blueprint(CheckReviewBlueprint)
    app_api.register_blueprint(DeleteReviewBlueprint)
    app_api.register_blueprint(GetAllOrderBlueprint)
    app_api.register_blueprint(UpdateOrderStatusBlueprint)
    app_api.register_blueprint(UpdateTrackingIdBlueprint)
    app_api.register_blueprint(AdminSeenAllUserBlueprint)
    app_api.register_blueprint(UserStatusUpdateBlueprint)
