import pymongo
from gridfs import GridFS
from django.conf import settings
from bson import ObjectId
import mimetypes
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GridFSManager:
    _connection = None
    _gridfs = None
    
    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            try:
                cls._connection = pymongo.MongoClient(
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=20000,
                    maxPoolSize=10
                )
                db = cls._connection[settings.DATABASES['default']['NAME']]
                cls._gridfs = GridFS(db)
                logger.info("Connexion MongoDB/GridFS établie")
            except Exception as e:
                logger.error(f"Erreur connexion MongoDB: {e}")
                raise
        return cls._gridfs, cls._connection[settings.DATABASES['default']['NAME']]
    
    def save_file(self, file_obj, document_instance):
        try:
            fs, db = self.get_connection()
            file_obj.seek(0)
            file_content = file_obj.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            # Vérification de déduplication
            from apps.documents.models import Document
            existing_doc = Document.objects.filter(file_hash=file_hash).first()
            if existing_doc and existing_doc != document_instance:
                logger.info(f"Fichier dupliqué détecté: {file_hash}")
                document_instance.gridfs_file_id = existing_doc.gridfs_file_id
                document_instance.file_hash = file_hash
                document_instance.original_filename = file_obj.name
                document_instance.file_type = mimetypes.guess_type(file_obj.name)[0] or 'application/octet-stream'
                document_instance.file_size = len(file_content)
                return existing_doc.gridfs_file_id
            
            metadata = {
                'document_id': str(document_instance.id),
                'owner_id': str(document_instance.owner.id),
                'upload_date': datetime.utcnow(),
                'original_filename': file_obj.name,
                'content_type': mimetypes.guess_type(file_obj.name)[0] or 'application/octet-stream',
                'file_hash': file_hash,
                'file_size': len(file_content)
            }
            
            file_id = fs.put(
                file_content,
                filename=file_obj.name,
                metadata=metadata
            )
            
            # Mise à jour des champs du document
            document_instance.gridfs_file_id = str(file_id)
            document_instance.original_filename = file_obj.name
            document_instance.file_type = metadata['content_type']
            document_instance.file_size = len(file_content)
            document_instance.file_hash = file_hash
            
            logger.info(f"Fichier sauvegardé: {file_id}")
            return str(file_id)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde GridFS: {e}")
            raise
    
    def save_version(self, file_obj, version_instance):
        try:
            fs, db = self.get_connection()
            file_obj.seek(0)
            file_content = file_obj.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            # Vérification de déduplication pour les versions
            from apps.documents.models import DocumentVersion
            existing_version = DocumentVersion.objects.filter(file_hash=file_hash).first()
            if existing_version and existing_version != version_instance:
                version_instance.gridfs_file_id = existing_version.gridfs_file_id
                version_instance.file_hash = file_hash
                version_instance.file_size = len(file_content)
                return existing_version.gridfs_file_id
            
            metadata = {
                'document_id': str(version_instance.document.id),
                'version_number': version_instance.version_number,
                'created_by': str(version_instance.created_by.id),
                'upload_date': datetime.utcnow(),
                'original_filename': file_obj.name,
                'content_type': mimetypes.guess_type(file_obj.name)[0] or 'application/octet-stream',
                'file_hash': file_hash
            }
            
            file_id = fs.put(
                file_content,
                filename=f"{version_instance.document.title}_v{version_instance.version_number}_{file_obj.name}",
                metadata=metadata
            )
            
            version_instance.gridfs_file_id = str(file_id)
            version_instance.file_hash = file_hash
            version_instance.file_size = len(file_content)
            
            return str(file_id)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde version GridFS: {e}")
            raise
    
    def get_file(self, file_id):
        try:
            fs, db = self.get_connection()
            object_id = ObjectId(file_id)
            
            if fs.exists(object_id):
                return fs.get(object_id)
            return None
        except Exception as e:
            logger.error(f"Erreur récupération GridFS: {e}")
            return None
    
    def delete_file(self, file_id, document_instance):
        try:
            from apps.documents.models import Document
            other_docs = Document.objects.filter(
                gridfs_file_id=file_id
            ).exclude(id=document_instance.id)
            
            if other_docs.exists():
                logger.info(f"Fichier partagé, suppression ignorée: {file_id}")
                return
            
            fs, db = self.get_connection()
            object_id = ObjectId(file_id)
            
            if fs.exists(object_id):
                fs.delete(object_id)
                logger.info(f"Fichier GridFS supprimé: {file_id}")
                
        except Exception as e:
            logger.error(f"Erreur suppression GridFS: {e}")
    
    def delete_version(self, file_id, version_instance):
        try:
            from apps.documents.models import DocumentVersion
            other_versions = DocumentVersion.objects.filter(
                gridfs_file_id=file_id
            ).exclude(id=version_instance.id)
            
            if other_versions.exists():
                logger.info(f"Version partagée, suppression ignorée: {file_id}")
                return
            
            fs, db = self.get_connection()
            object_id = ObjectId(file_id)
            
            if fs.exists(object_id):
                fs.delete(object_id)
                logger.info(f"Version GridFS supprimée: {file_id}")
                
        except Exception as e:
            logger.error(f"Erreur suppression version GridFS: {e}")