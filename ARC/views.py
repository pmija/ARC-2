from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Max
from itertools import chain
import datetime, time
from datetime import timedelta
from django.shortcuts import redirect
from django.shortcuts import reverse
#Forms
from ARC.forms import FacultyRegistrationForm
from ARC.forms import StudentRegistrationForm
from ARC.forms import AddGroupForm
from ARC.forms import AddAccount
#Models
from ARC.models import Inventory
from ARC.models import Ref_Laboratory
from ARC.models import AuditTable_Inventory
from ARC.models import User
from ARC.models import ActualResidency
from ARC.models import Group
from ARC.models import Ref_UserType
from ARC.models import Ref_Degree
from ARC.models import Ref_Department
from ARC.models import ResidencyTimeSlot
from ARC.models import StudentResidencySchedule

#NFC
import serial
import json
import threading

NFCTag = ""
NFCReady = False

def NFCRead():
	global NFCTag
	global NFCReady

	NFC = serial.Serial('COM3')
	while True:
		temp = ord(NFC.read())
		if temp == 2:
			tag = ""
			tag += str(temp)
			NFCReady = False
		elif temp == 10:
			tag += str(temp)
			NFCTag = tag
			NFCReady = True
			print(tag)
		else:
			tag += str(temp)

threading.Thread(target=NFCRead).start()

RFIDTag = ""
RFIDReady = False

def RFIDRead():
	global RFIDTag
	global RFIDReady

	RFID = serial.Serial('COM4')
	while True:
		temp2 = ord(RFID.read())
		if temp2 == 2:
			tag2 = ""
			tag2 += str(temp2)
			RFIDReady = False
		elif temp2 == 3:
			tag2 += str(temp2)
			RFIDTag = tag2
			RFIDReady = True
			print(tag2)
		else:
			tag2 += str(temp2)

threading.Thread(target=RFIDRead).start()

def NFCAjax(request):
	global NFCTag
	global NFCReady
	JSONVal = {}
	JSONVal['tag'] = NFCTag
	JSONVal['ready'] = NFCReady
	NFCReady = False
	NFCTag = ""
	return HttpResponse(json.dumps(JSONVal))

def RFIDAjax(request):
	global RFIDTag
	global RFIDReady
	JSONVal = {}
	JSONVal['tag'] = RFIDTag
	JSONVal['ready'] = RFIDReady
	RFIDReady = False
	RFIDTag = ""
	return HttpResponse(json.dumps(JSONVal))
#NFC


def ManageItemsAjax(request):

	items = Inventory.objects.all();
	item_serialized = serializers.serialize('json', items)

	return JsonResponse(item_serialized, safe=False)

#########

def ItemDetailsAjax(request):

	if request.method == 'POST': #result is not NULL or NONE but a black value ''

		id = request.POST.get('id', '')
		item = Inventory.objects.filter(ItemID=id)
		dateadded = AuditTable_Inventory.objects.filter(ItemID=id).filter(AuditAction='2')
		last_id = AuditTable_Inventory.objects.filter(ItemID=id).filter(AuditAction='1').aggregate(Max('AuditID'))
		lastborrowed = AuditTable_Inventory.objects.filter(AuditID=last_id.get('AuditID__max'))
		result_list = list(chain(item, dateadded, lastborrowed))
		item_serialized = serializers.serialize('json', result_list)

		return JsonResponse(item_serialized, safe=False)

#########

def ItemLogAjax(request):

	if request.method == 'POST':

		id = request.POST.get('id', '')
		logs = AuditTable_Inventory.objects.filter(ItemID=id)
		item_serialized = serializers.serialize('json', logs, use_natural_foreign_keys=True)

		return JsonResponse(item_serialized, safe=False)

#########

def EditItemAjax(request):

	if request.method == 'POST':

		id = request.POST.get('id', '')
		item = Inventory.objects.filter(ItemID=id)
		item_serialized = serializers.serialize('json', item)

		return JsonResponse(item_serialized, safe=False)
	
#KIM NEW AJAX
def getUserTimeInInfo(request):
	if request.method == 'POST':
		id = request.POST['id']
		student = User.objects.get(NFCUniqueID=id)
		studentInfo = User.objects.all().values_list().filter(NFCUniqueID=id)
		studentLab = studentInfo[0][14]
		residency = ActualResidency.objects.all().values_list().filter(Student=student, ResidencyStatus=1)
		if not residency:	
			timein = datetime.datetime.time(datetime.datetime.now())
			day = datetime.datetime.today().weekday()
			if day == 0:
				schedDay = 'M'
			elif day == 1:
				schedDay = 'T'
			elif day == 2:
				schedDay = 'W'
			elif day == 4:
				schedDay = 'H'
			elif day == 5:
				schedDay = 'F'
				
			
				
			time915 = timein.replace(hour=9, minute=15, second=0, microsecond=0)
			time1100 = timein.replace(hour=11, minute=0, second=0, microsecond=0)
			time1245 = timein.replace(hour=12, minute=45, second=0, microsecond=0)
			time1430 = timein.replace(hour=14, minute=30, second=0, microsecond=0)
			time1615 = timein.replace(hour=16, minute=15, second=0, microsecond=0)
			time1800 = timein.replace(hour=18, minute=0, second=0, microsecond=0)
			time1930 = timein.replace(hour=19, minute=30, second=0, microsecond=0)
			time2100 = timein.replace(hour=21, minute=0, second=0, microsecond=0)
			if timein < time915:
				sched = schedDay + '_07+30-09+00'
				timeout = time915
			elif timein < time1100:
				sched = schedDay + '_09+15-10+45'
				timeout = time1100
			elif timein < time1245:
				sched = schedDay + '_11+00-12+30'
				timeout = time1245
			elif timein < time1430:
				sched = schedDay + '_12+45-14+15'
				timeout = time1430
			elif timein < time1615:
				sched = schedDay + '_14+30-16+00'
				timeout = time1615
			elif timein < time1800:
				sched = schedDay + '_16+15-17+45'
				timeout = time1800
			elif timein < time1930:
				sched = schedDay + '_18+00-19+30'
				timeout = time1930
			elif timein < time2100:
				sched = schedDay + '_19+30-21+00'
				timeout = time2100
			
			studentSched = StudentResidencySchedule.objects.all().values_list().filter(Student=id)
			
			if studentSched:
				dummySched = StudentResidencySchedule.objects.all().values_list().filter(Student=id).latest('RefSchedVar', 'StudentSchedVar')
				max = dummySched[2]
				residencySched = StudentResidencySchedule.objects.all().values_list().filter(Student=id, Schedule=sched, StudentSchedVar=max)
				print(residencySched)
				if residencySched:
					#type1
					actualres = ActualResidency(Student=student, DateTime=datetime.datetime.now(), TimeIn=datetime.datetime.now(), TimeOut=timeout, ResidencyType=1, ResidencyStatus=1,  Schedule=sched)
					actualres.save()
					ares = ActualResidency.objects.all().values_list()
					inv_ares = ares.aggregate(Max('ActualResidencyID'))
					ares2 = ActualResidency.objects.filter(ActualResidencyID=inv_ares['ActualResidencyID__max'])
					res_serialized = serializers.serialize('json', ares2, use_natural_foreign_keys=True)
					return JsonResponse(res_serialized, safe=False)
				else:
					dummyCurrentSched = ResidencyTimeSlot.objects.all().values_list().filter(Laboratory=studentLab).latest('SchedVar')
					maxCurrentSched = dummyCurrentSched[5]
					currentSched = ResidencyTimeSlot.objects.all().values_list().filter(Laboratory=studentLab, Schedule=sched, SchedVar=maxCurrentSched)
					if currentSched:
						#type2
						print(currentSched)
						capacity = currentSched[0][3]
						takenSlot = currentSched[0][4]
						print(capacity, takenSlot)
						if capacity != takenSlot:
							dummyCurrentSched = ResidencyTimeSlot.objects.all().values_list().filter(Laboratory=studentLab).latest('SchedVar')
							maxDummyCurrent = dummyCurrentSched[5]
							print(maxDummyCurrent)
							currentSched = ResidencyTimeSlot.objects.all().values_list().filter(Laboratory=studentLab, SchedVar=maxDummyCurrent, Schedule=sched)
							print(currentSched)
							currentTaken = currentSched[0][4]
							finalTaken = int(currentTaken) + 1
							print(finalTaken)
							ResidencyTimeSlot.objects.filter(Laboratory=studentLab, Schedule=sched, SchedVar=maxDummyCurrent).update(TakenSlot=finalTaken)
						
							actualres = ActualResidency(Student=student, DateTime=datetime.datetime.now(), TimeIn=datetime.datetime.now(), Timeout=datetime.datetime.now(), ResidencyType=2, ResidencyStatus=1,  Schedule=sched)
							actualres.save()
							ares = ActualResidency.objects.all().values_list()
							inv_ares = ares.aggregate(Max('ActualResidencyID'))
							ares2 = ActualResidency.objects.filter(ActualResidencyID=inv_ares['ActualResidencyID__max'])
							res_serialized = serializers.serialize('json', ares2, use_natural_foreign_keys=True)
							return JsonResponse(res_serialized, safe=False)
					else:
						nonexisting = {}
						res_serialized = serializers.serialize('json', nonexisting, use_natural_foreign_keys=True)
						return JsonResponse(res_serialized, safe=False)
		else:
			timeoutActual = ActualResidency.objects.all().values_list().filter(Student=student, ResidencyStatus=1)
			actualSched = timeoutActual[0][3]
			type = timeoutActual[0][5]
			
			if type == 1:
				ActualResidency.objects.filter(Student=student, ResidencyStatus=1).update(TimeOut=datetime.datetime.now(), ResidencyStatus=2)
				actualResidency = ActualResidency.objects.all().values_list()
				agg_residency = actualResidency.aggregate(Max('ActualResidencyID'))
				finalResidency = ActualResidency.objects.filter(ActualResidencyID=agg_residency['ActualResidencyID__max'])
				res_serialized = serializers.serialize('json', finalResidency, use_natural_foreign_keys=True)
				return JsonResponse(res_serialized, safe=False)
			if type == 2:
				dummyActual = ActualResidency.objects.all().values_list().filter(Student=student, ResidencyStatus=1)
				dummyActualSched = dummyActual[0][7]
				
				dummyCurrentSched = ResidencyTimeSlot.objects.all().values_list().filter(Laboratory=studentLab).latest('SchedVar')
				maxDummyCurrent = dummyCurrentSched[5]
				print(maxDummyCurrent)
				currentSched = ResidencyTimeSlot.objects.all().values_list().filter(Laboratory=studentLab, SchedVar=maxDummyCurrent, Schedule=dummyActualSched)
				print(currentSched)
				currentTaken = currentSched[0][4]
				finalTaken = int(currentTaken) - 1
				print(finalTaken)
				ResidencyTimeSlot.objects.filter(Laboratory=studentLab, Schedule=dummyActualSched, SchedVar=maxDummyCurrent).update(TakenSlot=finalTaken)
				
				ActualResidency.objects.filter(Student=student, ResidencyStatus=1).update(TimeOut=datetime.datetime.now(), ResidencyStatus=2)
				actualResidency = ActualResidency.objects.all().values_list()
				agg_residency = actualResidency.aggregate(Max('ActualResidencyID'))
				finalResidency = ActualResidency.objects.filter(ActualResidencyID=agg_residency['ActualResidencyID__max'])
				res_serialized = serializers.serialize('json', finalResidency, use_natural_foreign_keys=True)
				return JsonResponse(res_serialized, safe=False)
				
	
