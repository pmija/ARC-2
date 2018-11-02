from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^timeinout$', views.timeinout, name='timeinout'),
    url(r'^register$', views.register, name='register'),
    url(r'^pending$', views.pending, name='pending'),

    #<--------------DIRECTORIES------------>

    #<--ADMIN-->
    #Dashboard
    url(r'^Admin$', views.AdminDashboard, name='Admin/Dashboard'),
    url(r'^Admin/Calendar$', views.AdminCalendar, name='Admin/Calendar'),
    #Accounts
    url(r'^Admin/ManageUsers$', views.AdminManageUsers, name='Admin/ManageUsers'),
    url(r'Admin/AddUser$', views.AdminAddUser, name='Admin/AddUser'),
    #Inventory
    url(r'^Admin/ViewInventory$', views.AdminViewInventory, name='Admin/ViewInventory'),
    url(r'^Admin/AddItem$', views.AdminAddItem, name='Admin/AddItem'),
    #Residency
    url(r'^Admin/ViewResidencies$', views.AdminViewResidencies, name='Admin/ViewResidencies'),
    url(r'^Admin/EvaluateResidency$', views.AdminEvaluateResidency, name='Admin/EvaluateResidency'),
    url(r'^Admin/ManageTerm$', views.AdminManageTerm, name='Admin/ManageTerm'),
    #Item Lending
    url(r'^Admin/BorrowItem$', views.AdminBorrowItem, name='Admin/BorrowItem'),
    url(r'^Admin/ReturnItem$', views.AdminReturnItem, name='Admin/ReturnItem'),
    url(r'^Admin/ReturnItem2$', views.AdminReturnItem2, name='Admin/ReturnItem2'),
    #Reports
    url(r'^Admin/ResidencyReport$', views.AdminResidencyReport, name='Admin/ResidencyReport'),
    url(r'^Admin/InventoryReport$', views.AdminInventoryReport, name='Admin/InventoryReport'),
    #Inbox
    url(r'^Admin/Inbox$', views.AdminInbox, name='Admin/Inbox'),
    #Laboratory
    url(r'^Admin/AddLaboratory', views.AdminAddLaboratory, name='Admin/AddLaboratory'),
    url(r'^Admin/EditLaboratory$', views.AdminEditLaboratory, name='Admin/EditLaboratory'),

    #<--END-->

    #<--STUDENT-->
    #Profile
    url(r'Student/Profile$', views.StudentProfile, name='Student/Profile'),
    #Dashboard
    url(r'^Student$', views.StudentDashboard, name='Student/Dashboard'),
    url(r'^Student/Calendar$', views.StudentDashboard2, name='Student/Calendar'),
    #Item Lending
    url(r'^Student/BorrowItem$', views.StudentBorrowItem, name='Student/BorrowItem'),
    url(r'^Student/ReturnItem$', views.StudentReturnItem, name='Student/ReturnItem'),
    url(r'^Student/ReturnItem2$', views.StudentReturnItem2, name='Student/ReturnItem2'),
    #Inbox
    url(r'^Student/Inbox$', views.StudentInbox, name='Student/Inbox'),
    #Residency
    url(r'Student/SetResidency$', views.StudentSetResidency, name='Student/SetResidency'),
    url(r'Student/EditResidency$', views.StudentEditResidency, name='Student/EditResidency'),
    #Reports
    url(r'Student/GroupInventory$', views.StudentGroupInventory, name='Student/GroupInventory'),
    url(r'^Student/ResidencyReport$', views.StudentResidencyReport, name='Student/ResidencyReport'),
    #<--END-->

    #<--FACULTY-->
    #Dashboard
    url(r'^Faculty$', views.FacultyDashboard, name='Faculty/Dashboard'),
    url(r'^Faculty/Calendar$', views.FacultyCalendar, name='Faculty/Calendar'),
	url(r'^Faculty/Profile$', views.FacultyProfile, name='Faculty/Profile'),
    #Groups
    url(r'Admin/EvaluateUser$', views.AdminEvaluateUser, name='Admin/EvaluateUser'),
    url(r'Faculty/ManageGroups$', views.FacultyManageGroups, name='Faculty/ManageGroups'),
    url(r'Faculty/AddGroup$', views.FacultyAddGroup, name='Faculty/AddGroup'),
    url(r'Faculty/EditGroup$', views.FacultyEditGroup, name='Faculty/EditGroup'),
    #Residency
    url(r'^Faculty/ViewResidencies$', views.FacultyViewResidencies, name='Faculty/ViewResidencies'),
    #Item Lending
    url(r'^Faculty/BorrowItem$', views.FacultyBorrowItem, name='Faculty/BorrowItem'),
    url(r'^Faculty/ReturnItem$', views.FacultyReturnItem, name='Faculty/ReturnItem'),
    url(r'^Faculty/ReturnItem2$', views.FacultyReturnItem2, name='Faculty/ReturnItem2'),
    #Reports
    url(r'^Faculty/InventoryReport$', views.FacultyInventoryReport, name='Faculty/InventoryReport'),
    url(r'^Faculty/ResidencyReport$', views.FacultyResidencyReport, name='Faculty/ResidencyReport'),
    #Inbox
    url(r'^Faculty/Inbox$', views.FacultyInbox, name='Faculty/Inbox'),
    #<--END-->

    #<--TECHNICIAN AND FACULTY-TECHNICIAN-->
    #Dashboard
    url(r'^FacultyTech$', views.FacultyTechDashboard, name='FacultyTech/Dashboard'),
    url(r'^FacultyTech/Calendar$', views.FacultyTechCalendar, name='FacultyTech/Calendar'),
	url(r'^FacultyTech/Profile$', views.FacultyTechProfile, name='FacultyTech/Profile'),
    #Inventory
    url(r'^FacultyTech/AddItem$', views.FacultyTechAddItem, name='FacultyTech/AddItem'),
    url(r'^FacultyTech/ManageItems$', views.FacultyTechManageItems, name='FacultyTech/ManageItems'),
    #Residency
    url(r'^FacultyTech/AddGroup$', views.FacultyTechAddGroup, name='FacultyTech/AddGroup'),
    url(r'^FacultyTech/ManageGroups$', views.FacultyTechManageGroups, name='FacultyTech/ManageGroups'),
    #Residency
    url(r'^FacultyTech/ViewResidencies$', views.FacultyTechViewResidencies, name='FacultyTech/ViewResidencies'),
    url(r'^FacultyTech/EvaluateResidency$', views.FacultyTechEvaluateResidency, name='FacultyTech/EvaluateResidency'),
    url(r'^FacultyTech/ManageTerm$', views.FacultyTechManageTerm, name='FacultyTech/ManageTerm'),
    #Item Lending
    url(r'^FacultyTech/BorrowItem$', views.FacultyTechBorrowItem, name='FacultyTech/BorrowItem'),
    url(r'^FacultyTech/ReturnItem$', views.FacultyTechReturnItem, name='FacultyTech/ReturnItem'),
    url(r'^FacultyTech/ReturnItem2$', views.FacultyTechReturnItem2, name='FacultyTech/ReturnItem2'),
    #Reports
    url(r'^FacultyTech/ResidencyReport$', views.FacultyTechResidencyReport, name='FacultyTech/ResidencyReport'),
    url(r'^FacultyTech/InventoryReport$', views.FacultyTechInventoryReport, name='FacultyTech/InventoryReport'),
    url(r'^FacultyTech/BorrowedItems$', views.FacultyTechBorrowedItems, name='FacultyTech/BorrowedItems'),
    url(r'^FacultyTech/GroupsInventory$', views.FacultyTechGroupsInventory, name='FacultyTech/GroupsInventory'),
    #Inbox
    url(r'^FacultyTech/Inbox$', views.FacultyTechInbox, name='FacultyTech/Inbox'),
    #<--END-->



	#AJAX
    url(r'ajax/editlab', views.EditLabAjax, name='Admin/EditLabAjax'),
    url(r'ajax/borrowitem', views.BorrowItemAjax, name='FacultyTech/BorrowItemAjax'),
    url(r'ajax/manualborrowitem', views.BorrowItemManAjax, name='FacultyTech/BorrowItemManAjax'),
    url(r'ajax/getuserinfo', views.UserInfoAjax, name='FacultyTech/UserInfoAjax'),
    url(r'ajax/gettimein', views.TimeInOutAjax, name='TimeInOutAjax'),
    url(r'ajax/manageusers', views.EditUserAjax, name='Admin/EditUserAjax'),
    url(r'ajax/managegroups', views.EditGroupAjax, name='Admin/EditGroupAjax'),
    url(r'ajax/schedajax', views.SchedAjax, name='Admin/SchedAjax'),
	url(r'ajax/resajax', views.ResAjax, name='Admin/ResAjax'),
    url(r'ajax/inserttimein', views.TimeInAjax, name='Admin/TimeInAjax'),
    url(r'ajax/checkcapajax', views.CheckCapacityAjax, name='Admin/CheckCapacityAjax'),
    url(r'ajax/setresidency', views.SetResidencyAjax, name='Admin/SetResidencyAjax'),
    url(r'ajax/evaluser', views.EvalUserAjax, name='Admin/EvalUserAjax'),
    url(r'ajax/manageitems', views.ManageItemsAjax, name='FacultyTech/ManageItemsAjax'),
    url(r'ajax/itemdetails', views.ItemDetailsAjax, name='FacultyTech/ItemDetailsAjax'),
    url(r'ajax/itemlog', views.ItemLogAjax, name='FacultyTech/ItemLogAjax'),
    url(r'ajax/edititem', views.EditItemAjax, name='FacultyTech/EditItemAjax'),
	
	
	#NEW AJAX KIM
    url(r'ajax/getBorrowed', views.getBorrowed, name='getBorrowed'),
	url(r'ajax/returnItem', views.returnItem, name='returnItem'),
	#NFC
	url(r'ajax/nfcajax', views.NFCAjax, name='NFCAjax'),
	url(r'ajax/rfidajax', views.RFIDAjax, name='RFIDAjax'),
    #<-----------END OF DIRECTORIES--------->

#<--TECHNICIAN-->
    #Dashboard
    url(r'^Technician$', views.TechnicianDashboard, name='Technician/Dashboard'),
    url(r'^Technician/Calendar$', views.TechnicianCalendar, name='Technician/Calendar'),
    url(r'^Technician/Profile$', views.TechnicianProfile, name='Technician/Profile'),
    #Inventory
    url(r'^Technician/AddItem$', views.TechnicianAddItem, name='Technician/AddItem'),
    #Item Lending
    url(r'^Technician/BorrowItem$', views.TechnicianBorrowItem, name='Technician/BorrowItem'),
    url(r'^Technician/ReturnItem$', views.TechnicianReturnItem, name='Technician/ReturnItem'),
    url(r'^Technician/ReturnItem2$', views.TechnicianReturnItem2, name='Technician/ReturnItem2'),
    #Reports
    url(r'^Technician/BorrowedItems$', views.TechnicianBorrowedItems, name='Technician/BorrowedItems'),
    url(r'^Technician/GroupsInventory$', views.TechnicianGroupsInventory, name='Technician/GroupsInventory'),
    #Inbox
    url(r'^Technician/Inbox$', views.TechnicianInbox, name='Technician/Inbox'),
    #<--END-->
    ]
