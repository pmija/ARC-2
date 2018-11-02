from django.db import models
import datetime

# Create your models here.
class Ref_UserType(models.Model):
	UserTypeID = models.AutoField(primary_key=True)
	UserType = models.CharField(max_length=50, default='')

	def natural_key(self):
		return self.UserType, self.UserTypeID

class Ref_UserStatus(models.Model):
	UserStatusID = models.AutoField(primary_key=True)
	UserStatus = models.CharField(max_length=50)

class Ref_Degree(models.Model):
	DegreeID = models.AutoField(primary_key=True)
	DegreeName = models.CharField(max_length=50)

	def natural_key(self):
		return self.DegreeName

class Ref_Department(models.Model):
	DepartmentID = models.AutoField(primary_key=True)
	DepartmentName = models.CharField(max_length=50)

	def natural_key(self):
		return self.DepartmentName

class Group(models.Model):
	GroupID = models.AutoField(primary_key=True)
	GroupName = models.CharField(max_length=50, default='')
	lab = models.ForeignKey('Ref_Laboratory', on_delete=models.CASCADE,default=0)
	Adviser = models.IntegerField(default=0)
	GroupStatus = models.IntegerField(default=0)
	Members = models.IntegerField(default=0)

	def natural_key(self):
		return self.GroupName

class User(models.Model):
	UserID = models.IntegerField(primary_key=True)
	NFCUniqueID = models.CharField(max_length=250, blank=True, null=True)
	UserType = models.IntegerField(default=0)
	Type = models.ForeignKey('Ref_UserType',on_delete=models.CASCADE,default=0,blank=True, null=True)
	UserStatus = models.IntegerField(default=0)
	Name = models.CharField(max_length=50, default='')
	IDNumber = models.IntegerField(default=0)
	PhoneNumber = models.IntegerField(default=0)
	Email = models.CharField(max_length=50, default='')
	Remarks = models.CharField(max_length=250, default='')
	group = models.ForeignKey('Group', on_delete=models.CASCADE,default=0,blank=True, null=True)
	adviser = models.ForeignKey('User', on_delete=models.CASCADE,default=0,blank=True, null=True)
	Degree = models.ForeignKey('Ref_Degree', on_delete=models.CASCADE,default=0,blank=True, null=True)
	Department = models.ForeignKey('Ref_Department', on_delete=models.CASCADE,default=0,blank=True, null=True)
	Laboratory = models.ForeignKey('Ref_Laboratory',  on_delete=models.CASCADE,default=0,blank=True, null=True)
	def get_id(self):
	    return self.UserID

	def get_UserType(self):
		return self.UserType

	def natural_key(self):
		return self.Name, self.UserID, self.IDNumber

class ActualResidency(models.Model):
	ActualResidencyID = models.AutoField(primary_key=True)
	Student = models.ForeignKey('User',  on_delete=models.CASCADE,default=0,blank=True, null=True)
	DateTime = models.DateField()
	TimeIn = models.TimeField()
	TimeOut = models.TimeField(blank=True, null=True)
	ResidencyStatus = models.IntegerField(blank=True, null=True)

class Ref_Term(models.Model):
	TermID = models.AutoField(primary_key=True)
	Term = models.CharField(max_length=50, default='')
	StartDate = models.DateTimeField(blank=True, null=True)
	StartDate = models.DateTimeField(blank=True, null=True)

class Ref_Laboratory(models.Model):
	LabID = models.AutoField(primary_key=True)
	LaboratoryName = models.CharField(max_length=50, default='')
	RoomNum = models.CharField(max_length=50, default='')
	Capacity = models.IntegerField(default=0)
	Status = models.IntegerField(default=0)

	def get_LaboratoryName(self):
		return self.LaboratoryName

	def get_id(self):
	    return self.LabID

	def natural_key(self):
		return self.LaboratoryName, self.LabID

class Ref_Schedule(models.Model):
	ScheduleID = models.AutoField(primary_key=True)
	Day = models.CharField(max_length=20, default='')
	Time = models.TimeField()

	def natural_key(self):
		return self.Time

		class Meta:
        		ordering = ['Time']

class ResidencyTimeSlot(models.Model):
	ResidencyID = models.AutoField(primary_key=True)
	Laboratory = models.ForeignKey('Ref_Laboratory',  on_delete=models.CASCADE,default=0,blank=True, null=True)
	Schedule = models.CharField(max_length=50, default='')
	TotalSlot = models.IntegerField(default=0)
	TakenSlot = models.IntegerField(default=0)
	SchedVar = models.IntegerField(default=0)

class StudentResidencySchedule(models.Model):
	StudentResSchedID = models.AutoField(primary_key=True)
	RefSchedVar = models.IntegerField(default=0)
	StudentSchedVar = models.IntegerField(default=0)
	Student =  models.CharField(max_length=250,default='')
	Schedule =  models.CharField(max_length=50,default='')

class Ref_AuditAction(models.Model):
	AuditActionID = models.AutoField(primary_key=True)
	Action = models.CharField(max_length=50, default='')

class Inventory(models.Model):
	ItemID = models.AutoField(primary_key=True)
	ItemName = models.CharField(max_length=50, default='')
	Description = models.CharField(max_length=50, default='')
	ItemType = models.CharField(max_length=50, default='')
	Quantity = models.IntegerField(default=0)
	ItemUniqueID = models.CharField(max_length=250, blank=True, null=True)
	QtyBorrowed = models.IntegerField(default=0)
	ItemStatus = models.IntegerField(default=1) 

	def natural_key(self):
		return self.ItemName, self.Description, self.ItemType

class AuditTable_Inventory(models.Model):
	AuditID = models.AutoField(primary_key=True)
	AuditAction = models.IntegerField(default=0)
	ItemID = models.ForeignKey('Inventory',on_delete=models.CASCADE,default=0,blank=True, null=True)
	Quantity = models.IntegerField(blank=True,null=True)
	DateTime = models.DateTimeField()
	DateTimeReturned = models.DateTimeField(blank=True,null=True)
	Borrower = models.ForeignKey('User',on_delete=models.CASCADE,related_name="borrower_users",blank=True, null=True)
	Admin = models.ForeignKey('User',on_delete=models.CASCADE,related_name="admin_users",blank=True, null=True)
	BorrowStatus = models.IntegerField(blank=True, null=True)
	Event = models.IntegerField(blank=True,default=0)
	Remarks = models.CharField(max_length=250,default='')