def getBorrowed(request):
	if request.method == 'POST':
		id = request.POST['id']
		inv = Inventory.objects.filter(ItemUniqueID=id)
		inventory = AuditTable_Inventory.objects.all().filter(ItemID=inv[0].pk, BorrowStatus=1)
		item_serialized = serializers.serialize('json', inventory, use_natural_foreign_keys=True)
		return JsonResponse(item_serialized, safe=False)

def returnItem(request):
	if request.method == 'POST':
		id = request.POST['id']
		qty = request.POST['qty']
		type = request.POST['type']
		qtyReturn = request.POST['qtyReturn']
		returnType = request.POST['returnType']
		qytDamage = request.POST['qytDamage']
		rfidtag = request.POST['rfidtag']
		if  returnType == 'complete':
			subtracted =  int(qty) - int(qtyReturn)
			if subtracted == 0:
				AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
				inv = Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag)
				currentBorrow = int(inv[0][6])
				qtyToSubtract = int(qtyReturn)
				finalQtyBorrowRemaining = currentBorrow - qtyToSubtract
				print (finalQtyBorrowRemaining)
				Inventory.objects.filter(ItemUniqueID=rfidtag).update(QtyBorrowed=finalQtyBorrowRemaining)
			else:
				AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
				inventory = AuditTable_Inventory.objects.all().values_list().filter(AuditID=id)
				item_id = Inventory.objects.get(ItemID=inventory[0][2])
				borrower = User.objects.get(UserID=inventory[0][6])
				admin = User.objects.get(UserID=inventory[0][7])
				auditInventory = AuditTable_Inventory(AuditAction=1, ItemID=item_id, Quantity=subtracted, DateTime=inventory[0][4], Borrower=borrower, Admin=admin, BorrowStatus=1)
				auditInventory.save()
				
				AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2, Quantity=qtyReturn)
				inv = Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag)
				currentBorrow = int(inv[0][6])
				qtyToSubtract = int(qtyReturn)
				finalQtyBorrowRemaining = currentBorrow - qtyToSubtract
				print (finalQtyBorrowRemaining)
				Inventory.objects.filter(ItemUniqueID=rfidtag).update(QtyBorrowed=finalQtyBorrowRemaining)
		else:
			print(id, qty, type, qtyReturn, returnType, qytDamage, rfidtag)
			subtracted =  int(qty) - int(qytDamage)
			if subtracted == 0:
				if type == 'big':
					AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
					inv = Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag)
					currentBorrow = int(inv[0][6])
					qtyToSubtract = int(qytDamage)
					finalQtyBorrowRemaining = currentBorrow - qtyToSubtract
					print (finalQtyBorrowRemaining)
					Inventory.objects.filter(ItemUniqueID=rfidtag).update(QtyBorrowed=finalQtyBorrowRemaining)
					Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag).update(ItemStatus = 2)
					
					inventory = AuditTable_Inventory.objects.all().values_list().filter(AuditID=id)
					item_id = Inventory.objects.get(ItemID=inventory[0][2])
					borrower = User.objects.get(UserID=inventory[0][6])
					admin = User.objects.get(UserID=inventory[0][7])
					auditInventory = AuditTable_Inventory(AuditAction=3, ItemID=item_id, Quantity=qytDamage, DateTime=datetime.datetime.now(), Borrower=borrower, Admin=admin)
					auditInventory.save()
				else:
					AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
					inv = Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag)
					currentBorrow = int(inv[0][6])
					qtyToSubtract = int(qytDamage)
					finalQtyBorrowRemaining = currentBorrow - qtyToSubtract
					currentQty = int(inv[0][4])
					newQty = currentQty - qtyToSubtract
					print (finalQtyBorrowRemaining)
					Inventory.objects.filter(ItemUniqueID=rfidtag).update(QtyBorrowed=finalQtyBorrowRemaining, Quantity=newQty)
					inventory = AuditTable_Inventory.objects.all().values_list().filter(AuditID=id)
					item_id = Inventory.objects.get(ItemID=inventory[0][2])
					borrower = User.objects.get(UserID=inventory[0][6])
					admin = User.objects.get(UserID=inventory[0][7])
					auditInventory = AuditTable_Inventory(AuditAction=3, ItemID=item_id, Quantity=qytDamage, DateTime=datetime.datetime.now(), Borrower=borrower, Admin=admin)
					auditInventory.save()
					if newQty == 0:
						Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag).update(ItemStatus = 2)
			else:
				subtracted2 =  int(qty) - int(qtyReturn)
				if subtracted2 == 0:
					AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
					inv = Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag)
					currentBorrow = int(inv[0][6])
					qtyToSubtract = int(qytDamage)
					qtyToSubtract2 = int(qtyReturn)
					finalQtyBorrowRemaining = currentBorrow - qtyToSubtract2
					currentQty = int(inv[0][4])
					newQty = currentQty - qtyToSubtract
					print (finalQtyBorrowRemaining)
					Inventory.objects.filter(ItemUniqueID=rfidtag).update(QtyBorrowed=finalQtyBorrowRemaining, Quantity=newQty)
					inventory = AuditTable_Inventory.objects.all().values_list().filter(AuditID=id)
					item_id = Inventory.objects.get(ItemID=inventory[0][2])
					borrower = User.objects.get(UserID=inventory[0][6])
					admin = User.objects.get(UserID=inventory[0][7])
					auditInventory = AuditTable_Inventory(AuditAction=3, ItemID=item_id, Quantity=qytDamage, DateTime=datetime.datetime.now(), Borrower=borrower, Admin=admin)
					auditInventory.save()
					if newQty == 0:
						Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag).update(ItemStatus = 2)
				else:
					AuditTable_Inventory.objects.filter(AuditID=id).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
					inv = Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag)
					currentBorrow = int(inv[0][6])
					qtyToSubtract = int(qytDamage)
					qtyToSubtract2 = int(qtyReturn)
					finalQtyBorrowRemaining = currentBorrow - qtyToSubtract2
					currentQty = int(inv[0][4])
					newQty = currentQty - qtyToSubtract
					print (finalQtyBorrowRemaining)
					Inventory.objects.filter(ItemUniqueID=rfidtag).update(QtyBorrowed=finalQtyBorrowRemaining, Quantity=newQty)
					inventory = AuditTable_Inventory.objects.all().values_list().filter(AuditID=id)
					item_id = Inventory.objects.get(ItemID=inventory[0][2])
					borrower = User.objects.get(UserID=inventory[0][6])
					admin = User.objects.get(UserID=inventory[0][7])
					auditInventory = AuditTable_Inventory(AuditAction=1, ItemID=item_id, Quantity=subtracted2, DateTime=inventory[0][4], Borrower=borrower, Admin=admin, BorrowStatus=1)
					auditInventory.save()
					auditInventory = AuditTable_Inventory(AuditAction=3, ItemID=item_id, Quantity=qytDamage, DateTime=datetime.datetime.now(), Borrower=borrower, Admin=admin)
					auditInventory.save()
					if newQty == 0:
						Inventory.objects.all().values_list().filter(ItemUniqueID=rfidtag).update(ItemStatus = 2)
#########

# Create your views here.


# "request.user" is the function to call the API of Google+ to retrieve data such as email, name, etc.

def login(request):
	if request.user.is_authenticated: # Returns boolean if user has completed Google Auth Login
		if User.objects.filter(Email=request.user.email).exists(): # Retrieve E-mail of logged in user from, and if user is registered (exists in DB) do these
			UserType = User.objects.filter(Email=request.user.email).values('UserType'); # Assign User type of user to this variable based from the email
			UserStatus = User.objects.filter(Email=request.user.email).values('UserStatus'); # Assign User status of user to this variable
			if UserType.filter(UserType='1'): # Usertype 1 means user logged in is a STUDENT
				if UserStatus.filter(UserStatus='0'): # If user is still pending evaluation for an account, redirect to logout function (view)
					return redirect('logout') # Redirect to this function (view)
				else: # Else, if user has UserStatus is 1
					return redirect('Student/Profile') # Redirect to this templated (this is based off the Name="" on urls.py)
			elif UserType.filter(UserType='2'): # Usertype 2 means user is a FACULTY
					if UserStatus.filter(UserStatus='0'):
						return redirect('logout')
					else:
						return redirect('Faculty/Profile')
			elif UserType.filter(UserType='3'): # Usertpe 3 means user is a TECHNICIAN
				if UserStatus.filter(UserStatus='0'):
					return redirect('logout')
				else:
					return redirect('FacultyTech/Profile')
			elif UserType.filter(UserType='4'): # Usertype 4 means user is a FACUTLY TECHNICIAN
				if UserStatus.filter(UserStatus='0'):
					return redirect('logout')
				else:
					return redirect('Technician/Profile')
			elif UserType.filter(UserType='5'): # Usertype 5 means user is an ADMIN
				if UserStatus.filter(UserStatus='0'):
					return redirect('logout')
				else:
					return redirect('Admin/ManageUsers')
			elif UserType.filter(UserType='0'): # Default
				return redirect('logout')
		else: # If email does not exist in the DB, that user hasn't registered yet and redirect the user to this view
				return redirect('register')
	return render(request,'login.html') # This is out of the IF-ELSE condition, this will always return with the render of the login.html page

