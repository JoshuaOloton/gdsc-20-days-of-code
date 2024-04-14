from api import db, bcrypt


class Permission:
    REGULAR_ACCESS = 1
    ADMIN_ACCESS = 2


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Administrator': [Permission.REGULAR_ACCESS, Permission.ADMIN_ACCESS],
            'User': [Permission.REGULAR_ACCESS],
        }
        for role, perms in roles.items():
            r = Role.query.filter_by(name=role).first()
            if r is None:
                r = Role(name=role)
            r.reset_permissions()
            for perm in perms:
                r.add_permission(perm)
            db.session.add(r)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def can(self, permission):
        role = Role.query.get(self.role_id)
        return role is not None and role.has_permission(permission)

    def to_dict(self):
        role = Role.query.get(self.role_id)
        return {
            'id': self.id,
            'name': self.name,
            'role': role.name
        }
    
    def __repr__(self) -> str:
        return f'<User {self.id} -> {self.name}>'


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_published = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'date_published': self.date_published,
            'price': self.price,
            'in_stock': self.in_stock
        }

    def __repr__(self) -> str:
        return f'<Book {self.id} -> {self.name}>'
