import os
import mimetypes
import hashlib
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound

class Assets:
    def __init__(self, app=None):
        self._bundles = {}
        self._processors = {}
        self._manifest = {}
        self._cache_busting = False
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        app.assets = self

    def serve_static(self, filename):
        static_path = os.path.join(self.app.static_folder, filename)
        if os.path.isfile(static_path):
            mimetype, _ = mimetypes.guess_type(static_path)
            if mimetype:
                return Response(open(static_path, 'rb').read(), mimetype=mimetype)
        raise NotFound()

    def url_for_static(self, filename):
        return f'/static/{filename}'

    def register_bundle(self, name, *assets):
        self._bundles[name] = assets

    def get_bundle_urls(self, name):
        urls = []
        assets = self._bundles.get(name, [])
        for asset in assets:
            urls.append(self.url_for_static(asset))
        return urls

    def generate_bundle_hash(self, name):
        assets = self._bundles.get(name, [])
        hash_content = ''.join(open(os.path.join(self.app.static_folder, asset), 'rb').read() for asset in assets)
        return hashlib.md5(hash_content.encode('utf-8')).hexdigest()

    def url_for_bundle(self, name):
        hash_value = self.generate_bundle_hash(name)
        return f'/static/bundles/{name}_{hash_value}.bundle'

    def add_processor(self, file_extension, processor):
        self._processors[file_extension] = processor

    def process_asset(self, asset):
        extension = os.path.splitext(asset)[1]
        processor = self._processors.get(extension)
        if processor:
            return processor(asset)
        return asset

    def url_for_processed(self, asset):
        processed_asset = self.process_asset(asset)
        return self.url_for_static(processed_asset)

    def enable_cache_busting(self):
        self._cache_busting = True

    def add_manifest_entry(self, original_path, hashed_path):
        self._manifest[original_path] = hashed_path

    def url_for_manifest(self, original_path):
        if self._cache_busting:
            hashed_path = self._manifest.get(original_path)
            if hashed_path:
                return self.url_for_static(hashed_path)
        return self.url_for_static(original_path)