def student_check(user):
	user = User.objects.get(Email=user.email)
	print(user.UserType)
	if user.UserType != 1:
		return False
	else:
		return True

def faculty_check(user):
	user = User.objects.get(Email=user.email)
	print(user.UserType)
	if user.UserType != 2:
		return False
	else:
		return True

def facultytech_check(user):
	user = User.objects.get(Email=user.email)
	print(user.UserType)
	if user.UserType != 3:
		return False
	else:
		return True

def technician_check(user):
	user = User.objects.get(Email=user.email)
	print(user.UserType)
	if user.UserType != 4:
		return False
	else:
		return True

def admin_check(user):
	user = User.objects.get(Email=user.email)
	print(user.UserType)
	if user.UserType != 5:
		return False
	else:
		return True

def EvalUserAjax(request):

	Labs = Ref_Laboratory.objects.filter(Status='1')
	Degree = Ref_Degree.objects.all()
	Advisers = User.objects.filter(UserType='3')
	Advisers2 = User.objects.filter(UserType='2')
	Depts = Ref_Department.objects.all()
	result_list = list(chain(Labs, Degree, Advisers, Advisers2, Depts))

	item_serialized = serializers.serialize('json', result_list)

	return JsonResponse(item_serialized, safe=False)

def logout_view(request):
	UserStatus = User.objects.filter(Email=request.user.email).values('UserStatus'); # Get user userstatus
	if UserStatus.filter(UserStatus='0'): # User status of 0 means that the user pending evaluation.
		logout(request) # This method is created by django and is used to log out a session.
		return redirect('pending')

	else: # This is used for regular log outs.
		logout(request)
		return redirect('login')

def register(request):
	if request.method == 'POST':
		idnum = request.POST.get('idnum', '')
		emailadd = request.user.email
		fname = request.POST.get('first_name', '')
		lname = request.POST.get('last_name', '')
		mobileno = request.POST.get('mobileno', '')
		remarks = request.POST.get('remarks','')
		degreeno = request.POST.get('degree','')
		if(degreeno == '0'):
			degree = None
		else:
			degree = Ref_Degree.objects.get(DegreeID=degreeno)

		user_obj = User (Remarks=remarks, IDNumber = idnum, Email = emailadd, Name = fname +" " + lname, PhoneNumber = mobileno, Type=None, adviser=None,Degree=degree,group=None,Department=None,Laboratory=None)
		user_obj.save();
		return redirect('logout')
	else:
		print(request.user.email)
		email = request.user.email # Gets logged in user's email
		first_name = request.user.first_name # Gets logged in user's last
		last_name = request.user.last_name # Gets logged in user's first name
		Degree = Ref_Degree.objects.all()
		# Send data to template to render data to the screen
		return render(request,'register.html',{'email':email,'first_name':first_name,'last_name':last_name,'degree':Degree})


def pending(request):
	return render(request,'pending.html')

def SetResidencyAjax(request):
	if request.method == 'POST':
		labid = request.POST['labid']
		student_nfc = request.POST['student_nfc']

	if ResidencyTimeSlot.objects.filter(Laboratory=labid).exists():

		get_var = ResidencyTimeSlot.objects.filter(Laboratory=labid).latest('SchedVar')
		sched = ResidencyTimeSlot.objects.filter(Laboratory=labid).filter(SchedVar=get_var.SchedVar)

		if StudentResidencySchedule.objects.filter(Student=student_nfc).exists():
			schedvar = StudentResidencySchedule.objects.filter(Student=student_nfc).latest('RefSchedVar', 'StudentSchedVar') # get most updated LAB and STUDENT sched
			student_sched = StudentResidencySchedule.objects.filter(Student=student_nfc).filter(RefSchedVar=schedvar.RefSchedVar).filter(StudentSchedVar=schedvar.StudentSchedVar)
			result_list = list(chain(sched, student_sched))
			item_serialized = serializers.serialize('json', result_list)

		else:
			item_serialized = serializers.serialize('json', sched)

		return JsonResponse(item_serialized, safe=False)

	else:

		return JsonResponse(NULL, safe=False)

def EditGroupAjax(request):
	if request.method == 'POST':
		id = request.POST['id']

	grouptoedit = Group.objects.filter(GroupID=id)
	members = User.objects.filter(group=id, UserType='1')
	notmembers = User.objects.filter(group__isnull=True, UserType='1')
	labs = Ref_Laboratory.objects.all()
	result_list = list(chain(grouptoedit, members, notmembers, labs))
	item_serialized = serializers.serialize('json', result_list, use_natural_foreign_keys=True)

	return JsonResponse(item_serialized, safe=False)

def EditUserAjax(request):
	if request.method == 'POST':
		id = request.POST['dbtableid']

	usertoedit = User.objects.filter(UserID=id)
	laboratories = Ref_Laboratory.objects.all()
	roles = Ref_UserType.objects.all()

	if User.objects.get(UserID=id).UserType == 1:
		a = User.objects.get(UserID=id)
		if a.adviser == '':
			print(a.adviser)
			aa = a.adviser.UserID
			adviser = User.objects.filter(UserID=aa)
			result_list = list(chain(usertoedit, adviser, laboratories, roles))

		else:
			result_list = list(chain(usertoedit,laboratories,roles))

	else:
		result_list = list(chain(usertoedit,laboratories,roles))

	item_serialized = serializers.serialize('json', result_list, use_natural_foreign_keys=True) #use this parameter to get foreign key objects
	return JsonResponse(item_serialized, safe=False)

def EditLabAjax(request):
	if request.method == 'POST':

		tableid = request.POST['tableid']
		labtoedit = Ref_Laboratory.objects.filter(LabID=tableid)
		lab_serialized = serializers.serialize('json', labtoedit)

		if ResidencyTimeSlot.objects.filter(Laboratory=tableid).exists():
			get_var = ResidencyTimeSlot.objects.filter(Laboratory=tableid).latest('SchedVar')
			sched = ResidencyTimeSlot.objects.filter(Laboratory=tableid).filter(SchedVar=get_var.SchedVar)
			result_list = list(chain(labtoedit, sched))
			lab_serialized = serializers.serialize('json', result_list)
			return JsonResponse(lab_serialized, safe=False)

		else:
			return JsonResponse(lab_serialized, safe=False)

def BorrowItemAjax(request):
	if request.method == 'POST':
		id = request.POST['id']
		itemtoborrow = Inventory.objects.filter(ItemID=id )
		item_serialized = serializers.serialize('json', itemtoborrow)
		return JsonResponse(item_serialized, safe=False)

def BorrowItemManAjax(request):
	if request.method == 'POST':
		uniqueid = request.POST['uniqueid']
		itemtoborrow2 = Inventory.objects.filter(ItemUniqueID=uniqueid )
		item2_serialized = serializers.serialize('json', itemtoborrow2)

		return JsonResponse(item2_serialized, safe=False)

def UserInfoAjax(request):
	if request.method == 'POST':
		studentid = request.POST['studentid']
		userinfo = User.objects.filter(NFCUniqueID=studentid)
		user_serialized = serializers.serialize('json', userinfo)

		return JsonResponse(user_serialized, safe=False)


def SchedAjax(request):
	if request.method == 'POST':
		id = request.POST['tableid']
		sched = ResidencyTimeSlot.objects.filter(Laboratory=id)
		item_serialized = serializers.serialize('json', sched)

		return JsonResponse(item_serialized, safe=False)



def timeinout(request):
	if request.method == 'POST':
		return render(request, 'timein-out.html')
	else:
		return render(request, 'timein-out.html')

		labtoedit = Ref_Laboratory.objects.filter(LabID=tableid)

#<--ADMIN-->
def AdminDashboard(request):
	return render(request, 'Admin/AdminDashboard.html')

@login_required
@user_passes_test(admin_check,redirect_field_name='Admin/Calendar')
def AdminCalendar(request):
	return render(request, 'Admin/AdminCalendar.html')

def AdminInbox(request):
	return render(request, 'Admin/AdminInbox.html')

def AdminAddUser(request):
	if request.method == 'POST':
		accounttype = request.POST.get('accounttype', '')
		email = request.POST.get('email', '')
		user_obj = User(UserType=accounttype,Email=email,Type=Ref_UserType.objects.get(UserTypeID=accounttype),Department=None,group=None,Degree=None,adviser=None,Laboratory=None)
		user_obj.save()

	return render(request, 'Admin/AddUser.html')

@login_required
@user_passes_test(admin_check,redirect_field_name='Admin/ManageUsers')
def AdminManageUsers(request):
	Users = User.objects.filter(UserStatus=1) |  User.objects.filter(UserStatus=2) # because userstatus=0 is PENDING

	if request.method == 'POST':

		userid = request.POST.get('submit', '')
		usertype = request.POST.get('type', '')
		idnum = request.POST.get('idnum', '')
		role = request.POST.get('role', '')
		name = request.POST.get('name', '')
		pnumber = request.POST.get('pnumber', '')
		status = request.POST.get('status', '')

		if usertype == '1': #Student
			adviser = request.POST.get('adviser', '')
			lab = request.POST.get('lab', '')
			User.objects.filter(UserID=userid).update(Name=name, IDNumber=idnum, PhoneNumber=pnumber, adviser=adviser, Laboratory=lab, UserStatus=status, Type=role, UserType=role)
		elif usertype == '3' or usertype == '4': #Faculty-Tech or Technician
			lab = request.POST.get('lab', '')
			User.objects.filter(UserID=userid).update(Name=name, IDNumber=idnum, PhoneNumber=pnumber, Laboratory=lab, UserStatus=status, Type=role, UserType=role)

		else: #Faculty or Admin
			User.objects.filter(UserID=userid).update(Name=name, IDNumber=idnum, PhoneNumber=pnumber, UserStatus=status, Type=role, UserType=role)

		return render(request, 'Admin/AdminManageUsers.html',{'Users':Users, 'Check': ['Success']})
	else:
		print(Users)
		return render(request, 'Admin/AdminManageUsers.html',{'Users':Users})


