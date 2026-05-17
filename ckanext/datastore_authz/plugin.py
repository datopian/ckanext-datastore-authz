import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckanext.datastore_authz.logic.action import datastore_authorize


class DatastoreAuthzPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "datastore_authz")

    # IActions
    def get_actions(self):
        return {"datastore_authorize": datastore_authorize}
