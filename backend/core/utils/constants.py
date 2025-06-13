# Types de fichiers autorisés
ALLOWED_FILE_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'text/csv',
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/zip',
    'application/x-rar-compressed',
]

# Extensions autorisées
ALLOWED_EXTENSIONS = [
    '.pdf', '.doc', '.docx', '.txt', '.csv',
    '.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar'
]

# Tailles maximales
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_TOTAL_SIZE_PER_USER = 500 * 1024 * 1024  # 500MB

# Statuts de documents
DOCUMENT_STATUS_CHOICES = [
    ('DRAFT', 'Brouillon'),
    ('PUBLISHED', 'Publié'),
    ('ARCHIVED', 'Archivé'),
    ('DELETED', 'Supprimé'),
]

# Niveaux de permissions
PERMISSION_LEVELS = [
    ('READ', 'Lecture'),
    ('WRITE', 'Écriture'),
    ('ADMIN', 'Administration'),
]

# Codes d'erreur personnalisés
ERROR_CODES = {
    'FILE_TOO_LARGE': 'FILE_001',
    'INVALID_FILE_TYPE': 'FILE_002',
    'FILE_NOT_FOUND': 'FILE_003',
    'PERMISSION_DENIED': 'AUTH_001',
    'INVALID_CREDENTIALS': 'AUTH_002',
    'ACCOUNT_DISABLED': 'AUTH_003',
}

# Messages d'erreur
ERROR_MESSAGES = {
    'FILE_TOO_LARGE': 'Le fichier est trop volumineux.',
    'INVALID_FILE_TYPE': 'Type de fichier non autorisé.',
    'FILE_NOT_FOUND': 'Fichier introuvable.',
    'PERMISSION_DENIED': 'Permissions insuffisantes.',
    'INVALID_CREDENTIALS': 'Identifiants invalides.',
    'ACCOUNT_DISABLED': 'Compte désactivé.',
}