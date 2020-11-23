"""
--> Models.py: CONTAINS CLASSES THAT REPRESENTS OBJECTS IN THE DATABASE  < --

makemigrations: generates the sql code
migrate: executes the generated sql code
auto_now=True: changes whenever the 'save/update' button is pressed. Used for update
auto_now_add=True: saves the initial date&time the object is created in the database. Used for created/date_created

One-To-Many: uses a 'ForeignKey'
Many-To-Many: uses an 'intermediate model'. In 'admin.py', create an inline class for the intermediate model,
to edit the intermediate model on the same page as a parent model 

This is the behaviour to adopt when the referenced object is deleted. It is not specific to Django; 
this is an SQL standard. Although Django has its own implementation on top of SQL. (1)

There are seven possible actions to take when such event occurs:

CASCADE: When the referenced object is deleted, also delete the objects that have references to it (when you remove 
a blog post for instance, you might want to delete comments as well). SQL equivalent: CASCADE.
PROTECT: Forbid the deletion of the referenced object. To delete it you will have to delete all objects that 
reference it manually. SQL equivalent: RESTRICT.
RESTRICT: (introduced in Django 3.1) Similar behavior as PROTECT that matches SQL's RESTRICT more accurately. 
SET_NULL: Set the reference to NULL (requires the field to be nullable). For instance, when you delete a User, 
you might want to keep the comments he posted on blog posts, but say it was posted by an anonymous (or deleted) user. 
SQL equivalent: SET NULL.
SET_DEFAULT: Set the default value. SQL equivalent: SET DEFAULT.
SET(...): Set a given value. This one is not part of the SQL standard and is entirely handled by Django.
DO_NOTHING: Probably a very bad idea since this would create integrity issues in your database (referencing an object 
that actually doesn't exist). SQL equivalent: NO ACTION.

Example:
class ParentModel(models.Model):
    name = models.CharField(max_length=20, null=True)
    
class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, null=True)
    
parent = ParentModel.objects.first()
parent.childmodel_set.all()/parent.related_name.all()/

- Template tags({% tag %}): controls the rendering of the template.
- Template variables ({{ variable }}): get replaced with values when the template is rendered.
• Template filters({{
variable|filter }}): allow you to modify variables for display.
"""
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    # OneToOneField: a user can have one customer and one customer can have one user
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)  # must specify the default max_length
    phone = models.CharField(max_length=11, null=True)
    email = models.EmailField(null=True)
    # with default picture for every user
    profile_picture = models.ImageField(null=True, blank=True, default="profile-picture.png")
    # saves the first time&date the object was created in the DB
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)


class Tag(models.Model):
    name = models.CharField(max_length=20, null=True)  # must specify the default max_length

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=200, null=True)
    # DecimalField(): requires 'max_digits' and 'decimal_places'by default
    # max_digits(10) & decimal_places(2) =10000000.00
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    # when using 'on_delete=models.SET_NULL', 'null=True' must also be set to True
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=25, null=True, choices=STATUS, default='Pending')
    note = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.product.name