def AdminBorrowItem(request):
	return render(request, 'Admin/AdminBorrowItem.html')

def AdminReturnItem(request):
	return render(request, 'Admin/AdminReturnItem.html')

def AdminReturnItem2(request):
	return render(request, 'Admin/AdminReturnItem2.html')

def AdminViewInventory(request):
	return render(request, 'Admin/AdminViewInventory.html')

@login_required
@user_passes_test(admin_check,redirect_field_name='Admin/AddItem')
def AdminAddItem(request):
	if request.method == 'POST':
		itemname = request.POST.get('itemname', '')
		description = request.POST.get('description', '')
		item_type = request.POST.get('item_type', '')
		quantity = request.POST.get('quantity', '')
		uid = request.POST.get('uid', '')

		inventory_obj = Inventory(ItemName=itemname, Description=description, ItemType=item_type, Quantity=quantity, ItemUniqueID=uid)
		inventory_obj.save()
		item_id = Inventory.objects.get(ItemID=inventory_obj.pk)
		admin = User.objects.get(Email=request.user.email)
		auditInventory = AuditTable_Inventory(AuditAction=2, ItemID=item_id, Quantity=quantity, DateTime=datetime.datetime.now(),  Admin=admin)
		auditInventory.save()

		return render(request,'Admin/AdminAddItem.html', {'Check': ['Success']})
	else:
		return render(request, 'Admin/AdminAddItem.html')

def AdminViewResidencies(request):
	return render(request, 'Admin/AdminViewResidencies.html')

def AdminEvaluateResidency(request):
	return render(request, 'Admin/AdminEvaluateResidency.html')

def AdminManageTerm(request):
	return render(request, 'Admin/AdminManageTerm.html')

def AdminResidencyReport(request):
	return render(request, 'Admin/AdminResidencyReport.html')

def AdminInventoryReport(request):
	borrowed = AuditTable_Inventory.objects.filter(AuditAction='1')
	audit = AuditTable_Inventory.objects.filter(AuditAction='2')
	incident = AuditTable_Inventory.objects.filter(AuditAction='4') | AuditTable_Inventory.objects.filter(AuditAction='5')
	return render(request, 'Admin/AdminInventoryReport.html',{'borrowed':borrowed,'audit':audit,'incident':incident})


@login_required
@user_passes_test(admin_check,redirect_field_name='Admin/AddLaboratory')
def AdminAddLaboratory(request):
	laboratories = Ref_Laboratory.objects.all().values_list()

	if request.method == 'POST':

		labid = request.POST.get('labid', '')

		if labid == '': #result is not NULL or NONE but a black value ''
			labname = request.POST.get('labname', '')
			roomno = request.POST.get('roomno', '')
			capacity = request.POST.get('capacity', '')
			inventory_obj = Ref_Laboratory(LaboratoryName=labname, RoomNum=roomno, Capacity=capacity)
			inventory_obj.save()

		else:
			labid = request.POST.get('labid', '')
			Ref_Laboratory.objects.filter(LabID=labid).update(LaboratoryName=labname,RoomNum=roomno, Capacity=capacity)


		return render(request,'Admin/AdminAddLaboratory.html', {'Labs': laboratories,'Check': ['Success']})

	else:
		return render(request, 'Admin/AdminAddLaboratory.html', {
		'Labs': laboratories
		})

@login_required # Self descriptive, this enforces that you should login before accessing this view which renders the template (webpage).
@user_passes_test(admin_check, redirect_field_name='Admin/EditLaboratory') # This function runs the function inside its parameter to verify the user

def AdminEditLaboratory(request):
	laboratories = Ref_Laboratory.objects.all().values_list()

	if request.method == 'POST':

		labname = request.POST.get('labname', '')
		roomno = request.POST.get('roomno', '')
		capacity = request.POST.get('capacity', '')
		labid = request.POST.get('labid', '')
		status = request.POST.get('status', '')
		sched = request.POST.getlist('sched[]', '')
		lab = Ref_Laboratory.objects.all().filter(LabID=labid)

		if (len(sched) > 0):

			changes = False
			lab_obj = Ref_Laboratory.objects.get(LabID=labid)

			if ResidencyTimeSlot.objects.filter(Laboratory=labid).exists():

				get_var = ResidencyTimeSlot.objects.latest('SchedVar', )
				next_var = get_var.SchedVar + 1
				old_sched = ResidencyTimeSlot.objects.filter(Laboratory=labid).filter(SchedVar=get_var.SchedVar) # current sched used

				if len(sched) != old_sched.count(): #automatically edited since size is not the same

					for m in range(0, len(sched)):
						newsched = ResidencyTimeSlot(Laboratory=lab_obj, Schedule=sched[m], TotalSlot = lab[0].Capacity, TakenSlot=0, SchedVar=next_var);
						newsched.save()

				elif len(sched) == old_sched.count(): #find if changes are made

					for m in range (0, old_sched.count()):
						if old_sched[m].Schedule != sched[m]:
							changes = True

					if changes:

						for x in range (0, len(sched)):
							newsched = ResidencyTimeSlot(Laboratory=lab_obj, Schedule=sched[x], TotalSlot = lab[0].Capacity, TakenSlot=0, SchedVar=next_var);
							newsched.save()

					else:
						print('no changes')

			else:

				next_var = 0;

				for m in range(0, len(sched)):
					newsched = ResidencyTimeSlot(Laboratory=lab_obj, Schedule=sched[m], TotalSlot = lab[0].Capacity, TakenSlot=0, SchedVar=next_var);
					newsched.save()

		Ref_Laboratory.objects.filter(LabID=labid).update(LaboratoryName=labname,RoomNum=roomno, Capacity=capacity, Status=status)
		return render(request, 'Admin/AdminAddLaboratory.html', {'Labs': laboratories, 'Check': ['Success']})

	else:
		return render(request, 'Admin/AdminAddLaboratory.html', {
		'Labs': laboratories
		})

#<--END-->

#<--STUDENT-->
@login_required
@user_passes_test(student_check,redirect_field_name='Student/Profile')
def StudentProfile(request):
	if request.method == 'POST':
		idno = request.POST.get('idnum', '')
		name = request.POST.get('fullname', '')
		mno = request.POST.get('mobileno', '')
		degree = request.POST.get('degree', '')
		deg = Ref_Degree.objects.get(DegreeID=degree)
		student_obj = User.objects.filter(Email=request.user.email).update(IDNumber=idno,Name=name,PhoneNumber=mno,Degree=deg)
		student_obj.save()
		return redirect('Student/Profile')
	student = User.objects.get(Email=request.user.email)
	group_members = User.objects.filter(group=student.group)
	degree = Ref_Degree.objects.all()
	return render(request, 'Students/StudentProfile.html',{'student':student,'group_members':group_members,'degree':degree})

def StudentDashboard(request):
	Users = User.objects.filter(UserType="2")
	degree = Ref_Degree.objects.all()
	email = request.user.email
	first_name = request.user.first_name
	last_name = request.user.last_name
	return render(request,'Students/StudentDashboard.html',{'Users':Users,'first_name':first_name,'last_name':last_name,'email':email,'degree':degree})

def StudentDashboard2(request):
	return render(request, 'Students/StudentDashboard2.html')

def StudentInbox(request):
	return render(request, 'Students/StudentInbox.html')

def StudentBorrowItem(request):
	return render(request, 'Students/StudentBorrowItem.html')

def StudentReturnItem(request):
	return render(request, 'Students/StudentReturnItem.html')

def StudentReturnItem2(request):
	return render(request, 'Students/StudentReturnItem2.html')

@login_required
@user_passes_test(student_check,redirect_field_name='Student/SetResidency')
def StudentSetResidency(request):

	# do login session

	student = User.objects.get(Email=request.user.email)

	if ResidencyTimeSlot.objects.filter(Laboratory=student.Laboratory.LabID).exists():

		get_var = ResidencyTimeSlot.objects.filter(Laboratory=student.Laboratory.LabID).latest('SchedVar')
		l_var = get_var.SchedVar

		if request.method == 'POST':

			sched = request.POST.getlist('sched[]', '')
			student_id = request.POST.get('student_id', '')
			lab = request.POST.get('lab_id', '')
			lab_var = request.POST.get('lab_var', '')
			changes = False

			if sched == '':
				return render(request, 'Students/StudentSetResidency.html', {'student':student, 'edit':3 })

			elif sched == '' and lab_var != '':
				return render(request, 'Students/StudentSetResidency.html', {'student':student, 'lab_var':l_var, 'edit':0 })

			else:

				if StudentResidencySchedule.objects.filter(Student=student_id).exists():

					schedvar = StudentResidencySchedule.objects.filter(Student=student_id).latest('RefSchedVar' ,'StudentSchedVar')
					old_sched = StudentResidencySchedule.objects.filter(Student=student_id).filter(RefSchedVar=schedvar.RefSchedVar).filter(StudentSchedVar=schedvar.StudentSchedVar)

					if len(sched) != old_sched.count():
						changes = True

					elif len(sched) == old_sched.count():

						for k in range(0, old_sched.count()):

							print('NEW: ' + sched[k] + ' | OLD: ' + old_sched[k].Schedule)

							if sched[k] != old_sched[k].Schedule:
								changes = True

					if changes:

						#outdated sched from lab
						if not StudentResidencySchedule.objects.filter(Student=student_id).filter(RefSchedVar=lab_var).exists():

							for i in range(0, len(sched)):

								ressched = StudentResidencySchedule(Student=student_id, Schedule=sched[i], RefSchedVar=lab_var)
								ressched.save()

								rt = ResidencyTimeSlot.objects.all().filter(Schedule=sched[i], Laboratory=lab, SchedVar=lab_var)
								x = rt[0].TakenSlot + 1
								rt.update(TakenSlot=x)

						else: #just editing current lab sched and has updated schedule from lab

							next_var = schedvar.StudentSchedVar + 1

							for m in range(0, old_sched.count()):

								rts = ResidencyTimeSlot.objects.all().filter(Schedule=old_sched[m].Schedule, Laboratory=lab, SchedVar=lab_var)
								x = rts[0].TakenSlot - 1
								rts.update(TakenSlot=x)

							for i in range(0, len(sched)):

								ressched = StudentResidencySchedule(Student=student_id, Schedule=sched[i], StudentSchedVar=next_var, RefSchedVar=lab_var)
								ressched.save()

								rt = ResidencyTimeSlot.objects.all().filter(Schedule=sched[i], Laboratory=lab, SchedVar=lab_var)
								x = rt[0].TakenSlot + 1
								rt.update(TakenSlot=x)

						return render(request, 'Students/StudentSetResidency.html', {'student':student, 'lab_var':l_var, 'edit':1}) #edited

					else:

						return render(request, 'Students/StudentSetResidency.html', {'student':student, 'lab_var':l_var, 'edit':0}) #no edit

				else:

					for i in range(0, len(sched)):

						ressched = StudentResidencySchedule(Student=student_id, Schedule=sched[i], RefSchedVar=lab_var)
						ressched.save()

						rt = ResidencyTimeSlot.objects.all().filter(Schedule=sched[i], Laboratory=lab, SchedVar=lab_var)
						x = rt[0].TakenSlot + 1
						rt.update(TakenSlot=x)

					return render(request, 'Students/StudentSetResidency.html', {'student':student, 'lab_var':l_var, 'edit':2})	#created first sched				

		else:
			return render(request, 'Students/StudentSetResidency.html', {'student':student, 'lab_var':l_var})

	else: #lab no sched available yet
		return render(request, 'Students/StudentSetResidency.html', {'student':student})

