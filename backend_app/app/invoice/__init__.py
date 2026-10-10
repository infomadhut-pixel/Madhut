from .invoice_generator import blp as InvoiceGeneratorBlueprint
def user_invoice_blueprint(app_api):
    app_api.register_blueprint(InvoiceGeneratorBlueprint)