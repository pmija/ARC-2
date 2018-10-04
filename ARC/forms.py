from django import forms
from .models import Inventory, User

class InventoryForm(forms.Form):
	
	class Meta:
		itemname = forms.CharField()
		description = forms.CharField()
		item_type = forms.CharField()
		quantity = forms.IntegerField()
		uid = forms.IntegerField()
		
class LaboratoryForm(forms.Form):
	
	class Meta:
		labname = forms.CharField()
		roomno = forms.CharField()
		capacity = forms.IntegerField()
		
class TermForm(forms.Form):
	
	class Meta:
		termname = forms.CharField()
		startdate = forms.DateField()
		enddate = forms.DateField()
	
class FacultyRegistrationForm(forms.Form):

	class Meta:
		uniqueid = forms.IntegerField()
		idnum = forms.IntegerField()
		email = forms.CharField()
		first_name = forms.CharField()
		last_name = forms.CharField()
		mobileno = forms.IntegerField()

class StudentRegistrationForm(forms.Form):

	class Meta:
		uniqueid = forms.IntegerField()
		idnum = forms.IntegerField()
		email = forms.CharField()
		first_name = forms.CharField()
		last_name = forms.CharField()
		mobileno = forms.IntegerField()
		adviser = forms.IntegerField()

class AddGroupForm(forms.Form):

	class Meta:
		groupname = forms.CharField()
		laboratory = forms.IntegerField()
		adviser = forms.IntegerField()

class AddAccount(forms.Form):
	class Meta:
		accounttype = forms.IntegerField()
		email = forms.CharField()