def StudentHome(request):
	borrowed = AuditTable_Inventory.objects.filter(AuditAction='1').filter(Borrower=User.objects.get(Email=request.user.email)).filter(DateTimeReturned=None)
	print(borrowed)
	return render(request, 'Students/StudentHome.html',{'borrowed':borrowed})

def StudentEditResidency(request):
	return render(request, 'Students/StudentEditResidency.html')

@login_required
@user_passes_test(student_check,redirect_field_name='Student/GroupInventory')
def StudentGroupInventory(request):
	borrowed = AuditTable_Inventory.objects.filter(AuditAction='1').filter(Borrower=User.objects.get(Email=request.user.email))
	print(borrowed)
	audit = AuditTable_Inventory.objects.filter(AuditAction='2')
	incident = AuditTable_Inventory.objects.filter(AuditAction='4') | AuditTable_Inventory.objects.filter(AuditAction='5')
	return render(request, 'Students/StudentInventoryReport.html',{'borrowed':borrowed,'audit':audit,'incident':incident})

@login_required
@user_passes_test(student_check,redirect_field_name='Student/ResidencyReport')
def StudentResidencyReport(request):
	user = User.objects.get(Email=request.user.email)
	schedule = StudentResidencySchedule.objects.filter(Student=user.NFCUniqueID)
	actual = ActualResidency.objects.filter(Student=user)
	monday = []
	tuesday = []
	wednesday = []
	thursday = []
	friday = []
	actual_residency = []
	a_total = 0
	for a in actual:
		timein = a.TimeIn
		timeout = a.TimeOut
		timein2 = timein.strftime("%I:%M%p")
		timeout2 =timeout.strftime("%I:%M%p")
		DateTime1 = datetime.datetime.strptime(timein2,'%I:%M%p')
		DateTime2 = datetime.datetime.strptime(timeout2,'%I:%M%p')
		dateTimeDifference = DateTime2 - DateTime1
		FMT = '%H:%M:%S'
		tt = dateTimeDifference.total_seconds()
		tdelta = str(timedelta(seconds=tt))
		a_total = a_total + tt
		split2 = tdelta.split(":")
		Hours = split2[0]
		minutes = split2[1]
		if Hours != '0':
			duration = Hours + " hours, " + minutes + " minutes"
		else:
			duration = minutes + " minutes"
		actual_residency.append({'Date':datetime.datetime.strftime(a.DateTime, '%b, %d %Y'),'Day':a.DateTime.strftime("%A"),
		'Start':a.TimeIn.__format__("%I:%M%p"),'End':a.TimeOut.__format__("%I:%M%p"),'Duration':duration})
	adelta = str(timedelta(seconds=a_total))
	aplit2 = adelta.split(":")
	Hours1 = aplit2[0]
	minutes1 = aplit2[1]
	if Hours1 != '0':
		actual_total = Hours1 + " hours, " + minutes1 + " minutes"
	else:
		actual_total = minutes1 + " minutes"

	for s in schedule:
		sched_list = s.Schedule.split('_')
		if sched_list[0] == 'M':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			monday.append(final)
		elif sched_list[0] == 'T':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			tuesday.append(final)
		elif sched_list[0] == 'W':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			wednesday.append(final)
		elif sched_list[0] == 'H':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			thursday.append(final)
		elif sched_list[0] == 'F':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			friday.append(final)

	mon = sorted(monday)
	tue = sorted(tuesday)
	wed = sorted(wednesday)
	thru = sorted(thursday)
	fri = sorted(friday)
	get_max = []
	get_max.append(len(mon))
	get_max.append(len(tue))
	get_max.append(len(wed))
	get_max.append(len(thru))
	get_max.append(len(fri))
	max1 = sorted(get_max)
	max = max1[4]
	data = []

	counter = 1
	while counter < max + 1:
		if len(mon) < counter:
			mon.append('---')
		if len(tue) < counter:
			tue.append('---')
		if len(wed) < counter:
			wed.append('---')
		if len(thru) < counter:
			thru.append('---')
		if len(fri) < counter:
			fri.append('---')

		counter = counter + 1

	counter2 = 0
	while counter2 < max:
		data.append({'Monday':mon[counter2],'Tuesday':tue[counter2],'Wednesday':wed[counter2],'Thursday':thru[counter2],'Friday':fri[counter2]})
		counter2 = counter2 + 1

	return render(request,'Students/StudentResidencyReport.html',{'actual_total':actual_total,'actual_residency':actual_residency,'user':user,'data':data,'actual':actual})

#<--FACULTY-->

def FacultyDashboard(request):
	email = request.user.email
	first_name = request.user.first_name
	last_name = request.user.last_name
	departments = Ref_Department.objects.all()
	laboratory = Ref_Laboratory.objects.all()
	return render(request, 'Faculty/FacultyDashboard.html',{'first_name':first_name,'last_name':last_name,'email':email,'form':form,'departments':departments,'laboratory':laboratory})

@login_required
@user_passes_test(admin_check,redirect_field_name='Admin/EvaluateUser')
def AdminEvaluateUser(request):
	if request.method == 'POST':
		if 'reject' in request.POST:
			id = request.POST.get('reject', '')
			user = User.objects.get(UserID=id)
			user.UserStatus = '2'
			user.save()
		else: #accept
			id = request.POST.get('accept', '')
			user = User.objects.get(UserID=id)
			usertype = request.POST.get('accType', '')
			nfc = request.POST.get('nfc','')
			print(usertype)

		if (usertype == '1'):
				print(usertype)
				degree = request.POST.get('degree', '')
				adviser = request.POST.get('adviser', '')
				nfc = request.POST.get('nfc','')
				User.objects.filter(UserID=id).update(UserStatus='1',Degree=degree,adviser=adviser,UserType=usertype,Type=usertype,NFCUniqueID=nfc)
		elif (usertype == '2' or usertype == '3'):
				print('23')
				dept = request.POST.get('dept', '')
				lab = request.POST.get('lab', '')
				nfc = request.POST.get('nfc','')
				User.objects.filter(UserID=id).update(UserStatus='1',Department=dept,Laboratory=lab,UserType=usertype,Type=usertype,NFCUniqueID=nfc)

		elif (usertype == '4'):
				print('4')
				lab = request.POST.get('lab', '')
				nfc = request.POST.get('nfc','')
				User.objects.filter(UserID=id).update(UserStatus='1',Laboratory=lab,UserType=usertype,Type=usertype,NFCUniqueID=nfc)

		return redirect("Admin/EvaluateUser")

	Users = User.objects.filter(UserStatus="0")

	return render(request,'Admin/AdminEvaluateUser.html',{'Users':Users})

@login_required
@user_passes_test(faculty_check,redirect_field_name='Faculty/Profile')
def FacultyProfile(request):
	if request.method == 'POST':
		idno = request.POST.get('idnum', '')
		name = request.POST.get('fullname', '')
		mno = request.POST.get('mobileno', '')
		degree = request.POST.get('departments', '')
		deg = Ref_Department.objects.get(DepartmentID=degree)
		faculty_obj = User.objects.filter(Email=request.user.email).update(IDNumber=idno,Name=name,PhoneNumber=mno,Department=deg)
		return redirect('Faculty/Profile')
	faculty = User.objects.get(Email=request.user.email)
	departments = Ref_Department.objects.all()
	return render(request, 'Faculty/FacultyProfile.html',{'faculty':faculty,'departments':departments})

@login_required
@user_passes_test(faculty_check,redirect_field_name='Faculty/InventoryReport')
def FacultyInventoryReport(request):
	borrowed = AuditTable_Inventory.objects.filter(AuditAction='1')
	audit = AuditTable_Inventory.objects.filter(AuditAction='2')
	incident = AuditTable_Inventory.objects.filter(AuditAction='4') | AuditTable_Inventory.objects.filter(AuditAction='5')
	return render(request, 'Faculty/FacultyInventoryReport.html',{'borrowed':borrowed,'audit':audit,'incident':incident})

def FacultyCalendar(request):
	return render(request, 'Faculty/FacultyCalendar.html')

def FacultyInbox(request):
	return render(request, 'Faculty/FacultyInbox.html')

def FacultyBorrowItem(request):
	return render(request, 'Faculty/FacultyBorrowItem.html')

def FacultyReturnItem(request):
	return render(request, 'Faculty/FacultyReturnItem.html')

def FacultyReturnItem2(request):
	return render(request, 'Faculty/FacultyReturnItem2.html')

