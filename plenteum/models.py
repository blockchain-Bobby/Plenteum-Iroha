from wallet import plenteumAddress
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, Column, Boolean, BigInteger ,Integer, String, ForeignKey, Date, DateTime 
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, BIGINT, JSON
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    ple_pub_key = Column(String(100), unique = True, nullable=False)
    asset_owner_key = Column(String(100), unique = True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_asset_owner_key(self, password):
        self.password_hash = generate_password_hash(password)

class Products(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String(100), unique=True, nullable=False)
    network = Column(String(100), unique=True, nullable=False)
    sellvalue = Column(Float(4, asdecimal=True))
    costprice = Column(Float(4, asdecimal=True))
    
class Assets(db.Model):
    __tablename__ = 'blockchain_assets'
    id = Column(Integer, primary_key=True,nullable=False)
    bc_loc_address = Column(String(100), unique = True, nullable=False)
    bc_owner_id = Column(String(100), unique=True, nullable=False)

class Quotations(db.Model):
    __tablename__ = 'qoutes'
    id = Column(Integer, primary_key=True, nullable=False)
    serviceWallet = Column(String(100),default=plenteumAddress(), nullable=False)
    paymentId = Column(String(30), nullable=False)
    recepients = Column(JSON)
    orderDetails = Column(JSON)
    qouteTotal = Column(Integer, nullable=False)
    valid = Column(Boolean, default=True)
    start_block_no = Column(Integer,nullabe=False)
    end_block_no = Column(Integer,nullabe=False)
    ple_payment_total = Column(Integer, nullable=False)

class ContactList(db.Model):
    __tablename__ = 'contactList'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False)
    details = Column(String(30), nullable=False)
    provider = Column(String(30), nullable=False)