@login_required
@user_passes_test(faculty_check,redirect_field_name='Faculty/ViewResidencies')
def FacultyViewResidencies(request):
	if request.method == 'POST':
		request.session['userid'] = request.POST.get('user_id','')
		return redirect('Faculty/ResidencyReport')
	residency = StudentResidencySchedule.objects.all()
	val = []
	print(residency)
	if residency:
		for s in residency:
		 	val.append(User.objects.get(NFCUniqueID=s.Student))
	students = list(set(val))
	return render(request, 'Faculty/FacultyViewResidencies.html',{'students':students})

@login_required
@user_passes_test(faculty_check,redirect_field_name='Faculty/ResidencyReport')
def FacultyResidencyReport(request):
	user = User.objects.get(UserID=request.session['userid'])
	schedule = StudentResidencySchedule.objects.filter(Student=user.NFCUniqueID)
	actual = ActualResidency.objects.filter(Student=user)
	monday = []
	tuesday = []
	wednesday = []
	thursday = []
	friday = []
	actual_residency = []
	a_total = 0
	for a in actual:
		timein = a.TimeIn
		timeout = a.TimeOut
		timein2 = timein.strftime("%I:%M%p")
		timeout2 =timeout.strftime("%I:%M%p")
		DateTime1 = datetime.datetime.strptime(timein2,'%I:%M%p')
		DateTime2 = datetime.datetime.strptime(timeout2,'%I:%M%p')
		dateTimeDifference = DateTime2 - DateTime1
		FMT = '%H:%M:%S'
		tt = dateTimeDifference.total_seconds()
		tdelta = str(timedelta(seconds=tt))
		a_total = a_total + tt
		split2 = tdelta.split(":")
		Hours = split2[0]
		minutes = split2[1]
		if Hours != '0':
			duration = Hours + " hours, " + minutes + " minutes"
		else:
			duration = minutes + " minutes"
		actual_residency.append({'Date':datetime.datetime.strftime(a.DateTime, '%b, %d %Y'),'Day':a.DateTime.strftime("%A"),
		'Start':a.TimeIn.__format__("%I:%M%p"),'End':a.TimeOut.__format__("%I:%M%p"),'Duration':duration})
	adelta = str(timedelta(seconds=a_total))
	aplit2 = adelta.split(":")
	Hours1 = aplit2[0]
	minutes1 = aplit2[1]
	if Hours1 != '0':
		actual_total = Hours1 + " hours, " + minutes1 + " minutes"
	else:
		actual_total = minutes1 + " minutes"
	for s in schedule:
		sched_list = s.Schedule.split('_')
		if sched_list[0] == 'M':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			monday.append(final)
		elif sched_list[0] == 'T':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			tuesday.append(final)
		elif sched_list[0] == 'W':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			wednesday.append(final)
		elif sched_list[0] == 'H':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			thursday.append(final)
		elif sched_list[0] == 'F':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			friday.append(final)

	mon = sorted(monday)
	tue = sorted(tuesday)
	wed = sorted(wednesday)
	thru = sorted(thursday)
	fri = sorted(friday)
	get_max = []
	get_max.append(len(mon))
	get_max.append(len(tue))
	get_max.append(len(wed))
	get_max.append(len(thru))
	get_max.append(len(fri))
	max1 = sorted(get_max)
	max = max1[4]
	data = []

	counter = 1
	while counter < max + 1:
		if len(mon) < counter:
			mon.append('---')
		if len(tue) < counter:
			tue.append('---')
		if len(wed) < counter:
			wed.append('---')
		if len(thru) < counter:
			thru.append('---')
		if len(fri) < counter:
			fri.append('---')

		counter = counter + 1

	counter2 = 0
	while counter2 < max:
		data.append({'Monday':mon[counter2],'Tuesday':tue[counter2],'Wednesday':wed[counter2],'Thursday':thru[counter2],'Friday':fri[counter2]})
		counter2 = counter2 + 1

	return render(request,'Faculty/FacultyResidencyReport.html',{'actual_total':actual_total,'actual_residency':actual_residency,'user':user,'data':data,'actual':actual})
#<--END-->

@login_required
@user_passes_test(faculty_check,redirect_field_name='Faculty/ManageGroups')
def FacultyManageGroups(request):
	UserID = User.objects.get(Email=request.user.email)
	group_set = Group.objects.filter(Adviser=UserID.UserID)

	if request.method == 'POST':

		groupid = request.POST.get('submit', '')
		members = request.POST.getlist('members[]', '')
		orig_members = request.POST.getlist('orig_member_id[]', '')
		lab = request.POST.get('lab', '')
		groupname = request.POST.get('groupname', '')

		totalmem = 0

		for i in range(0, len(members)):
			User.objects.filter(UserID=members[i]).update(group=groupid, Laboratory=lab)
			totalmem = i + 1

		for c in range(0, len(orig_members)):
			if orig_members[c] not in members:
				User.objects.filter(UserID=orig_members[c]).update(group=None)

		Group.objects.filter(GroupID=groupid).update(lab=lab, GroupName=groupname, Members=totalmem)

		return render(request, 'Faculty/FacultyManageGroups.html', {'group_set':group_set, 'Check': ['Success']})

	return render(request, 'Faculty/FacultyManageGroups.html', {'group_set':group_set})

@login_required
@user_passes_test(faculty_check,redirect_field_name='Faculty/AddGroup')
def FacultyAddGroup(request):
	if request.method == 'POST':
		form = AddGroupForm(request.POST)
		if form.is_valid():
			adviser = User.objects.get(Email=request.user.email).get_id();
			groupname = request.POST.get('groupname', '')
			labID = request.POST.get('laboratory', '')

			group_obj = Group (GroupName=groupname,Adviser=adviser,lab=Ref_Laboratory.objects.get(LabID=labID))
			group_obj.save();

			select2 = request.POST.getlist('select2[]', '')

			for i in range(0, len(select2)):
				group_member = User.objects.get(UserID=select2[i])
				group_member.group= Group.objects.get(GroupID=group_obj.pk)
				group_member.save();
				counter = i + 1

			g = Group.objects.get(GroupID=group_obj.pk)
			g.Members = counter
			g.save();
			return redirect("Faculty/AddGroup")
	else:
		form = AddGroupForm()
		UserID = User.objects.get(Email=request.user.email);
		members = User.objects.filter(adviser=UserID).filter(group=None)
		lab = Ref_Laboratory.objects.all()


	return render(request, 'Faculty/FacultyAddGroup.html',{'form':form,'members':members,'lab':lab})

def FacultyEditGroup(request):
	return render(request, 'Faculty/FacultyEditGroup.html')
#<--END-->

#<--TECHNICIAN AND FACULTY TECHNICIAN-->
def FacultyTechDashboard(request):
	return render(request, 'FacultyTech/FacultyTechDashboard.html')

def FacultyTechCalendar(request):
	return render(request, 'FacultyTech/FacultyTechCalendar.html')

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/AddGroup')
def FacultyTechAddGroup(request):
	if request.method == 'POST':
		form = AddGroupForm(request.POST)
		if form.is_valid():
			adviser = User.objects.get(Email=request.user.email).get_id();
			groupname = request.POST.get('groupname', '')
			labID = request.POST.get('laboratory', '')

			group_obj = Group (GroupName=groupname,Adviser=adviser,lab=Ref_Laboratory.objects.get(LabID=labID))
			group_obj.save();

			select2 = request.POST.getlist('select2[]', '')

			for i in range(0, len(select2)):
				group_member = User.objects.get(UserID=select2[i])
				group_member.group= Group.objects.get(GroupID=group_obj.pk)
				group_member.save();
				counter = i + 1

			g = Group.objects.get(GroupID=group_obj.pk)
			g.Members = counter
			g.save();
			return redirect("FacultyTech/AddGroup")
	else:
		form = AddGroupForm()
		UserID = User.objects.get(Email=request.user.email);
		members = User.objects.filter(adviser=UserID).filter(group=None)
		lab = Ref_Laboratory.objects.all()


	return render(request, 'FacultyTech/FacultyTechAddGroup.html',{'form':form,'members':members,'lab':lab})

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/AddGroup')
def FacultyTechProfile(request):
		if request.method == 'POST':
			idno = request.POST.get('idnum', '')
			name = request.POST.get('fullname', '')
			mno = request.POST.get('mobileno', '')
			degree = request.POST.get('departments', '')
			deg = Ref_Department.objects.get(DepartmentID=degree)
			faculty_obj = User.objects.filter(Email=request.user.email).update(IDNumber=idno,Name=name,PhoneNumber=mno,Department=deg)
			return redirect('FacultyTech/Profile')
		faculty = User.objects.get(Email=request.user.email)
		departments = Ref_Department.objects.all()
		return render(request, 'FacultyTech/FacultyTechProfile.html',{'faculty':faculty,'departments':departments})

def FacultyTechInbox(request):
	return render(request, 'FacultyTech/FacultyTechInbox.html')

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/BorrowItem')
def FacultyTechBorrowItem(request):
	inventory = Inventory.objects.filter(ItemStatus='1').values_list()
	if request.method == 'POST':
		uniqueid = request.POST.get('unique_id', '')
		idborrow = request.POST.getlist('idborrow[]', '')
		qtyborrow = request.POST.getlist('qtyborrow[]', '')

		for i in range(0, len(idborrow)):
			invent = Inventory.objects.get(ItemID=idborrow[i])
			Borrower = User.objects.get(NFCUniqueID=uniqueid)
			admin = User.objects.get(Email=request.user.email)
			auditInventory = AuditTable_Inventory(AuditAction=1, ItemID=invent, Quantity=qtyborrow[i], DateTime=datetime.datetime.now(), Borrower=Borrower, Admin=admin, BorrowStatus=1)
			auditInventory.save()
			inv = Inventory.objects.all().values_list().filter(ItemID=idborrow[i])
			currentBorrow = int(inv[0][6])
			stringBorrow = str(qtyborrow[i])
			toBorrow = int(stringBorrow)
			totalBorrow = currentBorrow + toBorrow
			finalTotalBorrow = int(totalBorrow)
			Inventory.objects.filter(ItemID=idborrow[i]).update(QtyBorrowed=finalTotalBorrow)
		return render(request, 'FacultyTech/FacultyTechBorrowItem.html', {
			'inventory': inventory
		})

	else:
		print(inventory)
		return render(request, 'FacultyTech/FacultyTechBorrowItem.html', {
		'inventory': inventory
		})

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ReturnItem')
def FacultyTechReturnItem(request):
	if request.method == 'POST':
		uid = request.POST.get('uniqueid', '')
		return redirect(reverse("View2", args =[inventory, pastborrow, userinfo]))
	else:
		return render(request, 'FacultyTech/FacultyTechReturnItem.html')

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ReturnItem2')
def FacultyTechReturnItem2(request):
	if request.method == 'POST':
		returnitem = request.POST.getlist('itemreturn[]', '')
		for i in range(0, len(returnitem)):
			AuditTable_Inventory.objects.filter(AuditID=returnitem[i]).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
			auditlatest = AuditTable_Inventory.objects.all().values_list().filter(AuditID=returnitem[i])
			inv = Inventory.objects.all().values_list().filter(ItemID=auditlatest[0][2])
			currentBorrow = int(inv[0][6])
			qtyToSubtract = int(auditlatest[0][3])
			finalQtyBorrowRemaining = currentBorrow - qtyToSubtract
			print (finalQtyBorrowRemaining)
			Inventory.objects.filter(ItemID=auditlatest[0][2]).update(QtyBorrowed=finalQtyBorrowRemaining)
		return render(request, 'FacultyTech/FacultyTechReturnItem2.html')
	else:
		uid = request.GET.get('uniqueid')
		inventory = AuditTable_Inventory.objects.all().filter(Borrower=uid, BorrowStatus=1).values_list()
		pastborrow = AuditTable_Inventory.objects.all().filter(Borrower=uid, BorrowStatus=2).values_list()
		userinfo = User.objects.all().filter(NFCUniqueID=uid).values_list()
		print (inventory)
		print (pastborrow)
		print (userinfo)
		return render(request, 'FacultyTech/FacultyTechReturnItem2.html', {'inventory': inventory, 'pastborrow': pastborrow, 'userinfo': userinfo})

def FacultyTechBorrowedItems(request):
	return render(request, 'FacultyTech/FacultyTechBorrowedItems.html')

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ManageStudents')
def FacultyTechManageStudents(request):
	UserID = User.objects.get(Email=request.user.email)
	students_set = User.objects.filter(adviser=UserID.UserID)
	
	return render(request, 'FacultyTech/FacultyTechManageStudents.html', {'students_set':students_set, 'Check': ['Success']})
	
@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ManageGroups')
def FacultyTechManageGroups(request):
	UserID = User.objects.get(Email=request.user.email)
	group_set = Group.objects.filter(Adviser=UserID.UserID)

	if request.method == 'POST':

		groupid = request.POST.get('submit', '')
		members = request.POST.getlist('members[]', '')
		orig_members = request.POST.getlist('orig_member_id[]', '')
		lab = request.POST.get('lab', '')
		groupname = request.POST.get('groupname', '')

		totalmem = 0

		for i in range(0, len(members)):
			User.objects.filter(UserID=members[i]).update(group=groupid, Laboratory=lab)
			totalmem = i + 1

		for c in range(0, len(orig_members)):
			if orig_members[c] not in members:
				User.objects.filter(UserID=orig_members[c]).update(group=None)

		Group.objects.filter(GroupID=groupid).update(lab=lab, GroupName=groupname, Members=totalmem)

	return render(request, 'FacultyTech/FacultyTechManageGroups.html', {'group_set':group_set, 'Check': ['Success']})


@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ManageItems')
def FacultyTechManageItems(request):
	items = Inventory.objects.all();

	if request.method == 'POST':

		itemid = request.POST.get('id', '')
		name = request.POST.get('name', '')
		desc = request.POST.get('desc', '')
		qty = request.POST.get('qty', '')
		status = request.POST.get('status', '')

		orig_item = Inventory.objects.get(ItemID=itemid)
		Inventory.objects.filter(ItemID=itemid).update(ItemName=name, Description=desc, Quantity=qty, ItemStatus=status)
		user = User.objects.get(Email=request.user.email)
		id = user.UserID
		new_item = Inventory.objects.get(ItemID=itemid)
		admin = User.objects.get(UserID=id) # --- FIX ADMIN ID --- #
		print('ORIG: ' + str(orig_item.ItemStatus) + ' | NEW: ' + status)

		if str(orig_item.ItemStatus) != status:

			if status == '0': #disabled
				audit_inv_obj = AuditTable_Inventory(AuditAction='3', ItemID=new_item, DateTime=datetime.datetime.now(), Admin=admin) # --- FIX DATETIME --- #
				audit_inv_obj.save()

			else: #enabled
				audit_inv_obj = AuditTable_Inventory(AuditAction='4', ItemID=new_item, DateTime=datetime.datetime.now(), Admin=admin) # --- FIX DATETIME --- #
				audit_inv_obj.save()

		else:
			audit_inv_obj = AuditTable_Inventory(AuditAction='5', ItemID=new_item, DateTime=datetime.datetime.now(), Admin=admin) # --- FIX DATETIME --- #
			audit_inv_obj.save()

		return render(request, 'FacultyTech/FacultyTechManageItems.html', {'items': items})

	else:
		return render(request, 'FacultyTech/FacultyTechManageItems.html', {'items': items})




@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/AddItem')
def FacultyTechAddItem(request):
	if request.method == 'POST':
		itemname = request.POST.get('itemname', '')
		description = request.POST.get('description', '')
		item_type = request.POST.get('item_type', '')
		if (item_type == "big"):
			quantity = 1;
		else:
			quantity = request.POST.get('quantity', '')
		uid = request.POST.get('uid', '')



		inventory_obj = Inventory(ItemName=itemname, Description=description, ItemType=item_type, Quantity=quantity, ItemUniqueID=uid)
		inventory_obj.save()
		item_id = Inventory.objects.get(ItemID=inventory_obj.pk)
		admin = User.objects.get(Email=request.user.email)
		auditInventory = AuditTable_Inventory(AuditAction=2, ItemID=item_id, Quantity=quantity, DateTime=datetime.datetime.now(),  Admin=admin)
		auditInventory.save()

		return render(request,'FacultyTech/FacultyTechAddItem.html', {'Check': ['Success']})
	else:
		return render(request, 'FacultyTech/FacultyTechAddItem.html')

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ViewResidencies')
def FacultyTechViewResidencies(request):
	if request.method == 'POST':
		request.session['userid'] = request.POST.get('user_id','')
		return redirect('FacultyTech/ResidencyReport')
	residency = StudentResidencySchedule.objects.all()
	val = []
	for s in residency:
		 val.append(User.objects.get(NFCUniqueID=s.Student))
	students = list(set(val))
	return render(request, 'FacultyTech/FacultyTechViewResidencies.html',{'students':students})

def FacultyTechEvaluateResidency(request):
	return render(request, 'FacultyTech/FacultyTechEvaluateResidency.html')

def FacultyTechManageTerm(request):
	return render(request, 'FacultyTech/FacultyTechManageTerm.html')

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/GroupsInventory')
def FacultyTechInventoryReport(request):
	borrowed = AuditTable_Inventory.objects.filter(AuditAction='1')
	audit = AuditTable_Inventory.objects.filter(AuditAction='2')
	incident = AuditTable_Inventory.objects.filter(AuditAction='4') | AuditTable_Inventory.objects.filter(AuditAction='5')
	return render(request, 'FacultyTech/FacultyTechInventoryReport.html',{'borrowed':borrowed,'audit':audit,'incident':incident})

@login_required
@user_passes_test(facultytech_check,redirect_field_name='FacultyTech/ResidencyReport')
def FacultyTechResidencyReport(request):
	user = User.objects.get(UserID=request.session['userid'])
	schedule = StudentResidencySchedule.objects.filter(Student=user.NFCUniqueID)
	actual = ActualResidency.objects.filter(Student=user)
	monday = []
	tuesday = []
	wednesday = []
	thursday = []
	friday = []
	actual_residency = []
	a_total = 0
	for a in actual:
		timein = a.TimeIn
		timeout = a.TimeOut
		timein2 = timein.strftime("%I:%M%p")
		timeout2 =timeout.strftime("%I:%M%p")
		DateTime1 = datetime.datetime.strptime(timein2,'%I:%M%p')
		DateTime2 = datetime.datetime.strptime(timeout2,'%I:%M%p')
		dateTimeDifference = DateTime2 - DateTime1
		FMT = '%H:%M:%S'
		tt = dateTimeDifference.total_seconds()
		tdelta = str(timedelta(seconds=tt))
		a_total = a_total + tt
		split2 = tdelta.split(":")
		Hours = split2[0]
		minutes = split2[1]
		if Hours != '0':
			duration = Hours + " hours, " + minutes + " minutes"
		else:
			duration = minutes + " minutes"
		actual_residency.append({'Date':datetime.datetime.strftime(a.DateTime, '%b, %d %Y'),'Day':a.DateTime.strftime("%A"),
		'Start':a.TimeIn.__format__("%I:%M%p"),'End':a.TimeOut.__format__("%I:%M%p"),'Duration':duration})
	adelta = str(timedelta(seconds=a_total))
	aplit2 = adelta.split(":")
	Hours1 = aplit2[0]
	minutes1 = aplit2[1]
	if Hours1 != '0':
		actual_total = Hours1 + " hours, " + minutes1 + " minutes"
	else:
		actual_total = minutes1 + " minutes"
	for s in schedule:
		sched_list = s.Schedule.split('_')
		if sched_list[0] == 'M':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			monday.append(final)
		elif sched_list[0] == 'T':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			tuesday.append(final)
		elif sched_list[0] == 'W':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			wednesday.append(final)
		elif sched_list[0] == 'H':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			thursday.append(final)
		elif sched_list[0] == 'F':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			friday.append(final)

	mon = sorted(monday)
	tue = sorted(tuesday)
	wed = sorted(wednesday)
	thru = sorted(thursday)
	fri = sorted(friday)
	get_max = []
	get_max.append(len(mon))
	get_max.append(len(tue))
	get_max.append(len(wed))
	get_max.append(len(thru))
	get_max.append(len(fri))
	max1 = sorted(get_max)
	max = max1[4]
	data = []

	counter = 1
	while counter < max + 1:
		if len(mon) < counter:
			mon.append('---')
		if len(tue) < counter:
			tue.append('---')
		if len(wed) < counter:
			wed.append('---')
		if len(thru) < counter:
			thru.append('---')
		if len(fri) < counter:
			fri.append('---')

		counter = counter + 1

	counter2 = 0
	while counter2 < max:
		data.append({'Monday':mon[counter2],'Tuesday':tue[counter2],'Wednesday':wed[counter2],'Thursday':thru[counter2],'Friday':fri[counter2]})
		counter2 = counter2 + 1

	return render(request,'FacultyTech/FacultyTechResidencyReport.html',{'actual_total':actual_total,'actual_residency':actual_residency,'user':user,'data':data,'actual':actual})
#<--END-->

def FacultyTechLabReport(request):
	if request.method == 'POST':
		request.session['slotid'] = request.POST.get('slotid','')
		return redirect('FacultyTech/TimeslotReport')
	laboratory = User.objects.get(Email=request.user.email).Laboratory
	timeslots = ResidencyTimeSlot.objects.filter(Laboratory=laboratory)
	slots = []
	monday = []
	tuesday = []
	wednesday = []
	thursday = []
	friday = []
	for s in timeslots:
		sched_list = s.Schedule.split('_')
		if sched_list[0] == 'M':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			slots.append({'Sched':final,'Total':s.TotalSlot,'Taken':s.TakenSlot,'Available':s.TotalSlot-s.TakenSlot,'Name':s.Schedule})
			monday.append(slots)

		elif sched_list[0] == 'T':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			slots.append({'Sched':final,'Total':s.TotalSlot,'Taken':s.TakenSlot,'Available':s.TotalSlot-s.TakenSlot,'Name':s.Schedule})
			tuesday.append(slots)

		elif sched_list[0] == 'W':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			slots.append({'Sched':final,'Total':s.TotalSlot,'Taken':s.TakenSlot,'Available':s.TotalSlot-s.TakenSlot,'Name':s.Schedule})
			wednesday.append(slots)

		elif sched_list[0] == 'H':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			slots.append({'Sched':final,'Total':s.TotalSlot,'Taken':s.TakenSlot,'Available':s.TotalSlot-s.TakenSlot,'Name':s.Schedule})
			thursday.append(slots)

		elif sched_list[0] == 'F':
			a = sched_list[1].replace("+", ":")
			b = a.split('-')
			t1 = b[0]
			t2 = b[1]
			time1 = time.strftime("%I:%M",time.strptime(t1, "%H:%M"))
			time2 = time.strftime("%I:%M %p",time.strptime(t2, "%H:%M"))
			final = time1 + "-" + time2
			slots.append({'Sched':final,'Total':s.TotalSlot,'Taken':s.TakenSlot,'Available':s.TotalSlot-s.TakenSlot,'Name':s.Schedule})
			friday.append(slots)

		slots = []

	return render(request, 'FacultyTech/FacultyTechLabReport.html',{'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday})


def FacultyTechTimeslotReport(request):
	slotid = request.session['slotid']

	residency = StudentResidencySchedule.objects.filter(Schedule=slotid)
	print(residency)
	student_list = residency.values_list('Student')
	student_info = []
	for s in student_list:
		str = ''.join(s)
		user = User.objects.get(NFCUniqueID=str)
		student_info.append({'ID':user.UserID,'Name':user.Name,'Group':user.group.GroupName})


	return render(request, 'FacultyTech/FacultyTechTimeslotReport.html',{'student_info':student_info})
	return render(request, 'FacultyTech/FacultyTechTimeslotReport.html')

def FacultyTechGroupsInventory(request):
	return render(request, 'FacultyTech/FacultyTechGroupsInventory.html')
#<--END-->

#<--TECHNICIAN-->
def TechnicianDashboard(request):
	return render(request, 'Technician/TechnicianDashboard.html')

def TechnicianCalendar(request):
	return render(request, 'Technician/TechnicianCalendar.html')

@login_required
@user_passes_test(technician_check,redirect_field_name='Technician/Profile')
def TechnicianProfile(request):
	if request.method == 'POST':
		idno = request.POST.get('idnum', '')
		name = request.POST.get('fullname', '')
		mno = request.POST.get('mobileno', '')
		faculty_obj = User.objects.filter(Email=request.user.email).update(IDNumber=idno,Name=name,PhoneNumber=mno)
		return redirect('Technician/Profile')
	faculty = User.objects.get(Email=request.user.email)
	return render(request, 'Technician/TechnicianProfile.html',{'faculty':faculty})

def TechnicianInbox(request):
	return render(request, 'Technician/TechnicianInbox.html')

@login_required
@user_passes_test(technician_check,redirect_field_name='Technician/BorrowItem')
def TechnicianBorrowItem(request):
	inventory = Inventory.objects.filter(ItemStatus='1').values_list()
	if request.method == 'POST':
		uniqueid = request.POST.get('unique_id', '')
		idborrow = request.POST.getlist('idborrow[]', '')
		qtyborrow = request.POST.getlist('qtyborrow[]', '')

		for i in range(0, len(idborrow)):
			invent = Inventory.objects.get(ItemID=idborrow[i])
			Borrower = User.objects.get(NFCUniqueID=uniqueid)
			admin = User.objects.get(Email=request.user.email)
			auditInventory = AuditTable_Inventory(AuditAction=1, ItemID=invent, Quantity=qtyborrow[i], DateTime=datetime.datetime.now(), Borrower=Borrower, Admin=admin, BorrowStatus=1)
			auditInventory.save()
			inv = Inventory.objects.all().values_list().filter(ItemID=idborrow[i])
			currentBorrow = int(inv[0][6])
			stringBorrow = str(qtyborrow[i])
			toBorrow = int(stringBorrow)
			totalBorrow = currentBorrow + toBorrow
			finalTotalBorrow = int(totalBorrow)
			Inventory.objects.filter(ItemID=idborrow[i]).update(QtyBorrowed=finalTotalBorrow)
		return render(request, 'Technician/TechnicianBorrowItem.html', {
			'inventory': inventory
		})

	else:
		print(inventory)
		return render(request, 'Technician/TechnicianBorrowItem.html', {
		'inventory': inventory
		})

@login_required
@user_passes_test(technician_check,redirect_field_name='Technician/ReturnItem')
def TechnicianReturnItem(request):
	if request.method == 'POST':
		uid = request.POST.get('uniqueid', '')
		return redirect(reverse("View2", args =[inventory, pastborrow, userinfo]))
	else:
		return render(request, 'Technician/TechnicianReturnItem.html')

@login_required
@user_passes_test(technician_check,redirect_field_name='Technician/ReturnItem2')
def TechnicianReturnItem2(request):
	if request.method == 'POST':
		returnitem = request.POST.getlist('itemreturn[]', '')
		for i in range(0, len(returnitem)):
			AuditTable_Inventory.objects.filter(AuditID=returnitem[i]).update(DateTimeReturned=datetime.datetime.now(), BorrowStatus=2)
			auditlatest = AuditTable_Inventory.objects.all().values_list().filter(AuditID=returnitem[i])
			inv = Inventory.objects.all().values_list().filter(ItemID=auditlatest[0][2])
			currentBorrow = int(inv[0][6])
			qtyToSubtract = int(auditlatest[0][3])
			finalQtyBorrowRemaining = currentBorrow - qtyToSubtract
			print (finalQtyBorrowRemaining)
			Inventory.objects.filter(ItemID=auditlatest[0][2]).update(QtyBorrowed=finalQtyBorrowRemaining)
			return render(request, 'Technician/TechnicianReturnItem2.html')
	else:
		uid = request.GET.get('uniqueid')
		inventory = AuditTable_Inventory.objects.all().filter(Borrower=uid, BorrowStatus=1).values_list()
		pastborrow = AuditTable_Inventory.objects.all().filter(Borrower=uid, BorrowStatus=2).values_list()
		userinfo = User.objects.all().filter(NFCUniqueID=uid).values_list()
		print (inventory)
		print (pastborrow)
		print (userinfo)
		return render(request, 'Technician/TechnicianReturnItem2.html', {'inventory': inventory, 'pastborrow': pastborrow, 'userinfo': userinfo})

def TechnicianBorrowedItems(request):
	return render(request, 'Technician/TechnicianBorrowedItems.html')

@login_required
@user_passes_test(technician_check,redirect_field_name='Technician/AddItem')
def TechnicianAddItem(request):
	if request.method == 'POST':
		itemname = request.POST.get('itemname', '')
		description = request.POST.get('description', '')
		item_type = request.POST.get('item_type', '')
		quantity = request.POST.get('quantity', '')
		uid = request.POST.get('uid', '')

		inventory_obj = Inventory(ItemName=itemname, Description=description, ItemType=item_type, Quantity=quantity, ItemUniqueID=uid)
		inventory_obj.save()
		item_id = Inventory.objects.get(ItemID=inventory_obj.pk)
		admin = User.objects.get(Email=request.user.email)
		auditInventory = AuditTable_Inventory(AuditAction=2, ItemID=item_id, Quantity=quantity, DateTime=datetime.datetime.now(),  Admin=admin)
		auditInventory.save()

		return render(request,'Technician/TechnicianAddItem.html', {'Check': ['Success']})
	else:
		return render(request, 'Technician/TechnicianAddItem.html')

@login_required
@user_passes_test(technician_check,redirect_field_name='Technician/GroupsInventory')
def TechnicianGroupsInventory(request):
	borrowed = AuditTable_Inventory.objects.filter(AuditAction='1')
	audit = AuditTable_Inventory.objects.filter(AuditAction='2')
	incident = AuditTable_Inventory.objects.filter(AuditAction='4') | AuditTable_Inventory.objects.filter(AuditAction='5')
	return render(request, 'Technician/TechnicianInventoryReport.html',{'borrowed':borrowed,'audit':audit,'incident':incident})
#<--END-->
